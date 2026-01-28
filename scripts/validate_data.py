"""
Data Validation Script

Performs data quality checks on raw and processed datasets.
"""

import os
import sys
from pathlib import Path
import json
from datetime import datetime

SCRIPT_DIR = Path(__file__).parent
ROOT_DIR = SCRIPT_DIR.parent
DATA_DIR = ROOT_DIR / "data"


def check_directory_structure():
    """Verify required directories exist."""
    print("📁 Checking directory structure...")
    
    required_dirs = [
        DATA_DIR / "raw",
        DATA_DIR / "processed",
        DATA_DIR / "external"
    ]
    
    missing = []
    for dir_path in required_dirs:
        if not dir_path.exists():
            missing.append(str(dir_path.relative_to(ROOT_DIR)))
    
    if missing:
        print(f"⚠️  Missing directories: {', '.join(missing)}")
        return False
    
    print("✅ All required directories exist.")
    return True


def list_data_files():
    """List all data files in the data directories."""
    print("\n📊 Data Files:")
    
    file_extensions = ['.csv', '.xlsx', '.parquet', '.json']
    file_count = 0
    
    for subdir in ['raw', 'processed', 'external']:
        dir_path = DATA_DIR / subdir
        if dir_path.exists():
            files = [f for f in dir_path.iterdir() 
                     if f.is_file() and f.suffix.lower() in file_extensions]
            if files:
                print(f"\n  {subdir}/")
                for f in files:
                    size_mb = f.stat().st_size / 1024 / 1024
                    print(f"    - {f.name} ({size_mb:.2f} MB)")
                    file_count += 1
    
    if file_count == 0:
        print("  (No data files found)")
    
    return file_count


def validate_csv_structure(filepath):
    """Perform basic validation on a CSV file."""
    try:
        import pandas as pd
        df = pd.read_csv(filepath, nrows=5)
        
        return {
            'valid': True,
            'columns': len(df.columns),
            'sample_columns': df.columns.tolist()[:5]
        }
    except Exception as e:
        return {
            'valid': False,
            'error': str(e)
        }


def run_validation():
    """Run all validation checks."""
    print("=" * 50)
    print("🔍 DATA VALIDATION REPORT")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    
    results = {
        'timestamp': datetime.now().isoformat(),
        'checks': {}
    }
    
    # Check 1: Directory structure
    results['checks']['directory_structure'] = check_directory_structure()
    
    # Check 2: List files
    file_count = list_data_files()
    results['checks']['files_found'] = file_count
    
    # Check 3: Validate CSVs in raw directory
    print("\n🔬 Validating CSV files...")
    raw_dir = DATA_DIR / "raw"
    csv_files = list(raw_dir.glob("*.csv")) if raw_dir.exists() else []
    
    if csv_files:
        for csv_file in csv_files:
            validation = validate_csv_structure(csv_file)
            print(f"  {csv_file.name}: {'✅ Valid' if validation['valid'] else '❌ Invalid'}")
            results['checks'][csv_file.name] = validation
    else:
        print("  (No CSV files to validate)")
    
    # Summary
    print("\n" + "=" * 50)
    print("📋 SUMMARY")
    print("=" * 50)
    
    all_passed = all(
        v if isinstance(v, bool) else v.get('valid', True) 
        for v in results['checks'].values()
    )
    
    if all_passed:
        print("✅ All validation checks passed!")
    else:
        print("⚠️  Some validation checks failed. Review the output above.")
    
    # Save results
    output_file = ROOT_DIR / "docs" / "validation_results.json"
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\n💾 Results saved to {output_file.relative_to(ROOT_DIR)}")
    
    return all_passed


if __name__ == "__main__":
    success = run_validation()
    sys.exit(0 if success else 1)
