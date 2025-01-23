import requests
import hashlib
import base64
import os

# Determine the script directory
script_dir = os.path.dirname(os.path.abspath(__file__))
# Server details
MANIFEST_URL = "https://raw.githubusercontent.com/rahuljshimpi/FOTA/main/manifest.json"
#SCRIPT_PATH = "/home/pi/Desktop/FOTA/Code_1.py"  # Replace with the path to your script
SCRIPT_PATH = os.path.join(script_dir, "Code_1.py")
UPDATE_PATH = "/tmp/update.bin"
CURRENT_VERSION = "1.0.0"  # Initial version of the script

#def check_for_updates():
def check_for_updates():
    print("Checking for updates...")
    response = requests.get(MANIFEST_URL)
    try:
        manifest = response.json()
    except requests.exceptions.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        print(f"Response text: {response.text}")
        return None, None, None

    if manifest.get("version") > CURRENT_VERSION:
        print(f"New version {manifest['version']} available!")
        return manifest["url"], manifest["hash"], manifest["version"]

    print("No updates available.")
    return None, None, None


def download_update(url):
    print(f"Downloading update from {url}...")
    response = requests.get(url, stream=True)
    with open(UPDATE_PATH, "wb") as update_file:
        for chunk in response.iter_content(chunk_size=1024):
            update_file.write(chunk)
    print("Download completed.")

def validate_update(file_path, expected_hash):
    print("Validating update...")
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(1024):
            sha256.update(chunk)
    calculated_hash = sha256.hexdigest()
    if calculated_hash == expected_hash:
        print("Validation successful!")
        return True
    print("Validation failed!")
    return False

def apply_update():
    print("Applying update...")
    with open(UPDATE_PATH, "rb") as f:
        decoded_data = base64.b64decode(f.read())
    with open(SCRIPT_PATH, "wb") as script_file:
        script_file.write(decoded_data)
    print("Update applied successfully!")

def main():
    update_url, expected_hash, new_version = check_for_updates()
    if update_url:
        download_update(update_url)
        if validate_update(UPDATE_PATH, expected_hash):
            apply_update()
            global CURRENT_VERSION
            CURRENT_VERSION = new_version
        else:
            print("Update validation failed. Aborting.")
            os.remove(UPDATE_PATH)
    else:
        print("System is up-to-date.")

if __name__ == "__main__":
    main()

