"""
AutoCommit Script

AI-powered git commit message generation and development log updates.
Adapted from ForgeLaunchSpring2026Jan30 for Data Science workflows.
"""

import os
import subprocess
import sys
import datetime
import re
import json
from pathlib import Path

# Setup paths
SCRIPT_DIR = Path(__file__).parent
ROOT_DIR = SCRIPT_DIR.parent
DEVLOG_FILE = ROOT_DIR / "docs" / "development_log.md"
TEST_SUMMARY_FILE = ROOT_DIR / "docs" / "test_summary.json"

try:
    from dotenv import load_dotenv
    from openai import OpenAI
except ImportError:
    print("⚠️  Missing dependencies (openai, python-dotenv).")
    print("   Please run: pip install openai python-dotenv")
    sys.exit(1)

load_dotenv(ROOT_DIR / ".env")


def get_staged_diff():
    """Get the diff of currently staged files."""
    result = subprocess.run(
        ["git", "diff", "--cached"], 
        capture_output=True, text=True, encoding='utf-8', errors='replace', cwd=ROOT_DIR
    )
    return result.stdout or ""


def get_staged_files():
    """Get the list of staged files."""
    result = subprocess.run(
        ["git", "diff", "--name-only", "--cached"], 
        capture_output=True, text=True, encoding='utf-8', errors='replace', cwd=ROOT_DIR
    )
    return result.stdout or ""


def generate_devlog_entry(client, diff, files):
    """Generates a high-level progress update for the dev log."""
    print("📔 Updating Dev Log...")
    today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    
    system_prompt = """
    You are a Principal Data Scientist writing a technical development log.
    
    Your goal is not just to list changes, but to explain the *data science story* behind them.
    
    For every major change (model updates, data processing, analysis improvements), use the following structure:
    
    1. **Context/Problem**: Briefly explain the limitation, bug, or missing requirement that triggered this work.
    2. **Solution/Implementation**: Describe the technical approach taken. Be specific (e.g., "Added feature engineering step", "Implemented cross-validation").
    3. **Rationale/Logic**: Explain *why* this solution was chosen. Discuss trade-offs, model performance, or data quality implications.
    4. **Outcome**: Mention how it was verified (tests passed, metrics improved) and the impact.
    
    **Formatting Rules:**
    - Use `## [Timestamp] Title of Change` for the header.
    - Use **bold** for key technical terms.
    - Keep it concise but dense with technical value.
    - For minor trivial fixes (typos, formatting), a simple bullet point is sufficient.
    """
    
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Current Timestamp: {today}\nFiles Changed:\n{files}\n\nTechnical Diff:\n{diff[:15000]}"} 
            ],
            temperature=0.3,
            max_tokens=500
        )
        log_content = response.choices[0].message.content.strip()
        
        # Append to development_log.md
        entry = f"\n\n{log_content}"
        
        with open(DEVLOG_FILE, "a", encoding="utf-8") as f:
            f.write(entry)
            
        print(f"✅ Appended new entry to {DEVLOG_FILE.name}")
        return True
    except Exception as e:
        print(f"⚠️  Failed to update Dev Log: {e}")
        return False


def generate_commit_message(client, diff, files):
    """Generates the conventional commit message."""
    print("🤖 Generating commit message...")
    
    system_prompt = (
        "You are a senior data scientist. Generate a detailed commit message complying with Conventional Commits."
        "\nStructure:"
        "\n<type>: <short summary>"
        "\n\n- <bullet point 1>"
        "\n- <bullet point 2>"
        "\n\nRules:"
        "\n1. First line must be under 72 chars."
        "\n2. Group changes logically."
        "\n3. Do not use markdown formatting (no bold/italics)."
        "\n4. Use types: feat, fix, docs, refactor, test, data, model, analysis"
    )
    
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Staged Files:\n{files}\n\nDiff Content:\n{diff[:20000]}"}
            ],
            temperature=0.4,
            max_tokens=250
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"⚠️  Generation failed: {e}")
        return "wip: update (generation failed)"


