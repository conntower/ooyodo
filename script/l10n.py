import json
import logging
import os

import requests
from kancolle.models import slot_item

from script import ROOT_PATH

logger = logging.getLogger(__name__)

class Localization:
    def __init__(self, version):
        self.version = version
        self.kcanotify_data_path = os.path.join(ROOT_PATH, 'repo', 'kcanotify-gamedata', 'files')

    def update_useitem_in_improve_l10n(self):
        kcanotify_data_path = os.path.join(self.kcanotify_data_path, 'akashi_reqitems.json')
        file_path = os.path.join(ROOT_PATH, 'data', 'useitem_in_improve_l10n.json')

        with open(kcanotify_data_path, 'r') as f:
            req_items = json.load(f)

        res = {}

        for item in req_items:
            if item['id'] > 0:
                res[item['useitem_id']] = {
                    'ja': item['name']['jp'],
                    'en': item['name']['en'],
                    'ko': item['name']['ko'],
                    'sc': item['name']['scn'],
                    'tc': item['name']['tcn']
                }

        self.check_l10n(res)

        with open(file_path, 'w') as f:
            data = {
                "data_version": str(self.version),
                "data": res
            }
            json.dump(data, f, indent=2, ensure_ascii=False)

    def update_item_l10n(self):
        data_path = "slotitem/all.json"
        items = slot_item.load_slot_item_list(self.req_kcdata_json(data_path))

        self.save_item_l10n_with_id(items)
        # self.save_item_l10n_without_id(items)

    def save_item_l10n_without_id(self, items):
        result = {item.name: {} for item in items}
        translations = self.load_kcanotify_l10n()
        for k, v in result.items():
            for lang, translation in translations.items():
                if k in translation:
                    result[k][lang] = translation[k]
        self.check_l10n(result, ['en', 'ko', 'sc', 'tc'])
        logger.info(f'{len(result)} translations, {len(items)} items')
        with open(os.path.join(ROOT_PATH, 'data', 'slotitem_l10n_without_id.json'), 'w') as f:
            data = {
                "data_version": str(self.version),
                "data": result
            }
            json.dump(data, f, indent=2, ensure_ascii=False)

    def save_item_l10n_with_id(self, items):
        result = {item.id: {"ja": item.name} for item in items}
        translations = self.load_kcanotify_l10n()
        for k, v in result.items():
            for lang, translation in translations.items():
                if v["ja"] in translation:
                    result[k][lang] = translation[v["ja"]]
        self.check_l10n(result)
        logger.info(f'{len(result)} translations, {len(items)} items')
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
    def check_l10n(data, lang_code=None):
        if lang_code is None:
            lang_code = ['ja', 'en', 'ko', 'sc', 'tc']
        for item in data.values():
            try:
                assert all(k in item for k in lang_code)
            except AssertionError:
                logger.error(f" {lang_code} not found in {item}")
                raise

    @staticmethod
    def req_kcdata_json(path):
        from kancolle.data import KC_DATA_URL
        url = KC_DATA_URL + path
        return requests.get(url).json()
