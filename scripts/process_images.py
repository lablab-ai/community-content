import requests
import re
import json
import os
import sys

CLOUDFLARE_DOMAIN = "imagedelivery.net"
VARIANT = "full"  # The specific variant name you want to use

def upload_image(image_path):
    url = "https://api.cloudflare.com/client/v4/accounts/df2eef4c5a85afb0880466202079da1b/images/v1"
    headers = {
        "Authorization": f"Bearer {os.environ['CLOUDFLARE_API_TOKEN']}"
    }
    files = {
        'file': open(image_path, 'rb')
    }
    response = requests.post(url, headers=headers, files=files)
    data = json.loads(response.text)
    if response.status_code == 200:
        # Look for the specific full-size variant in the list of variants
        variants = data.get('result', {}).get('variants', [])
        full_size_variant = next((variant for variant in variants if VARIANT in variant), None)
        if full_size_variant:
            return full_size_variant
    return None

def process_image_links(file_path):
    print(f"Processing file: {file_path}")
    
    with open(file_path, 'r') as file:
        content = file.read()

    pattern = re.compile(r'<Img[^<>]*\ssrc="(.*?)"\s[^<>]*?/?>')
    matches = pattern.findall(content)

    for image_url in matches:
        if CLOUDFLARE_DOMAIN in image_url:
            print(f"Image already on Cloudflare: {image_url}")
            continue

        image_name = os.path.basename(image_url)
        image_path = f"images/{image_name}"

        # Ensure the images directory exists
        os.makedirs(os.path.dirname(image_path), exist_ok=True)

        # Download image to disk
        r = requests.get(image_url)
        with open(image_path, 'wb') as image_file:
            image_file.write(r.content)

        new_image_url = upload_image(image_path)
        if new_image_url:
            content = content.replace(image_url, new_image_url)
            print(f"Replaced image with new URL: {new_image_url}")
        else:
            print(f"Failed to upload image")

        # Delete downloaded image from disk
        os.remove(image_path)

    with open(file_path, 'w') as new_file:
        new_file.write(content)

    print(f"Successfully processed file: {file_path}")

def process_changed_files(changed_files):
    if not changed_files:
        print("No .mdx files to process.")
        return
    for file_path in changed_files:
        if file_path.endswith(".mdx"):
            process_image_links(file_path)

if __name__ == "__main__":
    changed_files = sys.argv[1:]
    process_changed_files(changed_files)
