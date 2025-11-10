import re
import requests
import json
from bs4 import BeautifulSoup


class EconomicTimes:
    def __init__(self):
        self.base = "https://economictimes.indiatimes.com/topic/"
        self.last = json.loads(open("./access.json", "r").read())[self.base]
        self.object = {
            "provider": "economictimes",
            "lang": "en",
            "urls": []
        }

    def _readCard(self, endpoint):
        req = requests.get(self.base + endpoint)
        cards = BeautifulSoup(req.content, "html.parser").find_all("div", attrs={"class": "story_list"})
        last_access = self.last[endpoint]

        for card in cards:
            current_link = card.find("div", "contentD").find("a")["href"]
            if last_access == current_link:
                break
            self.object["urls"].append(self.base + current_link)

        if len(cards) > 0:
            self.last[endpoint] = cards[0].find("div", "contentD").find("a")["href"]
        

    def run(self):
        for dept in self.last.keys():
            self._readCard(dept)

        access_json = json.loads(open("./access.json", "r").read())
        access_json[self.base] = self.last
        open("./access.json", "w").write(json.dumps(access_json, indent=4))

        data = json.loads(open("./links.json", "r").read())
        data.append(self.object)
        open("./links.json", "w").write(json.dumps(data, indent=4))

        return self.object


class DainikBhaskar:
    def __init__(self):
        self.base = "https://www.bhaskar.com/national/"
        self.last = json.loads(open("./access.json", "r").read())[self.base]
        self.object = {
            "provider": "dainik",
            "lang": "hi",
            "urls": []
        }

    def _readCard(self, endpoint):
        req = requests.get(self.base + endpoint)
        last_access = self.last[endpoint]
        cards = set(map(lambda element: element["href"], BeautifulSoup(req.content, "html.parser").find_all(href=re.compile("^/national.*\.html$"))))

        for card in cards:
            if last_access == card:
                break
            self.object["urls"].append(self.base + card)

        if len(cards) > 0:
            self.last[endpoint] = list(cards)[0]

    def run(self):
        for dept in self.last.keys():
            self._readCard(dept)

        access_json = json.loads(open("./access.json", "r").read())
        access_json[self.base] = self.last
        open("./access.json", "w").write(json.dumps(access_json, indent=4))

        data = json.loads(open("./links.json", "r").read())
        data.append(self.object)
        open("./links.json", "w").write(json.dumps(data, indent=4))

        return self.object