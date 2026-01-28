"""
Update Documentation Script

AI-assisted documentation updates for strategy and analysis docs.
"""

import os
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
ROOT_DIR = SCRIPT_DIR.parent

try:
    from dotenv import load_dotenv
    from openai import OpenAI
except ImportError:
    print("⚠️  Missing dependencies (openai, python-dotenv).")
    print("   Please run: pip install openai python-dotenv")
    sys.exit(1)

load_dotenv(ROOT_DIR / ".env")


def get_recent_changes():
    """Get recent git changes for context."""
    result = subprocess.run(
        ["git", "log", "-5", "--oneline"],
        capture_output=True, text=True, encoding='utf-8', errors='replace', cwd=ROOT_DIR
    )
    return result.stdout or ""


def update_strategy_docs(client):
    """Update strategy documentation based on recent changes."""
    print("📚 Reviewing strategy documentation...")
    
    # Read current strategy analysis
    strategy_file = ROOT_DIR / "STRATEGY_ANALYSIS.md"
    if not strategy_file.exists():
        print("ℹ️  STRATEGY_ANALYSIS.md not found.")
        return False
    
    current_content = strategy_file.read_text(encoding="utf-8")
    recent_changes = get_recent_changes()
    
    system_prompt = """
    You are a senior data scientist reviewing strategy documentation.
    Your task is to identify if the strategy document needs updates based on recent changes.
    
    If updates are needed, provide specific suggestions in markdown format.
    If no updates are needed, respond with "NO_UPDATES_NEEDED".
    
    Focus on:
    - Data analysis methodology
    - Model selection rationale
    - Evaluation metrics
    - Technical trade-offs
    """
    
    try:
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Recent Changes:\n{recent_changes}\n\nCurrent Strategy Doc:\n{current_content[:10000]}"}
            ],
            temperature=0.3,
            max_tokens=500
        )
        
        suggestions = response.choices[0].message.content.strip()
        
        if "NO_UPDATES_NEEDED" in suggestions:
            print("✅ Strategy documentation is up to date.")
        else:
            print("💡 Suggestions for documentation updates:")
            print(suggestions)
            
        return True
    except Exception as e:
        print(f"⚠️  Failed to review documentation: {e}")
        return False


def main():
    api_key = os.getenv("DEEPSEEK_API_KEY") or os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("⚠️  API Key not found. Cannot update documentation.")
        sys.exit(1)
    
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    
    update_strategy_docs(client)
    print("✅ Documentation review complete.")


if __name__ == "__main__":
    main()
