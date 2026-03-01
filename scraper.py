import requests
from bs4 import BeautifulSoup
import sys
from urllib.parse import urljoin, urlparse

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/122.0 Safari/537.36"
    }

def update_url(url):
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url
    return url

def main(url):
    url = update_url(url)

    try:
        rq = requests.get(url, headers=headers, timeout=20)
        rq.raise_for_status()

    except requests.RequestException:
        sys.exit(1)

    soup = BeautifulSoup(rq.text, "html.parser")

    title = soup.title.string.strip() if soup.title and soup.title.string else ""
    print(title)
    print()

    if soup.body:
        text = soup.body.get_text(separator=" ", strip=True)
    else:
        text = "" 

    print(text)

    print()

    links = set()
    urls = soup.find_all("a", href=True)

    for link in urls:
        url1 = urljoin(url, link["href"])
        parsed_url = urlparse(url1)

        if parsed_url.scheme in ['http','https']:
            links.add(url1)

    for link in links:
        print(link)


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Invalid argument length, Please provide single url as input!")
        sys.exit(1)
        
    main(sys.argv[1])

