import requests 
from bs4 import BeautifulSoup
from collections import defaultdict
import re



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


try:

    url1 = input("Enter the first url: ")
    url2 = input("Enter the second url: ")

    rq = requests.get(url1,timeout=20)
    rq1 = requests.get(url2,timeout=20)


    content = rq.text
    soup = BeautifulSoup(content,'html.parser')
    words = re.findall(r'\w+', soup.get_text())

    content1 = rq1.text
    soup1 = BeautifulSoup(content1,'html.parser')
    words1 = re.findall(r'\w+', soup1.get_text())

    V_vector = fingerPrint(words)
    V_vector1 = fingerPrint(words1)


    print("Website 1 title = ",soup.title.string)
    print(V_vector)

    print()

    print("Website 2 title = ",soup1.title.string)
    print(V_vector1)

    comman_bits = 0

    for i in range(64):
        if V_vector1[i] == V_vector[i]:
            comman_bits +=1

    print("Comman bits = ",64 - comman_bits)


finally:
    print("end")



