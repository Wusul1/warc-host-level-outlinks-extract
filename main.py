import os
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from warcio.archiveiterator import ArchiveIterator

def extract_urls_from_warc(warc_path):
    urls = []
    total_htmls = 0
    processed_htmls = 0
    total_urls = 0
    with open(warc_path, 'rb') as warc_file:
        for record in ArchiveIterator(warc_file):
            if record.rec_type == 'response' and 'text/html' in record.http_headers.get('Content-Type', ''):
                total_htmls += 1
                html_content = record.content_stream().read()
                soup = BeautifulSoup(html_content, 'html.parser')
                for link in soup.find_all('a'):
                    href = link.get('href')
                    if href:
                        if not strip_to_host_level(href) in urls:
                            urls.append(strip_to_host_level(href))
                            total_urls += 1
                processed_htmls += 1
                if processed_htmls % 100 == 0:
                    print(f"Processed {processed_htmls} HTMLs")
                    print(f"Total URLs found so far: {total_urls}")
    print(f"Done")
    print(f"Total HTMLs processed: {total_htmls}")
    print(f"Total URLs found: {total_urls}")
    return urls

def strip_to_host_level(url):
    parsed_url = urlparse(url)
    return parsed_url.scheme + '://' + parsed_url.netloc

def deduplicate_urls(urls):
    return list(set(urls))

def write_urls_to_file(urls, output_file):
    with open(output_file, 'w') as file:
        for url in urls:
            file.write(url + '\n')

# Get the path to the WARC file from the user
warc_path = input("Enter the path to the WARC file: ")

# Extract URLs from the WARC file
urls = extract_urls_from_warc(warc_path)

# Write host level URLs to file
output_file = 'hosts_from_warc.txt'
write_urls_to_file(urls, output_file)

print("Host level URLs have been written to", output_file)

