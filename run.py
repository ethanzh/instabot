import requests
from bs4 import BeautifulSoup
import json
import sys
import sqlite3


def make_json(filename, usernames):
    data = {}
    count = 0
    if filename[-4:] != ".csv":
        filename = filename + ".csv"
    f = open(filename, "w")
    f.write("username,name,account_type,public,description,followers,following,posts\n")
    conn = sqlite3.connect('accounts.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS accounts (username text, name text, account_type text, public numeric, 
    description text, followers integer, following integer, posts integer, UNIQUE (username))''')
    conn.commit()
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
                name = data["name"].replace(",", " ").replace("、", " ").replace("，", " ")
            except KeyError:
                name = ""
        try:
            bio_description = " ".join(data["description"].replace(",", " ").replace("、", " ").replace("，", " ").split())
        except KeyError:
            bio_description = ""

        # get followers, following, etc
        soup = BeautifulSoup(html, features="html.parser")
        for tag in soup.find_all("meta"):
            if tag.get("property", None) == "og:description":
                description = tag.get("content", None)

                first_block = description.split("Followers")

                followers = parse_number(first_block[0].replace(',', '').strip())
                following = parse_number(first_block[1].split("Following")[0].replace(',', '').strip())
                posts = parse_number(description.split("Posts")[0].split("Following")[1].replace(',', '').strip())

                f.write("{0},{1},{2},{3},{4},{5},{6},{7}\n".format(username, name, account_type, public,
                                                               bio_description, following, followers, posts))
                count += 1
                c.execute("INSERT INTO accounts VALUES (\'%s\', \'%s\', \'%s\', %d, \'%s\', %d, %d, %d)" %
                          (username, name, account_type, public, bio_description, followers, following, posts))
                conn.commit()
                print("Completed {0} out of {1}".format(count, len(usernames)))

    return data


def parse_number(num):
    if num[-1] == "k":
        return int(float(num[:-1]) * 1000)
    elif num[-1] == "m":
        return int(float(num[:-1]) * 1_000_000)
    else:
        return int(num)


if len(sys.argv) != 1:
    if len(sys.argv) == 2:
        raise ValueError("Must provide usernames")
    else:
        make_json(sys.argv[1], sys.argv[2:])
