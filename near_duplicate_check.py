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

stopwords = get_stop_words('en')

print(stopwords)

def hash(s):
    m = 2**64
    p = 53
    power = 1
    hash = 0

    for i in range(len(s)):
        hash = hash + (ord(s[i]))*(power) % m
        power *= p

    return hash%m


def fingerPrint(words):

    words_with_weights = defaultdict(int)

    for word in words:
        if word not in stopwords:
            words_with_weights[hash(word)]+=1

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


def parse_doc(doc):
    soup = BeautifulSoup(doc,'lxml')

    words = [word for word in re.findall(r'\w+', soup.get_text().lower()) if word not in stopwords]

    return soup.title,words



try:
    args = sys.argv

    url1 = args[1]
    url2 = args[2]

    

    rq = requests.get(url1,headers=headers,timeout=20)
    rq1 = requests.get(url2,headers=headers,timeout=20)


    title,words = parse_doc(rq.text)
    title1,words1 = parse_doc(rq1.text)


    V_vector = fingerPrint(words)
    V_vector1 = fingerPrint(words1)


    if (title):
        print("Website 1 title = ",title.text)
    else:
        print("Title not found")

    # print(words)

    if (title1):
        print("Website 2 title = ",title1.text)
    else:
        print("Title not found")

    # print(words1)

    comman_bits = 0

    for i in range(64):
        if V_vector1[i] == V_vector[i]:
            comman_bits +=1

    print("Comman bits : ",comman_bits)

finally:
    print("end")



