import requests
import re
import json
import os
import sys
import mimetypes
from PIL import Image

CLOUDFLARE_DOMAIN = "imagedelivery.net"
VARIANT = "full"  # The specific variant name you want to use
ACCEPTABLE_CONTENT_TYPES = ['image/jpeg', 'image/png', 'image/webp', 'image/gif', 'image/svg+xml']

def download_image(image_url, image_path):
    response = requests.get(image_url, stream=True)
    if response.status_code == 200:
        with open(image_path, 'wb') as out_file:
            for chunk in response.iter_content(chunk_size=8192):
                out_file.write(chunk)
        return True
    return False

def convert_image_to_png(image_path):
    try:
        img = Image.open(image_path)
        new_image_path = os.path.splitext(image_path)[0] + ".png"
        img.save(new_image_path, 'PNG')
        os.remove(image_path)  # Remove the original file
        return new_image_path
    except Exception as e:
        print(f"Failed to convert image: {e}")
        return None

def upload_image(image_path):
    url = "https://api.cloudflare.com/client/v4/accounts/df2eef4c5a85afb0880466202079da1b/images/v1"
    api_token = os.environ.get('CLOUDFLARE_API_TOKEN')

    if not api_token:
        print("Error: CLOUDFLARE_API_TOKEN environment variable is not set.")
        return None

    # Guess the content type of the file
    content_type, _ = mimetypes.guess_type(image_path)
    if content_type not in ACCEPTABLE_CONTENT_TYPES:
        print(f"Unacceptable content type: {content_type}. Converting to PNG.")
        image_path = convert_image_to_png(image_path)
        if not image_path:
            return None
        content_type = 'image/png'

    headers = {
        "Authorization": f"Bearer {api_token}",
        "Content-Type": content_type
    }

    try:
        with open(image_path, 'rb') as file:
            files = {'file': (os.path.basename(image_path), file, content_type)}
            response = requests.post(url, headers=headers, files=files)
            print(f"Response Status Code: {response.status_code}")
            print(f"Response Text: {response.text}")
            
            if response.status_code != 200:
                print(f"Failed to upload image. Status code: {response.status_code}")
                return None

            data = response.json()
            # Look for the specific full-size variant in the list of variants
            variants = data.get('result', {}).get('variants', [])
            full_size_variant = next((variant for variant in variants if VARIANT in variant), None)
            if full_size_variant:
                return full_size_variant
            else:
                print("Full-size variant not found in the response.")
                return None
    except Exception as e:
        print(f"Exception occurred while uploading image: {e}")
        return None

def process_image_links(file_path):
    print(f"Processing file: {file_path}")
    
    with open(file_path, 'r') as file:
        content = file.read()

    pattern = re.compile(r'<Img[^<>]*\ssrc="(.*?)"\s[^<>]*?/?>')
    matches = pattern.findall(content)
    changes_made = False

    for image_url in matches:
        if CLOUDFLARE_DOMAIN in image_url:
            print(f"Image already on Cloudflare: {image_url}")
            continue

        image_name = os.path.basename(image_url)
        image_path = f"images/{image_name}"

        # Ensure the images directory exists
        os.makedirs(os.path.dirname(image_path), exist_ok=True)

        # Download image to disk
        if not download_image(image_url, image_path):
            print(f"Failed to download image: {image_url}")
            continue

        new_image_url = upload_image(image_path)
        if new_image_url:
            content = content.replace(image_url, new_image_url)
            print(f"Replaced image with new URL: {new_image_url}")
            changes_made = True
        else:
            print(f"Failed to upload image")

        # Delete downloaded image from disk
        if os.path.exists(image_path):
            os.remove(image_path)

    if changes_made:
        with open(file_path, 'w') as new_file:
            new_file.write(content)
        print(f"Successfully processed file: {file_path}")
    return changes_made

def process_changed_files(changed_files):
    changes_detected = False
    if not changed_files:
        print("No .mdx files to process.")
        return changes_detected
    for file_path in changed_files:
        if file_path.endswith(".mdx"):
            if process_image_links(file_path):
                changes_detected = True
    return changes_detected

if __name__ == "__main__":
    changed_files = sys.argv[1:]
    if process_changed_files(changed_files):
        print("CHANGES_MADE")
    else:
        print("NO_CHANGES")
