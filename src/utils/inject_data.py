import csv
import json
import os

def inject_data(csv_path, html_template_path, output_path):
    """
    Reads a CSV file, converts it to JSON, and injects it into an HTML template
    as a global window.RISK_DATA variable. Also injects global_drivers.json.
    """
    print(f"Reading data from {csv_path}...")
    
    # 1. Read the Real Data
    rows = []
    try:
        with open(csv_path, 'r', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                rows.append(row)
    except FileNotFoundError:
        print(f"Error: CSV file not found at {csv_path}")
        return

    # 2. Serialize to JSON
    json_payload = json.dumps(rows)

    # 2b. Read Global Drivers
    drivers_path = os.path.join(os.path.dirname(csv_path), 'global_drivers.json')
    drivers_json = "[]"
    if os.path.exists(drivers_path):
        with open(drivers_path, 'r') as f:
            drivers_json = f.read()
    else:
        print(f"Warning: Drivers file not found at {drivers_path}")

    # 3. Prepare the Injection String
    injection_code = f"""
    <script>
        window.RISK_DATA = {json_payload};
        window.GLOBAL_DRIVERS = {drivers_json};
        console.log("Build-Time Injection Complete. Rows loaded:", window.RISK_DATA.length);
    </script>
    """

    # 4. Inject into HTML
    print(f"Reading template from {html_template_path}...")
    try:
        with open(html_template_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except FileNotFoundError:
        print(f"Error: HTML template not found at {html_template_path}")
        return
    
    # Inject before closing body tag
    if "</body>" in html_content:
        final_html = html_content.replace("</body>", injection_code + "\n</body>")
    else:
        # Fallback if no body tag found (unlikely for valid HTML)
        final_html = html_content + injection_code

    # 5. Write Artifact
    print(f"Writing final report to {output_path}...")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(final_html)
    
    print(f"✅ Successfully generated portable report at {output_path}")

if __name__ == "__main__":
    # Adjust paths relative to the project root if run from there, 
    # or handle relative imports. Assuming run from project root.
    CSV_PATH = "results/risk_watch_list.csv"
    TEMPLATE_PATH = "slides.html"
    OUTPUT_PATH = "results/slides_final.html"
    
    inject_data(CSV_PATH, TEMPLATE_PATH, OUTPUT_PATH)
