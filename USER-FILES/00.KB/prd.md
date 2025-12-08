# PRD - TSV to TXT Column Extractor

## 01. Project Definition

### 01.1 Project Description

A minimalist batch processing tool that extracts the last column from TSV files, removing the header row, and outputs the extracted data as plain text files with one value per line.

### 01.2 Core Features

- Batch process all TSV files in `USER-FILES/04.INPUT/`
- Remove first row (header) from each TSV file
- Extract last column (rightmost) from remaining rows
- Skip empty rows silently during processing
- Write extracted values to `.txt` files (one value per line)
- Generate timestamped output directories
- Handle encoding detection automatically with UTF-8 fallback
- Continue processing on individual file failures
- Preserve original data exactly as-is (no transformations)

### 01.3 Specific Requirements

**Input Requirements:**
- TSV files must use tab (`\t`) delimiter
- Files must be UTF-8 encoded (fail with clear error if not)
- Files must be located in `USER-FILES/04.INPUT/`
- Files must have at least one column
- First row is always treated as header and removed

**Processing Requirements:**
- Extract last column only (rightmost column)
- Skip completely empty rows without logging
- Write values exactly as-is with no whitespace stripping or normalization
- Validate each file just before processing it
- Continue processing remaining files if one fails

**Output Requirements:**
- Create timestamped output directory: `USER-FILES/05.OUTPUT/{YYMMDD_HHMMSS}/`
- Each input file gets its own subfolder: `{YYMMDD_HHMMSS}/{input_filename}/`
- Output filename: `{input_filename}.txt` (removes `.tsv` extension)
- Format: One extracted value per line in output file
- Preserve original data without modifications

**Error Handling Requirements:**
- Skip corrupted/malformed TSV files
- Log errors to console with clear messages
- Continue processing remaining files after errors
- Fail immediately if file is not tab-delimited
- Fail immediately if file is not UTF-8 encoded

**User Feedback Requirements:**
- Show which file is currently being processed
- Display success/failure status for each file
- Report total files processed at completion
- No progress bars (tool runs quickly on typical inputs)

### 01.4 Project Context

#### Personal Tool (LLM-Operated)

- **Users**: Just me (developer/owner)
- **Operation**: Claude Code or other LLM operates on my behalf
- **Documentation**: LLM-readable (clear docstrings and comments)
- **Testing**: I test manually myself - no automated tests, no test frameworks, no test suites
- **CI/CD**: Not needed (no team, no external deployment)
- **Simplification Impact**:
  - No user documentation needed
  - No automated testing whatsoever
  - No test files or test directories
  - No release management
  - No external integrations
  - Focus exclusively on building functional scripts

### 01.5 Error Handling Strategy

- **Corrupted input**: Skip file, log error to console, continue processing remaining files
- **Wrong encoding**: Fail immediately with clear error message indicating encoding issue
- **Non-tab delimiter**: Fail immediately with clear error message indicating delimiter issue
- **Empty input folder**: Fail immediately with clear error message
- **Missing last column**: Fail on that file with clear error, continue with remaining files
- **Output directory exists**: Create new timestamped folder (timestamps prevent conflicts)
- **Inconsistent column count**: Process rows with data, skip rows with no columns

---

## 02. Minimalist Architecture Philosophy

### Core Principles

**Simplicity First**

- Single-purpose tool: TSV last column extraction only
- No configuration files (hardcoded behavior)
- No profile system (single fixed behavior)
- No summary reports or analytics
- Standard library only (no external dependencies except loguru)
- Single Python file implementation
- Self-documenting code with clear variable names
- Functions under 50 lines
- No premature abstractions

### Python Implementation Standards

**Code Structure**

- Single file: `src/main.py` (estimated ~150-200 lines)
- Type hints for all functions
- pathlib.Path for file operations (never os.path)
- One purpose per function
- Functions under 50 lines
- Clear separation: input discovery → validation → processing → output

**Error Handling**

- Fail fast on encoding/delimiter issues
- Skip individual files on corruption, continue batch
- Clear, actionable error messages to console
- Log file name and specific error for each failure
- No silent failures

**Dependencies**

- Python standard library: `csv`, `pathlib`, `sys`, `datetime`
- `loguru` for console logging only
- `chardet` for encoding detection
- Pin exact versions in requirements.txt
- Virtual environment isolation

**File Processing**

- Sequential processing (deterministic, simple)
- Natural sorting of input files using `natsort`
- Validate file just before processing
- Write directly to output (no temp files needed for simple extraction)
- Handle encoding issues gracefully with clear errors

