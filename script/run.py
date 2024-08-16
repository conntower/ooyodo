import json
import os
import datetime

from script import ROOT_PATH
from script import akashi_schedule
from script.l10n import Localization
from script.shiptag import ShipTagManager

if __name__ == '__main__':
    data_version = datetime.datetime.strftime(datetime.datetime.now(datetime.UTC), '%Y%m%d%H')
    print(data_version)

    l10n = Localization(data_version)
    l10n.update_item_l10n()
    l10n.update_useitem_in_improve_l10n()

    akashi_schedule.update_schedule(data_version)

    ship_tag = ShipTagManager(data_version)
    ship_tag.update_tags()

    data_version_path = os.path.join(ROOT_PATH, 'data', 'version.json')

    with open(data_version_path, 'w') as f:
        version_json = {
            "version": data_version
        }

        f.write(json.dumps(version_json))

    print('finish')
