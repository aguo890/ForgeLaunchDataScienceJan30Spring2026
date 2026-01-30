"""
Submission Packaging Script
Forge Launch Data Science Challenge - January 2026

Creates a clean, professional zip file for submission.
Excludes: __pycache__, .git, venv, .env, and other junk files.
"""

import zipfile
import os
from pathlib import Path
from datetime import datetime

# Configuration
PROJECT_ROOT = Path(__file__).parent
OUTPUT_NAME = f"ForgeLaunch_DataScience_Submission_{datetime.now().strftime('%Y%m%d')}.zip"
OUTPUT_PATH = PROJECT_ROOT / OUTPUT_NAME

# Files/folders to EXCLUDE
EXCLUDES = {
    '__pycache__',
    '.git',
    '.gitignore',
    'venv',
    '.env',
    '.pytest_cache',
    '.mypy_cache',
    '.vscode',
    '.idea',
    '*.pyc',
    '*.pyo',
    '*.egg-info',
    'package_submission.py',  # Don't include this script itself
}

# Files/folders to explicitly INCLUDE (in order of importance)
# Tuples specify (source_path, arcname) for files that need flattening in the zip
INCLUDES = [
    'README.md',
    'main.py',
    'requirements.txt',
    ('templates/slides.html', 'slides.html'),  # Flatten: place at zip root
    'src/',
    'notebooks/',
    'data/',
    'results/',
    'test/',
    'docs/',
]

def should_exclude(path: Path) -> bool:
    """Check if a path should be excluded."""
    for part in path.parts:
        if part in EXCLUDES:
            return True
        for pattern in EXCLUDES:
            if pattern.startswith('*') and part.endswith(pattern[1:]):
                return True
    return False

def create_submission_zip():
    """Create the submission zip file."""
    print(f"📦 Creating submission package: {OUTPUT_NAME}")
    print("-" * 50)
    
    files_added = 0
    
    with zipfile.ZipFile(OUTPUT_PATH, 'w', zipfile.ZIP_DEFLATED) as zf:
        for include in INCLUDES:
            # Handle tuple entries: (source_path, arcname) for flattening
            if isinstance(include, tuple):
                source_path, arcname = include
                include_path = PROJECT_ROOT / source_path
                
                if not include_path.exists():
                    print(f"⚠️  Skipping (not found): {source_path}")
                    continue
                
                zf.write(include_path, arcname)
                print(f"✅ Added: {source_path} → {arcname}")
                files_added += 1
                continue
            
            # Handle string entries (original behavior)
            include_path = PROJECT_ROOT / include
            
            if not include_path.exists():
                print(f"⚠️  Skipping (not found): {include}")
                continue
            
            if include_path.is_file():
                # Add single file
                zf.write(include_path, include)
                print(f"✅ Added: {include}")
                files_added += 1
            else:
                # Add directory recursively
                for file_path in include_path.rglob('*'):
                    if file_path.is_file() and not should_exclude(file_path):
                        arcname = file_path.relative_to(PROJECT_ROOT)
                        zf.write(file_path, arcname)
                        files_added += 1
                print(f"✅ Added: {include} (directory)")
    
    print("-" * 50)
    print(f"🎉 SUCCESS! Created: {OUTPUT_PATH}")
    print(f"   Total files: {files_added}")
    print(f"   Size: {OUTPUT_PATH.stat().st_size / 1024:.1f} KB")
    print()
    print("📋 Submission Checklist:")
    print("   [ ] Upload this zip to the Google Form")
    print("   [ ] Copy essays into the form text fields")
    print("   [ ] Double-check your contact email")

if __name__ == "__main__":
    create_submission_zip()
