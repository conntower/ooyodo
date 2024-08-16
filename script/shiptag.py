import json
import os

import requests

from script import ROOT_PATH


class ShipTag:
    def __init__(self, color, name):
        self.color = color
        self.name = name

class ShipTagManager:
    def __init__(self, data_version):
        self.data_version = data_version
        self.tags = {}
        self.request_tags()

    def request_tags(self):
        url = "https://raw.githubusercontent.com/poooi/poi/master/assets/data/fcd/shiptag.json"
        data = requests.get(url).json()
        colors = data["data"]["color"]
        fleetname = data["data"]["fleetname"]
        for index, color in enumerate(colors):
            color = color.replace("#", "0xff")
            name = {
                "ja": fleetname["ja-JP"][index],
                "en": fleetname["en-US"][index],
                "sc": fleetname["zh-CN"][index],
                "tc": fleetname["zh-TW"][index]
            }
            self.tags[index + 1] = ShipTag(color, name)

    def load_tags(self):
        with open(os.path.join(ROOT_PATH, 'repo', 'poi', 'shiptag.json'), 'r') as f:
            data = json.load(f)
            colors = data["data"]["color"]
            fleetname = data["data"]["fleetname"]
            for index, color in enumerate(colors):
                color = color.replace("#", "0xff")
                name = {
                    "ja": fleetname["ja-JP"][index],
                    "en": fleetname["en-US"][index],
                    "sc": fleetname["zh-CN"][index],
                    "tc": fleetname["zh-TW"][index]
                }
                self.tags[index] = ShipTag(color, name)

    def update_tags(self):
        data = {
            "data_version": self.data_version,
            "data": self.tags,
        }
        file_path = os.path.join(ROOT_PATH, 'data', 'event_ship_tags.json')
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=lambda o: o.__dict__)
        print(f'finish update tags, {len(self.tags)} tags')
