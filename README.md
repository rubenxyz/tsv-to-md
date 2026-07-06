# TSV to Markdown Converter

Extracts the last column (image prompt) from each TSV row and saves each prompt as a separate `.md` file.

## Usage

```bash
python3 run.py
```

## How it works

1. Scans `USER-FILES/04.INPUT/` for all `.tsv` files
2. Skips the header row
3. Extracts the last column from every data row
4. Saves each value as `[filename]_[index].md` in `USER-FILES/05.OUTPUT/`

## Output

```
USER-FILES/05.OUTPUT/
└── YYMMDD_HHMMSS_PROMPTS/
    ├── input_file/
    │   ├── input_file_1.md
    │   ├── input_file_2.md
    │   └── ...
    └── ...
```

Index starts at 1 (header row is not counted).