**Testing & Documentation**

- Build functional script - I test it manually myself
- No automated tests, no test frameworks, no test files
- LLM-readable docstrings in all functions
- Clear inline comments for TSV parsing logic
- No README needed (personal tool)

---

## 03. Dependencies

### Python Dependencies

```plaintext
# requirements.txt
loguru==0.7.2
chardet==5.2.0
natsort==8.4.0
```

### Folder Structure

```plaintext
tsv+prompt_to_txt_tool/
├── src/
│   └── main.py                # Single-file implementation
├── run.py                     # Venv activation wrapper
├── requirements.txt           # Python dependencies
├── .gitignore                 # Exclude USER-FILES data
└── USER-FILES/
    ├── 00.KB/                 # Knowledge base (PRD, manifesto, etc.)
    ├── 04.INPUT/              # Input TSV files (READ ONLY)
    ├── 05.OUTPUT/             # Generated outputs (WRITE ONLY)
    │   └── {YYMMDD_HHMMSS}/   # Timestamped run folders
    │       └── {filename}/    # Per-file output folders
    │           └── {filename}.txt
    └── 07.TEMP/               # Temporary files (questions, etc.)
```

---

## 04. Input/Output Pattern for Batch Processing Projects

### 04.1 Purpose and Scope

This tool follows the standard USER-FILES folder convention for batch processing. Users manage data organization; the script follows folder conventions.

**Key principle**: Users place files, script processes systematically.

### 04.2 Standard Folder Structure

```plaintext
tsv+prompt_to_txt_tool/
├── .gitignore                                        
└── USER-FILES/
    ├── 00.KB/                                         # Knowledge base and reference materials
    │   ├── prd.md                                     # This PRD document
    │   ├── idea_brief.md                              # Original idea outline
    │   ├── PRD_Instructions_Template.md               # PRD template
    │   ├── code_manifesto_memo.md                     # Coding philosophy
    │   ├── code_quantity_memo.md                      # File size guidelines
    │   └── code_progress_bar_manifesto.md             # Progress bar standards
    ├── 04.INPUT/                                      # Active input folder (script processes this)
    │   ├── data.tsv                                   # Example input file
    │   └── prompts.tsv                                # Example input file
    ├── 05.OUTPUT/                                     # Generated output files and folders
    │   └── {YYMMDD_HHMMSS}/                           # Folder created for each script run
    │       ├── data/                                  # Folder for data.tsv processing
    │       │   └── data.txt                           # Extracted last column
    │       └── prompts/                               # Folder for prompts.tsv processing
    │           └── prompts.txt                        # Extracted last column
    └── 07.TEMP/                                       # Temporary working files
        └── prd_questions.md                           # PRD clarification questions
```

### 04.3 Processing Flow

#### Before Processing

```plaintext
USER-FILES/04.INPUT/*.tsv → [Script Processing] → USER-FILES/05.OUTPUT/{timestamp}/{filename}/{filename}.txt
```

#### Processing States

```plaintext
[TSV Files in 04.INPUT] → [Validation] → [Header Removal] → [Last Column Extraction] → [TXT Output in 05.OUTPUT]
```

### 04.4 Folder Descriptions

| Folder      | Purpose                        | Script Access |
| ----------- | ------------------------------ | ------------- |
| 00.KB       | Knowledge base, reference docs | Read-only     |
| 04.INPUT    | Active processing queue        | Read-only     |
| 05.OUTPUT   | Timestamped results            | Write-only    |
| 07.TEMP     | Working files, reports         | Read/Write    |

### 04.5 User Workflow

#### Basic Processing Flow

1. **Prepare Files**: Place TSV files in `USER-FILES/04.INPUT/`
2. **Run Script**: Execute `python3 run.py`
3. **Check Output**: Results appear in `USER-FILES/05.OUTPUT/{timestamp}/`
4. **Archive**: Manually move processed files from `04.INPUT/` to archive location if desired

#### Example Workflow

**Standard Processing**

1. Place `data.tsv` in `04.INPUT/`
2. Run `python3 run.py`
3. Check `05.OUTPUT/250103_143022/data/data.txt`
4. Verify extracted column data
5. Manually archive `data.tsv` from `04.INPUT/` if needed

### 04.6 Output Organization

- Each processing run creates a timestamped folder in `05.OUTPUT/` using format `YYMMDD_HHMMSS`
- Each processed file gets its own subfolder with the extracted `.txt` file
- Failed files are logged to console (no separate failure files for this simple tool)
- No summary reports generated (minimalist approach)

