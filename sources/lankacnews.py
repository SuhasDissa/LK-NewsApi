from urllib.parse import quote

import aiohttp
from bs4 import BeautifulSoup

from helper.html_scraper import Scraper


class LankaCNews:
    def __init__(self):
        self.BASE_URL = "https://lankacnews.com/news"

    def _parser_topnews(self, htmls):
        try:
            for html in htmls:
                soup = BeautifulSoup(html, "lxml")
                my_dict = {"data": []}

                for div in soup.find(id="page-main-news") \
                        .find("div", class_="left") \
                        .find_all("article"):
                    url = div.find("h2").a["href"]
                    title = div.find("h2").a.text
                    image_link = div.find("img")["src"]
                    snippet = div.find("p").text
                    encoded_url = quote(url)
                    my_dict["data"].append({"url": url})
                    my_dict["data"].append({"title": title})
                    my_dict["data"].append({"snippet": snippet})
                    my_dict["data"].append({"image_link": image_link})
                    my_dict["data"].append({"encoded_url": encoded_url})
                return my_dict
        except:
            return None

    def _parser_readmore(self, htmls):
        try:
            for html in htmls:
                soup = BeautifulSoup(html, "lxml")
                my_dict = {"post": []}

                div = soup.find(id="article-container") \
                    .find("article")

                title = div.find("h1").a.text
                paragraphes = div.find_all("p")
                body = ''
                for p in paragraphes:
                    body += p.text

                my_dict["post"].append({"title": title})
                my_dict["post"].append({"body": body})
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
