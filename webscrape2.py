import requests
from bs4 import BeautifulSoup
import urllib

# URL of NWAnimators.com
url = 'https://johnaroberts.blogspot.com/'

# Send a GET request to fetch the page content
page = requests.get(url)

# Check if the request was successful
if page.status_code == 200:
    # Parse HTML content
    soup = BeautifulSoup(page.content, 'html.parser')

    # Find and download images
    image_tags = soup.find_all('img')
    for image_tag in image_tags:
        image_url = image_tag.get('src')
        # Download the image
        if image_url.startswith(('http://', 'https://')):
            file_name = image_url.split("/")[-1]
            file_path = f'J:\\webscrap\\{file_name}'  # Modified file path
            urllib.request.urlretrieve(image_url, file_path)
        else:
            absolute_image_url = urllib.parse.urljoin(url, image_url)
            file_name = absolute_image_url.split("/")[-1]
            file_path = f'J:\\webscrap\\{file_name}'  # Modified file path
            urllib.request.urlretrieve(absolute_image_url, file_path)
else:
    print("Failed to retrieve the page. Status code:", page.status_code)
