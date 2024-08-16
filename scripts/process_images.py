import requests
import re
import json
import os
import sys

CLOUDFLARE_DOMAIN = "imagedelivery.net"
VARIANT = "full"  # The specific variant name you want to use

def upload_image(image_path):
    """
    Upload an image to Cloudflare and retrieve the URL of the specific image variant.
    
    :param image_path: Path of the image file to upload.
    :return: The URL of the full-size variant of the uploaded image or None if upload fails.
    """
    url = "https://api.cloudflare.com/client/v4/accounts/df2eef4c5a85afb0880466202079da1b/images/v1"
    headers = {
        "Authorization": f"Bearer {os.environ.get('CLOUDFLARE_API_TOKEN', '')}"  # Using environment variable for token
    }
    
    # Check if the Cloudflare API token is missing
    if not headers['Authorization']:
        print(f"Error: CLOUDFLARE_API_TOKEN environment variable is not set.")
        return None

    try:
        with open(image_path, 'rb') as image_file:
            print(f"Uploading image: {image_path}")
            files = {'file': image_file}
            response = requests.post(url, headers=headers, files=files)
            response.raise_for_status()  # Raise HTTPError for bad responses
    except FileNotFoundError:
        print(f"Error: File {image_path} not found.")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error uploading image: {e}")
        print(f"Response Text: {response.text if response else 'No response'}")
        return None

    try:
        data = response.json()
    except json.JSONDecodeError:
        print(f"Error decoding JSON response from Cloudflare. Response text: {response.text}")
        return None

    # Check if the response is missing expected data
    if response.status_code == 200:
        variants = data.get('result', {}).get('variants', [])
        if not variants:
            print("Warning: No variants found in the response from Cloudflare.")
        full_size_variant = next((variant for variant in variants if VARIANT in variant), None)
        if full_size_variant:
            print(f"Successfully uploaded image. Variant URL: {full_size_variant}")
            return full_size_variant
        else:
            print("Warning: No full-size variant found in the uploaded image response.")
    else:
        print(f"Error: Received unexpected status code {response.status_code} from Cloudflare.")
        print(f"Response: {response.text}")
    
    return None

def process_image_links(file_path):
    """
    Process image links in the given .mdx file. If any image URLs are found,
    they are downloaded, uploaded to Cloudflare, and replaced with the new URL.
    
    :param file_path: Path to the .mdx file to process.
    :return: True if changes were made to the file, False otherwise.
    """
    print(f"Processing file: {file_path}")
    
    try:
        with open(file_path, 'r') as file:
            content = file.read()
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        return False

    # Regular expression to find all <Img> tags and extract the src attribute (image URLs)
    pattern = re.compile(r'<Img[^<>]*\ssrc="(.*?)"\s[^<>]*?/?>')
    matches = pattern.findall(content)
    changes_made = False

    for image_url in matches:
        # Skip images that are already hosted on Cloudflare
        if CLOUDFLARE_DOMAIN in image_url:
            print(f"Image already on Cloudflare: {image_url}")
            continue

        image_name = os.path.basename(image_url)  # Extract image file name from URL
        image_path = f"images/{image_name}"  # Set local path for saving the image

        # Ensure the local 'images' directory exists
        os.makedirs(os.path.dirname(image_path), exist_ok=True)

        try:
            # Download the image from the original URL
            print(f"Downloading image from URL: {image_url}")
            r = requests.get(image_url)
            r.raise_for_status()  # Raise HTTPError for bad responses
            with open(image_path, 'wb') as image_file:
                image_file.write(r.content)  # Save the image to disk
            print(f"Successfully downloaded image to: {image_path}")
        except requests.exceptions.RequestException as e:
            print(f"Error downloading image: {e}")
            continue

        # Upload the image to Cloudflare and get the new URL
        new_image_url = upload_image(image_path)
        if new_image_url:
            # Replace the old URL with the new Cloudflare URL in the file content
            content = content.replace(image_url, new_image_url)
            print(f"Replaced image with new URL: {new_image_url}")
            changes_made = True
        else:
            print("Failed to upload image to Cloudflare.")

        # Remove the image from local storage after processing
        try:
            os.remove(image_path)
            print(f"Deleted local image: {image_path}")
        except OSError as e:
            print(f"Error deleting local image: {e}")

    # If any changes were made, overwrite the .mdx file with the new content
    if changes_made:
        try:
            with open(file_path, 'w') as new_file:
                new_file.write(content)
            print(f"Successfully processed file: {file_path}")
        except OSError as e:
            print(f"Error writing updated content to {file_path}: {e}")
    
    return changes_made

def process_changed_files(changed_files):
    """
    Process each changed .mdx file and replace image URLs as needed.
    
    :param changed_files: List of .mdx file paths to process.
    :return: True if any changes were detected across all files, False otherwise.
    """
    changes_detected = False
    
    # Check if there are any files to process
    if not changed_files:
        print("No .mdx files to process.")
        return changes_detected
    
    # Process each .mdx file
    for file_path in changed_files:
        if file_path.endswith(".mdx"):
            if process_image_links(file_path):  # If changes were made to the file, set flag
                changes_detected = True
    
    return changes_detected

if __name__ == "__main__":
    # Take the list of changed files as arguments from the command line
    changed_files = sys.argv[1:]
    
    # Process the files and print whether changes were made
    if process_changed_files(changed_files):
        print("CHANGES_MADE")
    else:
        print("NO_CHANGES")
