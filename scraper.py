import requests
from bs4 import BeautifulSoup
import time
import uuid
import hashlib

URL = "https://search.techcrunch.com/search;_ylt=Awr9ImJ9y_9falAAChmnBWVH;_ylu=Y29sbwNncTEEcG9zAzEEdnRpZAMEc2VjA3BhZ2luYXRpb24-"
HEADERS = {
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
}

params = {
    "p": "fundraising",
    "fr": "techcrunch",
    "fr2": "sb-top",
    "b": 1,
    "pz": "1",
}


def create_uuid():
    return str(uuid.uuid1()).replace("-", "").lower()


# create unique hash
def create_md5(md5_data):
    try:
        s = ""
        for k in md5_data:
            s += str(k)
        result = hashlib.md5(s.encode())
        return result.hexdigest()
    except Exception as e:
        print("Error while creating md5")
        print(e)
        return create_uuid()


def soup_creator(response):
    return BeautifulSoup(response.text, "lxml")


# check wheather user already seen this article
def isuser_seen_the_article(md5):
    try:
        read_file = open("hash.txt", "r").read()
        md5_data = read_file.split("\n")
        if md5 in md5_data:
            return True
        else:
            return False
    except:
        open("hash.txt", "a")
        isuser_seen_the_article(md5)


# fetch all arcticle data of current page
def fetch_article_data(article):
    try:
        data_dict = {}
        data_dict["article_title"] = article.find("a", {"class": "thmb"}).get(
            "title"
        )
        data_dict["article_url"] = article.find("a", {"class": "thmb"}).get(
            "href"
        )
        data_dict["img_url"] = (
            article.find("a", {"class": "thmb"}).find("img").get("src")
        )
        data_dict["date_of_publishing"] = (
            article.find("p", {"class": "csub"})
            .find_all("span")[-1]
            .text.strip()
        )
        return data_dict
    except:
        return {}


# this function recursively run until they not return 50 new article
def get_news_data(data_list, soup=None, counter=0):
    try:
        if soup is None:
            params["b"] = params["b"] + 10
            response = requests.get(
                "https://search.techcrunch.com/search;_ylt=Awr9ImJ9y_9falAAChmnBWVH;_ylu=Y29sbwNncTEEcG9zAzEEdnRpZAMEc2VjA3BhZ2luYXRpb24-",
                headers=HEADERS,
                params=params,
            )
            soup = soup_creator(response)

        articlelist = soup.find("ul", {"class": "compArticleList"})
        # if articlelist is not None
        for article in articlelist.find_all("li"):
            data_dict = fetch_article_data(article)
            md5 = create_md5(
                [
                    data_dict.get("article_title"),
                    data_dict.get("date_of_publishing"),
                ]
            )

            if not isuser_seen_the_article(md5):
                data_list.append(data_dict)
                counter += 1
            write_to_file(md5)
            if counter >= 50:
                return data_list

        else:
            # again call itself for fetching articles
            data_list = get_news_data(data_list, counter=counter)
            return data_list
    except Exception as e:
        print("Exception while fetching news data", e)
        time.sleep(5)
        get_news_data(data_list, counter=counter)


# write each article md5(unique hash) into the file
def write_to_file(md5):
    try:
        read_file = open("hash.txt", "r").read()
        md5_data = read_file.split("\n")
        with open("hash.txt", "a") as hash:
            if md5 not in md5_data:
                hash.write(md5)
                hash.write("\n")
    except:
        open("hash.txt", "w")
        write_to_file(md5)


# return 50 unseen article which user not seen previously
def start_parsing():
    try:
        response = requests.get(
            "https://search.techcrunch.com/search;_ylt=Awr9ImJ9y_9falAAChmnBWVH;_ylu=Y29sbwNncTEEcG9zAzEEdnRpZAMEc2VjA3BhZ2luYXRpb24-",
            headers=HEADERS,
            params=params,
        )
        data_list = []
        soup = soup_creator(response)
        data = get_news_data(data_list, soup=soup)
        return dict(status="SUCCESS", data=data)
    except Exception as e:
        return dict(
            status="ERROR", message="EXCEPTION OCCURED " + str(e).upper()
        )
