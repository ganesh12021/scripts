#!/usr/bin/env python3
"""Folder Cleaner - Organize files based on rules."""

import os
import sys
import shutil
import fnmatch


def matches_pattern(filename, patterns):
    """Check if filename matches any pattern."""
    if isinstance(patterns, str):
        patterns = [patterns]
    # Perform case-insensitive matching by lowercasing both sides
    filename_l = filename.lower()
    for p in patterns:
        if fnmatch.fnmatch(filename_l, p.lower()):
            return True
    return False


def move_file(file_path, destination):
    """Move file to destination, handling duplicates."""
    try:
        filename = os.path.basename(file_path)
        dest_file = os.path.join(destination, filename)

        if os.path.exists(dest_file):
            base, ext = os.path.splitext(filename)
            counter = 1
            while os.path.exists(os.path.join(destination, f"{base}_{counter}{ext}")):
                counter += 1
            dest_file = os.path.join(destination, f"{base}_{counter}{ext}")

        shutil.move(file_path, dest_file)
        print(f"✓ Moved: {filename}")
        return True
    except (OSError, PermissionError) as e:
        print(f"✗ Failed to move {file_path}: {e}")
        return False


def organize_subfolder(root_dir, subfolder_name, subrules, recursive=False):
    """Run `organize()` on a named subfolder under `root_dir` using `subrules`.

    Example: organize_subfolder('/path/to/dir', 'images', subfolder_rulesets['images'])
    will run the provided subrules inside '/path/to/dir/images'.
    """
    subroot = os.path.join(root_dir, subfolder_name)
    if not os.path.isdir(subroot):
        print(f"Subfolder not found: {subroot}")
        return
    organize(subroot, subrules, recursive=recursive)


def organize(source_dir, rules, recursive=False):
    """Organize files based on rules."""
    if not os.path.isdir(source_dir):
        print(f"Error: '{source_dir}' is not a valid directory.")
        return

    files = []
    if recursive:
        for root, _, filenames in os.walk(source_dir):
            files.extend(os.path.join(root, f) for f in filenames)
    else:
        files = [
            os.path.join(source_dir, f)
            for f in os.listdir(source_dir)
            if os.path.isfile(os.path.join(source_dir, f))
        ]

    moved = skipped = 0
    print(f"\n📁 Processing {len(files)} files")

    for file_path in files:
        filename = os.path.basename(file_path)
        matched = False

        for patterns, dest in rules:
            if matches_pattern(filename, patterns):
                destination = dest if os.path.isabs(dest) else os.path.join(source_dir, dest)
                os.makedirs(destination, exist_ok=True)
                if move_file(file_path, destination):
                    moved += 1
                matched = True
                break

        if not matched:
            skipped += 1

    print(f"\n✅ Summary -> {source_dir}: {moved} moved, {skipped} skipped\n")


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python folder_cleaner.py <directory> [--recursive]")
        print("\nEdit rules in the script file to customize behavior.")
        sys.exit(1)

    source = sys.argv[1]
    recurse_subfolders = '--recursive' in sys.argv or '-r' in sys.argv

    # Define rules here: (patterns, destination)
    base_rules = [
        (['*.txt', '*.md', '*.doc', '*.docx'], './documents'),
        (['*.jpg', '*.png', '*.gif', '*.jpeg', '*.HEIC'], './images'),
        (['*.mp3', '*.wav', '*.flac', '*.aac'], './audio'),
        (['*.mp4', '*.mkv', '*.avi', '*.mov'], './videos'),
        (['*.zip', '*.rar', '*.7z'], './archives'),
        (['*.pdf'], './pdfs'),
        (['*.dmg', '*.exe', '*.msi', '*.pkg'], './installers'),
        (['*.py', '*.js', '*.html', '*.css'], './code'),
        (['*.csv', '*.xlsx', '*.xls'], './spreadsheets'),
        (['*.ppt', '*.pptx'], './presentations'),
        (['*.log'], './logs'),
        (['*.apk', '*.ipa'], './apps'),
        (['*.p12', '*.p8', '*.pfx'], './certificates')
    ]

    # Main organize call for top-level rules
    organize(source, base_rules, recursive=recurse_subfolders)

    # ===========================================================
    # Specific handling for image subfolder
    # ===========================================================
    image_rulesets = [
        (['*screenshot*', '*screen_shot*'], './screenshots'),
        (['IMG_*', 'IMG-*.jpg'], './camera'),
        (['WhatsApp Image*'], './whatsapp-images')
    ]
    organize_subfolder(source, 'images', image_rulesets, recursive=False)

    # ============================================================
    # Specific handling for videos subfolder
    # ============================================================
    video_rulesets = [
        (['*-Meeting Recording*'], './lectures'),
        (['Screen Recording*'], './screen-recordings'),
        (['WhatsApp Video*'], './whatsapp-videos'),
        (['Simulator Screen Recording*'], './simulator-recordings')
    ]
    organize_subfolder(source, 'videos', video_rulesets, recursive=False)

    # ============================================================
    # Specifc handling for apps subfolder
    # ============================================================
    app_rulesets = [
        (['*.apk'], './android'),
        (['*.ipa'], './ios')
    ]
    organize_subfolder(source, 'apps', app_rulesets, recursive=False)

    # ============================================================
    # Specifc handling for pdf subfolder
    # ============================================================
    pdf_rulesets = [
        (['invoice-*'], './invoices'),
        (['Payslip*'], './payslips'),
        (['Tax Report*'], './tax-reports')
    ]
    organize_subfolder(source, 'pdfs', pdf_rulesets, recursive=False)
