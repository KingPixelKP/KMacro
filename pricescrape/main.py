import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import json

def main():

    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 Edge/16.16299'
    }

    url = "https://backpack.tf/search?text={}%20".format(input(">>>"))

    results = requests.get(url=url, headers=headers)

    text = json.loads(results.content).get("results")

    for i in text:
        for k in i.get("values"):
            print(i.get("item_name"), k.get("quality"), k.get("price"))

main()