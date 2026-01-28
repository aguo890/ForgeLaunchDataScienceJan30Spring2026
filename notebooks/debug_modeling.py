
import sys
import os
import pandas as pd
import traceback

print(f"CWD: {os.getcwd()}")

# Add src to path (assuming we are in notebooks/)
# If we are in root, this might need adjustment, but we will run it from root so we need to be careful.
# If I run `python notebooks/debug_modeling.py`, CWD is usually where I run it from (Root).
# But the notebook execution sets CWD to the notebook dir.
# So I should change CWD to notebooks/ to simulate.

if os.path.basename(os.getcwd()) != 'notebooks':
    try:
        os.chdir('notebooks')
        print(f"Changed CWD to: {os.getcwd()}")
    except Exception as e:
        print(f"Could not change to notebooks dir: {e}")

sys.path.append(os.path.abspath(os.path.join('..')))

try:
    from src.modeling import load_processed_data
    print("Import successful")
except ImportError as e:
    print(f"Import failed: {e}")
    sys.exit(1)

try:
    # Try to list the data dir relative to here
    data_dir_rel = '../data/processed'
    print(f"Checking absolute path of {data_dir_rel}: {os.path.abspath(data_dir_rel)}")
    
    if os.path.exists(data_dir_rel):
        print(f"Listing {data_dir_rel}: {os.listdir(data_dir_rel)}")
    else:
        print(f"{data_dir_rel} does not exist.")
        
    X_train, y_train, X_test, y_test = load_processed_data(data_dir_rel)
    print("Load successful")
    print(f"Train Shape: {X_train.shape}")
except Exception as e:
    print(f"Load failed: {e}")
    traceback.print_exc()
