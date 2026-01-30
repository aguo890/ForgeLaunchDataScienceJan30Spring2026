import os
import sys
import zipfile
import shutil
import subprocess
from pathlib import Path

def fail(msg):
    print(f"❌ FAILURE: {msg}")
    sys.exit(1)

def pass_msg(msg):
    print(f"✅ VERIFIED: {msg}")

def verify_submission():
    print("🔍 Starting 'Clean Room' Verification...")
    
    # 1. Find the submission zip
    cwd = Path.cwd()
    zips = list(cwd.glob("ForgeLaunch_DataScience_Submission_*.zip"))
    
    if not zips:
        fail("No submission zip found!")
        
    # Sort by modification time, newest first
    submission_zip = sorted(zips, key=lambda p: p.stat().st_mtime, reverse=True)[0]
    print(f"📦 Found submission artifact: {submission_zip.name}")
    
    # 2. Create temp Clean Room
    temp_dir = cwd / "temp_verification_room"
    if temp_dir.exists():
        shutil.rmtree(temp_dir)
    temp_dir.mkdir()
    
    try:
        # 3. Extract
        print("📂 Unzipping to temporary clean room...")
        with zipfile.ZipFile(submission_zip, 'r') as zf:
            zf.extractall(temp_dir)
            
        print(f"   Extracted to: {temp_dir}")
        
        # 4. Verify Structure
        required_files = [
            'slides.html',
            'requirements.txt',
            'main.py',
            'README.md',
            'data/raw/WA_Fn-UseC_-HR-Employee-Attrition.csv' # Check for data existence
        ]
        
        missing = []
        for f in required_files:
            if not (temp_dir / f).exists():
                missing.append(f)
        
        if missing:
            fail(f"Missing required files in artifact: {missing}")
        pass_msg("Directory structure and required files present.")

        # 5. Verify Execution
        print("🚀 Running main.py in clean environment...")
        
        # We use the current python executable but run it inside the clean room
        # We assume requirements are met by the current environment for this tests
        # or we could create a venv, but that takes time. User said "verification: environment (Optional)"
        # so we skip venv creation and just run with current python.
        
        result = subprocess.run(
            [sys.executable, "main.py"],
            cwd=temp_dir,
            capture_output=True,
            text=True
        )
        
        # Print output for debugging if needed
        # print(result.stdout)
        # print(result.stderr)
        
        if result.returncode != 0:
            print("--- STDOUT ---")
            print(result.stdout)
            print("--- STDERR ---")
            print(result.stderr)
            fail("main.py execution failed with non-zero exit code.")
            
        # 6. Verify Outputs
        # main.py should create results/risk_watch_list.csv and results/figures
        expected_outputs = [
            'results/risk_watch_list.csv',
            'results/global_drivers.json',
            'results/figures'
        ]
        
        missing_outputs = []
        for out in expected_outputs:
            if not (temp_dir / out).exists():
                missing_outputs.append(out)
                
        if missing_outputs:
            fail(f"Execution finished but output files missing: {missing_outputs}")
            
        pass_msg("main.py executed successfully and produced expected artifacts.")
        
        print("\n🎉 SUCCESS: Submission Artifact is VALID and ready to ship!")
        
    finally:
        # Cleanup
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
            print("🧹 Cleaned up verification room.")

if __name__ == "__main__":
    verify_submission()
