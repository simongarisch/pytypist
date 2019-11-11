import os
from configparser import ConfigParser


config = ConfigParser()
config.read(
    os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "db_settings.ini"
    )
)
