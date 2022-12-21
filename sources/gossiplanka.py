from urllib.parse import quote

import aiohttp
from bs4 import BeautifulSoup

from helper.html_scraper import Scraper


class GossipLanka:
    def __init__(self):
        self.BASE_URL = "https://www.gossiplankanews.com/"

    def _parser_topnews(self, htmls):
        try:
            for html in htmls:
                soup = BeautifulSoup(html, "lxml")
                my_dict = {"data": []}

                for div in soup.find(id="main") \
                        .find("div", class_="grid-posts") \
                        .find_all("div", class_="blog-post"):
                    url = div.find("h2").a["href"]
                    title = div.find("h2").a.text
                    image_link = div.find("span", class_="post-thumb")["image-src"]
                    snippet = div.find("div", class_="snippet-item").text
                    encoded_url = quote(url)
                    my_dict["data"].append({"url": url,"title": title,"snippet": snippet,"image_link": image_link,"encoded_url": encoded_url})
                return my_dict
        except:
            return None

    def _parser_readmore(self, htmls):
        try:
            for html in htmls:
                soup = BeautifulSoup(html, "lxml")
                my_dict = {"post": []}

                div = soup.find(id="main") \
                    .find("div", class_="post-item-inner")

                title = div.find("h1").text
                body = div.find("div", class_="post-body").text

                my_dict["post"].append({"title": title,"body": body})
                return my_dict
        except:
            return None

    async def topnews(self):
        async with aiohttp.ClientSession() as session:
            htmls = await Scraper().get_all_results(session, self.BASE_URL)
            result = self._parser_topnews(htmls)
            return result

    async def readmore(self, url):
        async with aiohttp.ClientSession() as session:
            htmls = await Scraper().get_all_results(session, url)
            result = self._parser_readmore(htmls)
            return result
