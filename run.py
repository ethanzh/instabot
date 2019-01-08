import requests
from bs4 import BeautifulSoup
import json
import sys


def make_json(filename, usernames):
    data = {}
    count = 0
    if filename[-4:] != ".csv":
        filename = filename + ".csv"
    f = open(filename, "w")
    f.write("username,name,account_type,public,description,followers,following,posts\n")
    for user in usernames:
        try:
            html = requests.get("https://www.instagram.com/{0}/".format(user)).text
        except TimeoutError:
            print("Timed out", user)
            continue
        except ConnectionResetError:
            print("Connection reset", user)
            continue

        # if alternateName doesn't exist, profile is private
        try:
            text = html.split('<script type="application/ld+json">')[1].split('</script>')[0]
        except IndexError:
            continue
        data = json.loads(text)
        name = ""
        try:
            username = data["alternateName"][1:]
            public = True
        except KeyError:
            username = data["name"][1:]
            public = False
        try:
            account_type = data["@type"]
        except KeyError:
            account_type = ""
        if public:
            try:
                name = data["name"].replace(",", " ")
            except KeyError:
                name = ""
        try:
            bio_description = " ".join(data["description"].replace(",", " ").split())
        except KeyError:
            bio_description = ""

        # get followers, following, etc
        soup = BeautifulSoup(html, features="html.parser")
        for tag in soup.find_all("meta"):
            if tag.get("property", None) == "og:description":
                description = tag.get("content", None)
                # TODO: Clean these up, shouldn't have to re-do these operations
                followers = description.split("Followers")[0].replace(',', '').strip()
                following = description.split("Followers")[1].split("Following")[0].replace(',', '').strip()
                posts = description.split("Posts")[0].split("Following")[1].replace(',', '').strip()

                f.write("{0},{1},{2},{3},{4},{5},{6},{7}\n".format(username, name, account_type, public,
                                                               bio_description, following, followers, posts))
                count += 1
                print("Completed {0} out of {1}".format(count, len(usernames)))

    return data


if len(sys.argv) != 1:
    if len(sys.argv) == 2:
        raise ValueError("Must provide usernames")
    else:
        make_json(sys.argv[1], sys.argv[2:])