### 04.7 Key Principles

#### Data Organization

- Users control where files are placed
- Script follows the established folder conventions
- Clear separation between input and output
- No configuration files needed

#### Processing Safety

- Original files are never modified in place
- All outputs are generated in timestamped folders
- Failed processing doesn't affect successful results
- Continue processing on individual failures

#### Configuration Separation

- No configuration files (hardcoded behavior)
- No profile system (single extraction mode)
- Reference materials kept in 00.KB
- Temporary files in 07.TEMP

### 04.8 Implementation Details

#### Logging Strategy

Simple console logging only:

- **Info Messages**: "Processing: {filename}.tsv"
- **Success Messages**: "✓ Extracted {filename}.txt ({row_count} rows)"
- **Error Messages**: "✗ Failed {filename}.tsv: {error_description}"
- **Summary**: "Completed: {success_count}/{total_count} files processed"

No log files generated (minimalist approach for simple tool).

#### File Naming and Organization

**Input Preservation**: Original filenames preserved (minus .tsv extension).

**Timestamped Outputs**: Format `YYMMDD_HHMMSS` prevents overwrites (e.g., `250103_143022`).

**Output Directory Naming**

- **Format**: `YYMMDD_HHMMSS` only (e.g., `250103_143022`)
- **No descriptive prefixes**: Follows PRD standard (no `_MULTI-LINE_PROMPT_TXT` suffix)
- **Consistency**: Clean timestamp-only format
- **Per-file organization**: Each processed file gets its own subfolder

**File Naming**: Remove `.tsv` extension from input filename (e.g., `data.tsv` → `data.txt`).

#### Error Handling and Recovery

- **Graceful Degradation**: Continue processing despite individual file failures
- **Clear Error Reporting**: Console messages with file name and error description
- **No Recovery Attempts**: Fail fast on encoding/delimiter issues, skip corrupted files
- **Performance**: Sequential processing (simple, deterministic)

#### Processing Mode

- **Extraction Mode**: Process all TSV files in INPUT, output to timestamped folders
- **No Configuration**: Single hardcoded behavior

#### Technical Implementation

**Script Flow**: 
1. Discover all `.tsv` files in `04.INPUT/` (using natsort)
2. Create timestamped output directory in `05.OUTPUT/`
3. For each TSV file:
   - Validate file exists and is readable
   - Detect encoding (prefer UTF-8)
   - Open with csv.reader, delimiter=`\t`
   - Skip first row (header)
   - Extract last column from each remaining row
   - Skip empty rows
   - Write to `{timestamp}/{filename}/{filename}.txt` (one value per line)
   - Log success or failure to console
4. Report final summary

**File Formats**: INPUT (TSV with tab delimiter), OUTPUT (TXT with one value per line)

**Logging**: Loguru to console only (no log files)

**Error Handling**: Continue on individual failures, detailed console messages

**Performance**: Sequential processing, no progress bars

### 04.9 Version Control Guidelines

#### .gitignore Configuration

```plaintext
# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.so
*.egg
*.egg-info/
dist/
build/
venv/
.venv/

# User data (DO NOT COMMIT)
USER-FILES/04.INPUT/*
USER-FILES/05.OUTPUT/*
USER-FILES/06.DONE/*
USER-FILES/07.TEMP/*

# Keep directory structure
!USER-FILES/04.INPUT/.gitkeep
!USER-FILES/05.OUTPUT/.gitkeep
!USER-FILES/06.DONE/.gitkeep
!USER-FILES/07.TEMP/.gitkeep

# Keep knowledge base
!USER-FILES/00.KB/*

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store
```

#### Rationale for Exclusion

1. **Repository Size Management**: Input and output files can be large
2. **Data Privacy**: Input files may contain sensitive information
3. **Reproducibility**: Output files are regenerated each run
4. **Focus on Code**: Version control focuses on processing logic, not data

#### Security Considerations

**Sensitive Data**

- Never commit input data files
- Never commit output files
- Keep only code and knowledge base in repository

**Data Privacy**

- Review files before committing any examples
- Use synthetic data for documentation if needed
- Document data format requirements without exposing actual data

#### How to Run the Script

- **Main entry point**: `python3 -m src.main` (with venv activated)
- **Wrapper script**: `run.py` activates venv and runs the main entry point
- **Usage**: `python3 run.py` handles venv activation automatically

---

## 05. Technical Specifications

