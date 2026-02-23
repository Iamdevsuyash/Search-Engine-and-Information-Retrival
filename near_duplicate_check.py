
import requests 
from bs4 import BeautifulSoup
from collections import defaultdict
import re
import sys
from stop_words import get_stop_words


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/122.0 Safari/537.36"
    }


# Get English stop words using language code
# used from -  https://pypi.org/project/stop-words/

stopwords = get_stop_words('en')

print("Number of stopwords : " ,len(stopwords))

def hash_word(s):
    m = 2**64
    p = 53
    power = 1
    hash = 0

    for i in range(len(s)):
        hash = (hash + (ord(s[i]))*(power)) % m
        power = (power*p)%m

    return hash%m


def fingerPrint(text):

    words = [word for word in re.findall(r'\w+',text) if word not in stopwords]
    words_with_weights = defaultdict(int)

    for word in words:
        words_with_weights[hash_word(word)] += 1

    V_vector = [0]*64

    for i in range(64):
        for fingerprint in words_with_weights:

            bit = (fingerprint >> (63 - i)) & 1

            if bit == 1:
                V_vector[i] += words_with_weights[fingerprint]
            else:
                V_vector[i] -= words_with_weights[fingerprint]
    
        if V_vector[i] > 0:
            V_vector[i] = 1
        else:
            V_vector[i] = 0

    return V_vector


def parse_doc(url):
    rq = requests.get(url,headers=headers,timeout=20)
    soup = BeautifulSoup(rq.text,'html.parser')

    return soup.title.text if soup.title else None,soup.get_text().lower()


def main():
    try:
        args = sys.argv

        url1 = args[1]
        url2 = args[2]

        title,text = parse_doc(url1)
        title1,text1 = parse_doc(url2)


        V_vector = fingerPrint(text)
        V_vector1 = fingerPrint(text1)


        print("Website 1 title = ",title)
        print("Website 2 title = ",title1)


        comman_bits = 0

        for i in range(64):
            if V_vector1[i] == V_vector[i]:
                comman_bits +=1

        print("Comman bits : ",comman_bits)
        print("Websites are Similar" if comman_bits > 60 else "Not similar")

    except Exception as e:
        print(e)


    finally:
        print("Thank you!")


main()

