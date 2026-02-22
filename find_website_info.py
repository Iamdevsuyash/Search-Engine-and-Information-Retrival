import requests 
from bs4 import BeautifulSoup
import re

try:

    url1 = input("Enter the first url: ")
    # url2 = input("Enter the second url: ")

    rq = requests.get("https://sitare.org/",timeout=20)
    # rq1 = requests.get(url2,timeout=20)


    content = rq.text
    soup = BeautifulSoup(content,'html.parser')
    print((soup.get_text().split()))
    words = soup.get_text()

finally:
    print("end")