### 05.1 Algorithm Overview

**Input Discovery Phase:**
```python
1. Validate USER-FILES/04.INPUT/ exists
2. Discover all *.tsv files using natsorted(Path.glob("*.tsv"))
3. If no files found, fail with clear error message
4. Create timestamped output directory: USER-FILES/05.OUTPUT/{YYMMDD_HHMMSS}/
```

**Processing Phase (per file):**
```python
1. Log: "Processing: {filename}.tsv"
2. Detect file encoding using chardet (fallback to UTF-8)
3. Open file with csv.reader(delimiter='\t')
4. Skip first row (header) using next(reader)
5. For each remaining row:
   - Skip if row is empty
   - Extract last column: row[-1]
   - Store in list
6. Create output subfolder: {timestamp}/{filename}/
7. Write to {filename}.txt (one value per line)
8. Log success with row count
```

**Error Handling (per file):**
```python
- If encoding error: Log error, skip file, continue
- If delimiter error: Log error, skip file, continue
- If no columns: Log error, skip file, continue
- If file not found: Log error, skip file, continue
```

**Completion Phase:**
```python
1. Report summary: "Completed: {success}/{total} files processed"
2. Exit with code 0 if any successes, 1 if all failed
```

### 05.2 Module Structure

**Single File: `src/main.py`**

Estimated structure (~150-200 lines total):

```python
# Imports (10 lines)
from pathlib import Path
import csv
import sys
from datetime import datetime
from loguru import logger
import chardet
from natsort import natsorted

# Constants (5 lines)
INPUT_DIR = Path("USER-FILES/04.INPUT")
OUTPUT_DIR = Path("USER-FILES/05.OUTPUT")

# Functions (120-150 lines)
def setup_logging() -> None:
    """Configure loguru for console output only."""
    
def get_timestamp() -> str:
    """Generate YYMMDD_HHMMSS timestamp."""
    
def discover_tsv_files(input_dir: Path) -> list[Path]:
    """Find all .tsv files in input directory using natural sort."""
    
def detect_encoding(file_path: Path) -> str:
    """Detect file encoding using chardet, fallback to UTF-8."""
    
def extract_last_column(tsv_path: Path, encoding: str) -> list[str]:
    """Extract last column from TSV file, skip header and empty rows."""
    
def write_output(values: list[str], output_path: Path) -> None:
    """Write extracted values to text file, one per line."""
    
def process_file(tsv_path: Path, output_dir: Path) -> bool:
    """Process single TSV file, return success status."""
    
def main() -> None:
    """Main entry point for batch TSV processing."""

# Entry point (5 lines)
if __name__ == "__main__":
    main()
```

### 05.3 Data Flow

```plaintext
INPUT: USER-FILES/04.INPUT/*.tsv
  ↓
[Discover files with natsorted]
  ↓
[Create timestamp directory]
  ↓
FOR EACH FILE:
  ↓
  [Detect encoding]
  ↓
  [Open with csv.reader(delimiter='\t')]
  ↓
  [Skip first row]
  ↓
  [Extract row[-1] for each remaining row, skip empty]
  ↓
  [Write to {timestamp}/{filename}/{filename}.txt]
  ↓
OUTPUT: USER-FILES/05.OUTPUT/{YYMMDD_HHMMSS}/{filename}/{filename}.txt
```

### 05.4 Edge Cases

| Edge Case | Handling |
|-----------|----------|
| Empty input folder | Fail immediately with clear error |
| TSV with only header | Create empty output file |
| TSV with single column | Extract that single column |
| Inconsistent column counts | Extract last available column per row |
| Empty rows | Skip silently |
| Non-UTF-8 encoding | Detect with chardet, use detected encoding |
| Non-tab delimiter | Fail with clear error |
| File read permission error | Log error, skip file, continue |
| Output directory already exists | Create new timestamped folder (no conflicts) |

### 05.5 Performance Considerations

- **Sequential Processing**: Simple, deterministic, sufficient for typical batch sizes (<100 files)
- **Memory Usage**: Read entire file into memory (acceptable for typical TSV sizes <10MB)
- **Encoding Detection**: Only on failure, UTF-8 tried first
- **No Progress Bars**: Tool runs quickly on typical inputs, overhead not justified

### 05.6 Validation Rules

**Pre-Processing Validation:**
- INPUT directory exists
- At least one .tsv file found

**Per-File Validation:**
- File is readable
- File uses tab delimiter
- File has at least one row (header can be empty)

