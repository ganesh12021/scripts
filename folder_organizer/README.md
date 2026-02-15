# Folder Organizer

A lightweight Python script to organize files in a directory based on customizable rules. Files are sorted by type and optional naming patterns into organized folders, with automatic cleanup of empty directories.

## Features

- 🎯 **Pattern-based organization** – Match files by extension (glob patterns)
- 📝 **Name-based matching** – Match files by filename patterns (contains, startswith, endswith, regex)
- 📂 **Subfolder organization** – Apply specific rules to organize files within folders
- 🗑️ **Auto cleanup** – Remove empty directories after organization
- 🔄 **Recursive mode** – Optionally process subdirectories
- 🚫 **Case-insensitive** – `.PNG` and `.png` are treated the same
- ⚡ **Zero dependencies** – Uses only Python standard library

## Installation

No installation needed. Just download `folder_cleaner.py` and run it.

```bash
python3 folder_cleaner.py --help
```

## Usage

### Basic Usage

Organize files in a directory using default rules:

```bash
python3 folder_cleaner.py ~/Downloads
```

### Recursive Mode

Process all subdirectories:

```bash
python3 folder_cleaner.py ~/Downloads --recursive
python3 folder_cleaner.py ~/Downloads -r
```

## Configuration

Edit the `rules` array in `folder_cleaner.py` to customize file organization:

```python
rules = [
    (['*.txt', '*.md', '*.doc', '*.docx'], './documents'),
    (['*.jpg', '*.png', '*.gif', '*.jpeg', '*.heic'], './images'),
    (['*.mp3', '*.wav', '*.flac', '*.aac'], './audio'),
    (['*.mp4', '*.mkv', '*.avi', '*.mov'], './videos'),
    # Add more rules as needed...
]
```

**Format:** Each rule is a tuple of `(patterns, destination)`
- `patterns`: List of file patterns (glob-style, case-insensitive)
- `destination`: Where matching files will be moved (relative or absolute path)

## Advanced: Subfolder Organization

Define fine-tuned rules for specific folders using `subfolder_rulesets`:

```python
subfolder_rulesets = {
    'images': [
        (['*screenshot*', '*screen_shot*'], './screenshots'),
        (['IMG_*', 'IMG-*.jpg'], './camera'),
    ],
}
```

Then organize the subfolder:

```python
organize_subfolder(source, 'images', subfolder_rulesets['images'])
```

**Example workflow:**
1. Run `folder_cleaner.py ~/Downloads` to organize top-level files
2. Then call `organize_subfolder()` to further organize inside the `images` folder

## Pattern Matching

### Glob Patterns (Default)

Standard wildcard patterns, case-insensitive:

```python
'*.jpg'      # All JPG files
'*screenshot*'  # Files containing 'screenshot' in the name
'IMG_*'      # Files starting with 'IMG_'
```

## How It Works

1. **Scan** – Collects all files in the target directory
2. **Match** – Checks each file against rules (first match wins)
3. **Move** – Moves matching files to their destination folder
4. **Deduplicate** – If a file already exists in the destination, appends a counter
5. **Cleanup** – Removes empty directories (preserves root)
6. **Report** – Prints summary of moved and skipped files

## Example Output

```
📁 Processing 42 files

✓ Moved: photo.jpg
✓ Moved: document.pdf
✓ Moved: song.mp3
...

✅ Summary: 38 moved, 4 skipped

🧹 Cleaned up 2 empty folder(s)
```

## Default Rules

Files are organized into these folders:

| Folder | File Types |
|--------|-----------|
| `documents` | `.txt`, `.md`, `.doc`, `.docx` |
| `images` | `.jpg`, `.png`, `.gif`, `.jpeg`, `.heic` |
| `audio` | `.mp3`, `.wav`, `.flac`, `.aac` |
| `videos` | `.mp4`, `.mkv`, `.avi`, `.mov` |
| `archives` | `.zip`, `.rar`, `.7z` |
| `pdfs` | `.pdf` |
| `code` | `.py`, `.js`, `.html`, `.css` |
| `spreadsheets` | `.csv`, `.xlsx`, `.xls` |
| And many more... | |

Files that don't match any rule are left untouched.

## Tips & Tricks

### Rename Files Safely

The script handles duplicate filenames automatically:
- `photo.jpg` and `photo.jpg` → `photo.jpg` and `photo_1.jpg`

### Absolute Paths

Use absolute paths for precise control:

```python
rules = [
    (['*.mp4'], '/mnt/storage/videos'),
]
```

### Dry Run

Inspect rules first without moving files – comment out `move_file()` call or just review the code logic.

## Troubleshooting

**Q: Files are not moving**
- Check that the patterns match your filenames (case-insensitive)
- Verify the destination folder is accessible and writable
- Run with a test file to debug

**Q: Permission denied errors**
- Ensure you have write access to both source and destination directories

**Q: Want to undo changes?**
- Use your system's file browser or `mv` command to restore files
- Consider using a test directory first

## License

Free to use and modify.

## Contributing

Feel free to extend this script for your use cases – it's designed to be simple and hackable!
