import requests
from bs4 import BeautifulSoup
import sys
import json

html = requests.get("https://www.instagram.com/{0}/".format(sys.argv[1])).text

# get description
text = html.split('<script type="application/ld+json">')[1].split('</script>')[0]
data = json.loads(text)
account_type = data["@type"]
name = data["name"]
username = data["alternateName"][1:]
description = data["description"].replace("\n", " ")

print("Name: {0}\nUsername: {1}\nAccount Type: {2}\nDescription: {3}".format(name, username, account_type, description))

# get followers, following, etc
soup = BeautifulSoup(html, features="html.parser")
for tag in soup.find_all("meta"):
    if tag.get("property", None) == "og:description":
        description = tag.get("content", None)
        # TODO: Clean these up, shouldn't have to re-do these operations
        followers = description.split("Followers")[0].replace(',', '').strip()
        following = description.split("Followers")[1].split("Following")[0].replace(',', '').strip()
        posts = description.split("Posts")[0].split("Following")[1].replace(',', '').strip()
        print("Followers: {0}\nFollowing: {1}\nPosts: {2}".format(followers, following, posts))
