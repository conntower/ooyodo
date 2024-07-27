import json
import os.path

from script import *


class Item:
    def __init__(self, id, improve_data, use_item_map):
        self.improvement = None
        self.id = int(id)
        self.improve_data = improve_data
        self.use_item_map = use_item_map

    def __dict__(self):
        self.reformat()
        res = {
            "id": self.id,
            "improvement": self.improvement
        }
        assert len(self.improvement) > 0
        return res

    def reformat(self):
        self.improvement = []

        for i in self.improve_data['improvement']:
            upgrade = i['upgrade']
            req = i['req']
            resource = i['resource']
            req_item = i.get('require_item', None)

            improve = {
                "req": [{
                    "ship": item[1] if isinstance(item[1], list) else [],
                    "day": day_stringify(item[0])
                } for item in req],
                "resource": self.resource_reformat(resource, req_item),
            }
            if upgrade:
                improve["upgrade"] = {"id": upgrade[0], "lv": upgrade[1]}

            self.improvement.append(improve)

    def resource_reformat(self, data_list, req_item):
        res = {"base": data_list[0], "extra": []}
        for i in data_list[1:]:
            item = {
                "dm": i[0:2],
                "im": i[2:4],
            }
            if i[4] > 0:
                item["slot"] = {str(i[4]): i[5]}
            res["extra"].append(item)
        if req_item:
            res["extra"][2]["use"] = {str(self.use_item_map[item[0]]): item[1] for item in req_item}
        return res


def day_stringify(day):
    """
    [true, true, true, true, true, true, true] -> 1111111
    """
    return "".join([str(int(i)) for i in day])


def update_schedule(data_version):
    kcanotify_path = os.path.join(ROOT_PATH, 'repo', 'kcanotify-gamedata')
    kcanotify_data_path = os.path.join(kcanotify_path, 'files')
    data_path = os.path.join(ROOT_PATH, 'data')

    with open(os.path.join(kcanotify_data_path, 'akashi_reqitems.json'), 'r') as f:
        item_list = json.load(f)
    item_map = {item['id']: item.get('useitem_id') for item in item_list if item['id'] > 0}
    with open(os.path.join(kcanotify_data_path, 'akashi_data.json'), 'r') as f:
        data_map = json.load(f)
    improve_list = []
    for k, v in data_map.items():
        improve_list.append(Item(k, v, item_map).__dict__())

    print(f'{len(improve_list)} items')

    with open(os.path.join(data_path, 'akashi_schedule.json'), 'w') as f:
        data = {
            "data_version": str(data_version),
            "items": improve_list
        }
        json.dump(data, f, indent=2)