**Post-Processing Validation:**
- Output file created successfully
- Output contains expected number of lines

---

## 06. Success Criteria

### 06.1 Functional Requirements

- ✅ Process all TSV files in `04.INPUT/` directory
- ✅ Remove first row (header) from each file
- ✅ Extract last column from remaining rows
- ✅ Skip empty rows without errors
- ✅ Create timestamped output directories
- ✅ Generate one `.txt` file per input `.tsv` file
- ✅ Output format: one value per line
- ✅ Preserve original data exactly (no transformations)
- ✅ Continue processing on individual file failures
- ✅ Log clear errors to console

### 06.2 Non-Functional Requirements

- ✅ Single Python file under 250 lines
- ✅ Standard library only (plus loguru, chardet, natsort)
- ✅ Type hints on all functions
- ✅ Clear docstrings for LLM readability
- ✅ Sequential processing (deterministic)
- ✅ No configuration files
- ✅ No progress bars (tool runs quickly)
- ✅ Console logging only
- ✅ Fail fast on encoding/delimiter issues
- ✅ Virtual environment isolation

### 06.3 User Experience Requirements

- ✅ Run with single command: `python3 run.py`
- ✅ Show which file is currently being processed
- ✅ Display success/failure status per file
- ✅ Report total files processed at completion
- ✅ Clear, actionable error messages
- ✅ No manual intervention required during processing

### 06.4 Acceptance Criteria

**Given** a TSV file with 3 columns and 5 rows (1 header + 4 data)
**When** the script runs
**Then** output contains 4 lines (last column values only)

**Given** an empty `04.INPUT/` directory
**When** the script runs
**Then** script fails with error: "No TSV files found in USER-FILES/04.INPUT/"

**Given** a corrupted TSV file in `04.INPUT/`
**When** the script runs
**Then** script logs error for that file and continues with remaining files

**Given** multiple TSV files in `04.INPUT/`
**When** the script runs
**Then** each file gets its own subfolder in timestamped output directory

**Given** a TSV file with UTF-16 encoding
**When** the script runs
**Then** encoding is detected and file is processed correctly

---

## 07. Implementation Checklist

### 07.1 Setup Phase

- [ ] Create project structure
- [ ] Initialize virtual environment
- [ ] Create `requirements.txt` with pinned versions
- [ ] Create `.gitignore` for USER-FILES data exclusion
- [ ] Create USER-FILES directory structure with .gitkeep files
- [ ] Create `run.py` wrapper script

### 07.2 Development Phase

- [ ] Implement `setup_logging()` function
- [ ] Implement `get_timestamp()` function
- [ ] Implement `discover_tsv_files()` with natsort
- [ ] Implement `detect_encoding()` with chardet
- [ ] Implement `extract_last_column()` with csv.reader
- [ ] Implement `write_output()` function
- [ ] Implement `process_file()` with error handling
- [ ] Implement `main()` orchestration function
- [ ] Add type hints to all functions
- [ ] Add docstrings to all functions
- [ ] Add inline comments for complex logic

### 07.3 Testing Phase (Manual)

- [ ] Test with single TSV file
- [ ] Test with multiple TSV files
- [ ] Test with empty input directory
- [ ] Test with TSV containing only header
- [ ] Test with TSV with single column
- [ ] Test with TSV with inconsistent column counts
- [ ] Test with TSV with empty rows
- [ ] Test with non-UTF-8 encoded file
- [ ] Test with corrupted TSV file
- [ ] Test with non-tab-delimited file
- [ ] Verify output directory naming (timestamp only)
- [ ] Verify output file naming (removed .tsv extension)
- [ ] Verify output format (one value per line)
- [ ] Verify console logging messages
- [ ] Verify error handling (skip and continue)

### 07.4 Documentation Phase

- [ ] Verify all functions have docstrings
- [ ] Verify complex logic has inline comments
- [ ] Verify README is NOT created (personal tool)
- [ ] Store this PRD in `USER-FILES/00.KB/prd.md`

### 07.5 Deployment Phase

- [ ] Run script manually to verify functionality
- [ ] Commit code to repository (exclude USER-FILES data)
- [ ] Verify .gitignore excludes input/output data
- [ ] Verify directory structure preserved with .gitkeep files

---

## 08. Future Considerations

### 08.1 Not Included (By Design)

These features are explicitly **NOT** included to maintain minimalism:

