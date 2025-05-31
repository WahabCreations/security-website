import base64

import os
# Correct path to logo (relative to where script is run)
logo_path = os.path.join(os.path.dirname(__file__), "templates/email/logo.png")

# Read and encode the image
try:
    with open(logo_path, "rb") as image_file:
        base64_string = base64.b64encode(image_file.read()).decode("utf-8")
    print(f"data:image/png;base64,{base64_string}")
except FileNotFoundError:
    print(f"Error: Could not find file at {logo_path}")
    print("Current working directory:", os.getcwd())