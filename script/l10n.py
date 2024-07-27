import json
import os

from kancolle.models import slot_item
import requests

from script import ROOT_PATH, DATA_VERSION


def req_kcdata_json():
    from kancolle.data import KC_DATA_URL
    ship_class_url = KC_DATA_URL + "slotitem/all.json"
    return requests.get(ship_class_url).json()


def load_kcanotify_l10n():
    kcanotify_path = os.path.join(ROOT_PATH, 'repo', 'kcanotify-gamedata')
    kcanotify_data_path = os.path.join(kcanotify_path, 'files')
    item_en_path = os.path.join(kcanotify_data_path, 'items-en.json')
    item_ko_path = os.path.join(kcanotify_data_path, 'items-ko.json')
    item_sc_path = os.path.join(kcanotify_data_path, 'items-scn.json')
    item_tc_path = os.path.join(kcanotify_data_path, 'items-tcn.json')
    with open(item_en_path, 'r') as f:
        item_en = json.load(f)
    with open(item_ko_path, 'r') as f:
        item_ko = json.load(f)
    with open(item_sc_path, 'r') as f:
        item_sc = json.load(f)
    with open(item_tc_path, 'r') as f:
        item_tc = json.load(f)
    return item_en, item_ko, item_sc, item_tc


def check_l10n(data):
    for item in data.values():
        try:
            assert item.get("ja") is not None
            assert item.get("en") is not None
            assert item.get("ko") is not None
            assert item.get("sc") is not None
            assert item.get("tc") is not None
        except AssertionError:
            print(f'item {item["ja"]} is missing translation')
            raise


if __name__ == '__main__':
    items = slot_item.load_slot_item_list(req_kcdata_json())

    l10n_dict = {}
    for item in items:
        l10n_dict[item.id] = {"ja": item.name}

    item_en, item_ko, item_sc, item_tc = load_kcanotify_l10n()
    for k, v in l10n_dict.items():
        if v["ja"] in item_en:
            l10n_dict[k]["en"] = item_en[v["ja"]]
        if v["ja"] in item_ko:
            l10n_dict[k]["ko"] = item_ko[v["ja"]]
        if v["ja"] in item_sc:
            l10n_dict[k]["sc"] = item_sc[v["ja"]]
        if v["ja"] in item_tc:
            l10n_dict[k]["tc"] = item_tc[v["ja"]]

    check_l10n(l10n_dict)

    with open(os.path.join(ROOT_PATH, 'data', 'item_l10n.json'), 'w') as f:
        data = {
            "data_version": str(DATA_VERSION),
            "data": l10n_dict
        }
        json.dump(data, f, indent=2, ensure_ascii=False)
