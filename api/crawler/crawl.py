import requests
from bs4 import BeautifulSoup
import json
# from translate import Translator

class Crawl:
	def __init__(self, lang = 'en', provider = 'economictimes'):
		self.lang = lang
		self.provider = provider
		# self.translator = Translator(from_lang = 'hi', to_lang = "en")
		self.article = {}

		self.KEYS = ['inLanguage', 'headline', 'articleBody']

	def getNews(self, url):
		try:
			if self.provider == 'economictimes':
				content_soup = BeautifulSoup(requests.get(url).text, 'html.parser')
				jsonData = json.loads(content_soup.find_all("script", attrs = {"type": "application/ld+json"})[1].string)

				self.article.update({ "url": url })
			
				for key in self.KEYS:
					self.article.update({ key: jsonData[key] })

			elif self.provider == "dainik":
				content_soup = BeautifulSoup(requests.get(url).text, 'html.parser')

				self.article.update({ 'inLanguage': 'hi', 'url': url })
				self.article.update({"articleBody": content_soup.find_all('article')[0].find_all('p')[0].string})

				title = content_soup.find("h1").contents
				self.article.update({"headline": title[0].string + title[1].string})

			return self.article
		except:
			return None

if __name__ == "__main__":
	crawler = Crawl(provider = "dainik")
	url = "https://www.bhaskar.com/national/news/air-india-controversy-delhi-pune-flight-delays-due-to-pilot-131903634.html"
	print(crawler.getNews(url))
