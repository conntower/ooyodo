import os.path

from script import *
import json


def data_reformat(id, data, use_item_map):
    res = {"id": int(id)}
    for k, v in data.items():
        if k == 'improvement':
            res[k] = []
            for i in v:
                upgrade = i['upgrade']
                req = i['req']
                resource = i['resource']
                req_item = i.get('require_item', None)

                improve = {
                    "req": [{
                        "ship": item[1] if isinstance(item[1], list) else [],
                        "day": day_stringify(item[0])
                    } for item in req],
                    "resource": resource_reformat(resource, req_item, use_item_map),
                }
                if upgrade:
                    improve["upgrade"] = {"id": upgrade[0], "lv": upgrade[1]}

                res[k].append(improve)
    return res


def resource_reformat(data_list, req_item, use_item_map):
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
        res["extra"][2]["use"] = {str(use_item_map[item[0]]): item[1] for item in req_item}
    return res


def day_stringify(day):
    """
    [true, true, true, true, true, true, true] -> 1111111
    """
    return "".join([str(int(i)) for i in day])


if __name__ == '__main__':
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
        improve_list.append(data_reformat(k, v, item_map))
    with open(os.path.join(data_path, 'akashi_schedule.json'), 'w') as f:
        data = {
            "data_version": str(DATA_VERSION),
            "items": improve_list
        }
        json.dump(data, f, indent=2)