import requests 
from bs4 import BeautifulSoup
import re
import sys

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/122.0 Safari/537.36"
    }


def main():
    args = sys.argv

    try:
        url = args[1]
        rq = requests.get(url,headers=headers,timeout=20)
        soup = BeautifulSoup(rq.text,'html.parser')

        urls = [link.get('href') for link in soup.find_all('a')]
        
        print("Title : " + soup.title.text if soup.title else "None" )
        print("Body : " + soup.body.getText(strip=True) if soup.body else "None")

        print()

        print("Urls : ")
        for url in urls:
            print(f"    {url}")

    except Exception as e:
        print("Invalid Input")

    finally:
        print("end")


main()