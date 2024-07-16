import requests
import re
import json
import os

CLOUDFLARE_DOMAIN = "imagedelivery.net"

def upload_image(image_path):
    url = "https://api.cloudflare.com/client/v4/accounts/df2eef4c5a85afb0880466202079da1b/images/v1"
    headers = {
        "Authorization": "Bearer {os.environ['CLOUDFLARE_API_TOKEN']}"
    }
    files = {
        'file': open(image_path, 'rb')
    }
    response = requests.post(url, headers=headers, files=files)
    data = json.loads(response.text)
    if response.status_code == 200:
        variants = data.get('result', {}).get('variants', [])
        if variants:
            return variants[0]
    return None

def process_image_links(file_path):
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

    print("Successful")

def process_all_mdx_files():
    for root, _, files in os.walk("."):
        for file in files:
            if file.endswith(".mdx"):
                process_image_links(os.path.join(root, file))

if __name__ == "__main__":
    process_all_mdx_files()