def update_qa_report(log_output, success):
    """Updates the QA_REPORT.md file with the new verification log."""
    qa_file = ROOT_DIR / "docs" / "qa_report.md"
    if not qa_file.exists():
        print("ℹ️  QA Report not found, skipping update.")
        return False

    try:
        content = qa_file.read_text(encoding="utf-8")
        today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Update Date
        content = re.sub(r"(\*\*Date:\*\* ).*", f"\\g<1>{today}", content)

        # Update Log Content
        log_pattern = r"(```text\n)(.*?)(```)"
        
        if not re.search(log_pattern, content, re.DOTALL):
            print("⚠️  Could not find '```text' block in QA Report.")
            return False

        # Clean ANSI codes from log before injecting
        clean_log = re.sub(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])', '', log_output)
        # Escape backslashes to prevent regex errors during substitution
        clean_log = clean_log.replace('\\', '\\\\')
        
        # Inject new log
        new_log_block = f"```text\n{clean_log.strip()}\n```"
        content = re.sub(log_pattern, new_log_block, content, flags=re.DOTALL)

        # Update Conclusion Signature
        status_pattern = r"(\*Signed: Automated Verification Suite.*)"
        status_emoji = '✅ PASS' if success else '❌ FAIL'
        status_line = f"*Signed: Automated Verification Suite (Result: {status_emoji})*"
        
        if re.search(status_pattern, content):
            content = re.sub(status_pattern, status_line, content)
        else:
            content += f"\n\n{status_line}"

        qa_file.write_text(content, encoding="utf-8")
        print(f"✅ Updated {qa_file.name} with latest logs (Result: {status_emoji}).")
        return True

    except Exception as e:
        print(f"⚠️  Failed to update QA Report: {e}")
        return False


def run_verification():
    """Runs the test suite and returns (output, success) tuple."""
    print("🔍 Running test suite...")
    venv_python = ROOT_DIR / "venv" / "Scripts" / "python.exe"
    python_cmd = str(venv_python) if venv_python.exists() else sys.executable

    try:
        result = subprocess.run(
            [python_cmd, "-m", "pytest", "test/", "-v", "--tb=short"], 
            cwd=ROOT_DIR, 
            capture_output=True,
            text=True,
            encoding='utf-8'
        )
        
        output = result.stdout
        if result.stderr:
            output += f"\n\nSTDERR:\n{result.stderr}"
        
        success = (result.returncode == 0)
        
        if success:
            print("✅ Tests Passed.")
        else:
            print("❌ Tests FAILED.")
            
        return output, success
        
    except Exception as e:
        return f"CRITICAL ERROR: {str(e)}", False


def main():
    api_key = os.getenv("DEEPSEEK_API_KEY") or os.getenv("OPENAI_API_KEY")
    
    # Run Verification
    verification_output, is_passing = run_verification()
    
    # Update report REGARDLESS of pass/fail
    if verification_output:
        updated = update_qa_report(verification_output, is_passing)
        if updated:
            qa_file = ROOT_DIR / "docs" / "qa_report.md"
            subprocess.run(["git", "add", str(qa_file)], cwd=ROOT_DIR)
            if TEST_SUMMARY_FILE.exists():
                subprocess.run(["git", "add", str(TEST_SUMMARY_FILE)], cwd=ROOT_DIR)

    # Halt if verification failed
    if not is_passing:
        print("\n❌ Verification FAILED. Report updated. Commit aborted.")
        sys.exit(1)

    # Stage initial changes
    print("📦 Staging changes...")
    subprocess.run(["git", "add", "."], cwd=ROOT_DIR)
    
    diff = get_staged_diff()
    files = get_staged_files()
    
    if not diff.strip():
        print("No changes to commit.")
        sys.exit(0)

    # Initialize Client
    if not api_key:
        print("⚠️  API Key not found. Skipping AI generation.")
        commit_msg = "wip: quick push"
    else:
        client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

        # Generate Dev Log entry
        generate_devlog_entry(client, diff, files)

        # Stage the Dev Log update
        subprocess.run(["git", "add", str(DEVLOG_FILE)], cwd=ROOT_DIR)
        
        # Refresh diff/files
        diff = get_staged_diff() 
        files = get_staged_files()

        # Generate Commit Message
        commit_msg = generate_commit_message(client, diff, files)

    # Execute Git Operations
    branch = subprocess.run(
        ["git", "branch", "--show-current"], 
        capture_output=True, text=True, cwd=ROOT_DIR
    ).stdout.strip()
    
    print("---------------------------------------------------")
    print(f"🚀 Branch: {branch}")
    print(f"📝 Message:\n{commit_msg}")
    print("---------------------------------------------------")
    
    try:
        subprocess.run(["git", "commit", "-m", commit_msg], cwd=ROOT_DIR, check=True)
        subprocess.run(["git", "push"], cwd=ROOT_DIR, check=True)
        print("✅ Pushed!")
    except subprocess.CalledProcessError:
        print("❌ Failed to commit/push.")
        sys.exit(1)


if __name__ == "__main__":
    main()
