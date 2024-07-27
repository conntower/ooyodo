import json
import os

import requests
from kancolle.models import slot_item

from script import ROOT_PATH


class Localization:
    def __init__(self, version):
        self.version = version
        self.kcanotify_data_path = os.path.join(ROOT_PATH, 'repo', 'kcanotify-gamedata', 'files')

    def update_item_l10n(self):
        data_path = "slotitem/all.json"
        items = slot_item.load_slot_item_list(self.req_kcdata_json(data_path))

        result = {item.id: {"ja": item.name} for item in items}

        translations = self.load_kcanotify_l10n()

        for k, v in result.items():
            for lang, translation in translations.items():
                if v["ja"] in translation:
                    result[k][lang] = translation[v["ja"]]

        self.check_l10n(result)

        print(f'{len(result)} translations, {len(items)} items')

        with open(os.path.join(ROOT_PATH, 'data', 'slotitem_l10n.json'), 'w') as f:
            data = {
                "data_version": str(self.version),
                "data": result
            }
            json.dump(data, f, indent=2, ensure_ascii=False)

    def load_kcanotify_l10n(self):
        kcanotify_data_path = self.kcanotify_data_path
        item_paths = {
            'en': os.path.join(kcanotify_data_path, 'items-en.json'),
            'ko': os.path.join(kcanotify_data_path, 'items-ko.json'),
            'sc': os.path.join(kcanotify_data_path, 'items-scn.json'),
            'tc': os.path.join(kcanotify_data_path, 'items-tcn.json')
        }
        translations = {}
        for lang, path in item_paths.items():
            with open(path, 'r') as f:
                translations[lang] = json.load(f)
        return translations

    @staticmethod
    def check_l10n(data):
        for item in data.values():
            try:
                assert all(k in item for k in ['ja', 'en', 'ko', 'sc', 'tc'])
            except AssertionError:
                print(item)
                raise

    @staticmethod
    def req_kcdata_json(path):
        from kancolle.data import KC_DATA_URL
        ship_class_url = KC_DATA_URL + path
        return requests.get(ship_class_url).json()
