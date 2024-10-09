import configparser
from pathlib import Path

config_file = Path(__file__).parent / "config.ini"

Config = configparser.ConfigParser()

Config.read(config_file)

def get_config(section: str):
    return Config[section]

if __name__ == "__main__":
    # iterate over all sections
    for section in Config.sections():
        print(section)
        for key, value in Config.items(section):
            print(f"{key} = {value}")