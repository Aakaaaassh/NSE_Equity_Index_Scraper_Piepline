import requests
from bs4 import BeautifulSoup
import os

# URLs of the webpage 
urls = ['https://www.niftyindices.com/indices/equity/broad-based-indices',
        'https://www.niftyindices.com/indices/equity/sectoral-indices',
        'https://www.niftyindices.com/indices/equity/thematic-indices',
        'https://www.niftyindices.com/indices/equity/strategy-indices']

# Names of the sections
names = ["BROAD BASED INDICES","SECTORAL INDICES","THEMATIC INDICES","STRATEGY INDICES"]


# Custom headers to mimic a browser request
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Function to fetch and parse webpage content
def fetch_webpage(url):
    try:
        # Send a GET request to the URL with custom headers
        response = requests.get(url, headers=headers)
        
        # Raise an exception for HTTP errors
        response.raise_for_status()
        
        # Parse the content using BeautifulSoup
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Return the parsed content
        return soup
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

# Function to scrape the urls
def Fetch_URLs():
    try:
        Dictionary = {}
        for i in range(len(urls)):
            soup = fetch_webpage(urls[i])
            name = names[i]
            Dictionary[name] = {} 
            if soup:
                downloads_list = soup.find('ul', class_='downloads')
                if downloads_list:
                    links = downloads_list.find_all('a')
                    for link in links:
                        href = 'https://www.niftyindices.com' + link.get('href')
                        text = link.text.strip()
                        Dictionary[name][text] = href
                else:
                    print("Element with class 'downloads' not found.")
        return Dictionary
    except:
        print(f"An error occurred {requests.exceptions.RequestException}")
        return None

# Function to download files from the urls
def download_file(url, save_path):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        with open(save_path, 'wb') as file:
            file.write(response.content)
    except requests.exceptions.RequestException as e:
        print(f"Failed to download {url}: {e}")


Dictionary = Fetch_URLs()

# Base directory to store downloaded files
base_dir = 'downloaded_files'

# Initiating Download and Saving in Directories
for i, j in Dictionary.items():
    for key, value in j.items():
        url = str(value)
        soup = fetch_webpage(url)
        if soup:
            downloads_list = soup.find_all('ul', class_='downloads')
            for downloads in downloads_list:
                links = downloads.find_all("a")
                for link in links:
                    text = link.text.strip()
                    if text in ['Factsheet', 'Index Constituent', 'Methodology']:
                        href = link.get('href')
                        if href.startswith("../../../"):
                            href = 'https://www.niftyindices.com/' + href[9:]
                        elif href.startswith("/"):
                            href = 'https://www.niftyindices.com' + href

                        # Create directory structure
                        category_dir = os.path.join(base_dir, i)
                        if not os.path.exists(category_dir):
                            os.makedirs(category_dir)

                        # Define file name and download path
                        file_name = href.split('/')[-1]
                        save_path = os.path.join(category_dir, file_name)
                        
                        # Download the file
                        download_file(href, save_path)
                        print(f"Downloaded {text}: {href} to {save_path}")
        