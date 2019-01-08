from bs4 import BeautifulSoup
from run import make_json

names = []

with open("scrape_data.txt", "r") as file:
    html = str(file.readlines())
    soup = BeautifulSoup(html, features="html.parser")

    for tag in soup.find_all("a"):
        if "FPmhX" in tag.get("class"):
            # print out username
            names.append(tag.getText())

print(make_json("scrape_data", names))
