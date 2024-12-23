import json
import logging
import os
from datetime import datetime

from script import ROOT_PATH
from script import akashi_schedule
from script import setup_logging
from script.l10n import Localization
from script.shiptag import ShipTagManager

if __name__ == '__main__':
    log_level = os.environ.get('LOG_LEVEL', 'INFO')
    setup_logging(level=getattr(logging, log_level))
    logger = logging.getLogger(__name__)

    data_version = datetime.strftime(datetime.utcnow(), '%Y%m%d%H')
    logger.info(f"Data version: {data_version}")
    logger.info("Starting data update process")

    l10n = Localization(data_version)
    l10n.update_equipment_type_l10n()
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

    logger.info('Finished processing')
