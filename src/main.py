"""TSV to TXT Column Extractor - Extracts last column from TSV files."""
from pathlib import Path
import csv
import sys
from datetime import datetime
from loguru import logger
import chardet
from natsort import natsorted

INPUT_DIR = Path("USER-FILES/04.INPUT")
OUTPUT_DIR = Path("USER-FILES/05.OUTPUT")


def setup_logging() -> None:
    """Configure loguru for console-only output with INFO level."""
    logger.remove()
    logger.add(sys.stderr, format="<level>{message}</level>", level="INFO", colorize=True)


def get_timestamp() -> str:
    """Generate timestamp in YYMMDD_HHMMSS format (e.g., '250103_143022')."""
    return datetime.now().strftime("%y%m%d_%H%M%S")


def discover_tsv_files(input_dir: Path) -> list[Path]:
    """Find all .tsv files in input directory using natural sort."""
    tsv_files = list(input_dir.glob("*.tsv"))
    if not tsv_files:
        raise FileNotFoundError(f"No TSV files found in {input_dir}")
    return natsorted(tsv_files)  # Natural sort: file1, file2, file10


def detect_encoding(file_path: Path) -> str:
    """Detect file encoding using chardet, fallback to UTF-8 if confidence < 0.7."""
    with open(file_path, 'rb') as f:
        raw_data = f.read(10240)  # Read first 10KB
    result = chardet.detect(raw_data)
    encoding = result.get('encoding') or 'utf-8'
    confidence = result.get('confidence', 0)
    return 'utf-8' if confidence < 0.7 else encoding


def extract_last_column(tsv_path: Path, encoding: str) -> list[str]:
    """Extract last column from TSV, skipping header and empty rows."""
    extracted_values = []
    try:
        with open(tsv_path, 'r', encoding=encoding) as f:
            reader = csv.reader(f, delimiter='\t')
            next(reader, None)  # Skip header row
            for row in reader:
                if row:  # Skip empty rows
                    extracted_values.append(row[-1])  # Extract last column
    except UnicodeDecodeError as e:
        raise UnicodeDecodeError(
            e.encoding, e.object, e.start, e.end,
            f"Encoding error: unable to decode {tsv_path.name} with {encoding}"
        )
    except csv.Error as e:
        raise csv.Error(f"Invalid tab-delimited format in {tsv_path.name}: {e}")
    return extracted_values


def write_output(values: list[str], stem: str, output_dir: Path) -> None:
    """Write each extracted value to a separate markdown file."""
    output_dir.mkdir(parents=True, exist_ok=True)
    for idx, value in enumerate(values, start=1):
        output_path = output_dir / f"{stem}_{idx}.md"
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(value)


def process_file(tsv_path: Path, output_dir: Path) -> bool:
    """Process single TSV file: detect encoding, extract last column, write output."""
    filename = tsv_path.stem
    try:
        logger.info(f"Processing: {tsv_path.name}")
        encoding = detect_encoding(tsv_path)
        extracted_values = extract_last_column(tsv_path, encoding)
        file_output_dir = output_dir / filename
        write_output(extracted_values, filename, file_output_dir)
        logger.success(f"✓ Extracted {len(extracted_values)} files in {filename}/ ({len(extracted_values)} rows)")
        return True
    except Exception as e:
        logger.error(f"✗ Failed {tsv_path.name}: {e}")
        return False


def main() -> None:
    """Main entry point: discover TSV files, process each, report summary."""
    setup_logging()
    if not INPUT_DIR.exists():
        logger.error(f"Input directory not found: {INPUT_DIR}")
        sys.exit(1)
    try:
        tsv_files = discover_tsv_files(INPUT_DIR)
        timestamp = get_timestamp()
        output_dir = OUTPUT_DIR / f"{timestamp}_PROMPTS"
        success_count = 0
        total_count = len(tsv_files)
        for tsv_path in tsv_files:
            if process_file(tsv_path, output_dir):
                success_count += 1
        logger.info(f"Completed: {success_count}/{total_count} files processed successfully")
        sys.exit(0 if success_count > 0 else 1)
    except FileNotFoundError as e:
        logger.error(str(e))
        sys.exit(1)


if __name__ == "__main__":
    main()