- ❌ Configuration files or profiles
- ❌ Matrix processing (multiple profiles per input)
- ❌ Progress bars
- ❌ Summary reports or analytics
- ❌ Automated tests
- ❌ CSV support (TSV only)
- ❌ Multi-column extraction
- ❌ Row filtering
- ❌ Data transformations
- ❌ Custom delimiter support
- ❌ Header preservation options
- ❌ Column selection by name or index
- ❌ Log files (console only)
- ❌ Retry logic
- ❌ Parallel processing

### 08.2 Potential Extensions (If Needed Later)

If requirements change, consider these extensions:

1. **CSV Support**: Add delimiter detection to support CSV files
2. **Column Selection**: Allow specifying column index or name via command-line argument
3. **Profile System**: Add YAML profiles for different extraction modes
4. **Progress Bars**: Add alive-progress for large batch operations
5. **Log Files**: Generate per-file log files in output folders

**Note**: Any extensions should maintain the minimalist philosophy and single-purpose design. Clone and specialize rather than generalize.

---

## 09. Constraints and Assumptions

### 09.1 Constraints

- Single Python file under 250 lines (soft limit)
- Standard library preferred (external deps: loguru, chardet, natsort only)
- No automated testing (manual testing only)
- No configuration system
- No progress bars (runs quickly on typical inputs)
- Console logging only (no log files)
- Sequential processing only (no parallelism)
- Personal tool (single user, LLM-operated)

### 09.2 Assumptions

- Input TSV files use tab (`\t`) delimiter
- Input files are reasonably sized (<10MB typical)
- First row is always a header (removed unconditionally)
- Last column is the desired data
- Empty rows should be skipped
- Original data should not be modified
- Batch sizes are small (<100 files typical)
- User manually manages file organization (no auto-archiving)
- Encoding is typically UTF-8 (detect others as fallback)

### 09.3 Dependencies Rationale

| Dependency | Purpose | Justification |
|------------|---------|---------------|
| `csv` | TSV parsing | Standard library, built-in, reliable |
| `pathlib` | File operations | Standard library, modern, clean API |
| `sys` | Exit codes | Standard library, basic functionality |
| `datetime` | Timestamps | Standard library, simple time handling |
| `loguru` | Console logging | Simple, clean logging API (minimal external dependency) |
| `chardet` | Encoding detection | Handles non-UTF-8 files gracefully |
| `natsort` | Natural file sorting | Deterministic file ordering (e.g., file1, file2, file10) |

---

## 10. Project Timeline

### 10.1 Estimated Implementation Time

- **Setup**: 10 minutes (project structure, venv, dependencies)
- **Core Development**: 30-45 minutes (single file implementation)
- **Manual Testing**: 15-20 minutes (test various scenarios)
- **Documentation**: 5 minutes (docstrings, inline comments)

**Total**: ~60-80 minutes for complete implementation

### 10.2 Milestones

1. **Setup Complete**: Project structure, venv, dependencies installed
2. **Core Logic Complete**: File discovery, extraction, output writing
3. **Error Handling Complete**: Validation, skip-on-error, console logging
4. **Testing Complete**: Manual verification of all test scenarios
5. **Production Ready**: Committed to repository, ready for use

---

## 11. Appendix

### 11.1 Example Input/Output

**Input: `USER-FILES/04.INPUT/data.tsv`**
```tsv
ID	Name	Description	Prompt
1	Task A	First task	Write a function to parse JSON
2	Task B	Second task	Create a REST API endpoint
3	Task C	Third task	Implement error handling
```

**Output: `USER-FILES/05.OUTPUT/250103_143022/data/data.txt`**
```txt
Write a function to parse JSON
Create a REST API endpoint
Implement error handling
```

### 11.2 Example Console Output

```
[INFO] Processing: data.tsv
[SUCCESS] ✓ Extracted data.txt (3 rows)
[INFO] Processing: prompts.tsv
[SUCCESS] ✓ Extracted prompts.txt (5 rows)
[INFO] Processing: corrupted.tsv
[ERROR] ✗ Failed corrupted.tsv: Invalid tab-delimited format
[INFO] Completed: 2/3 files processed successfully
```

### 11.3 File Size Estimate

- `src/main.py`: ~180 lines (well under 250-line soft limit)
- `run.py`: ~15 lines
- `requirements.txt`: ~3 lines
- `.gitignore`: ~30 lines

**Total**: ~230 lines (excluding PRD and manifesto files)

### 11.4 Command Reference

**Setup:**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**Run:**
```bash
python3 run.py
```

**Or manually:**
```bash
source venv/bin/activate
python3 -m src.main
```

---

**End of PRD**
