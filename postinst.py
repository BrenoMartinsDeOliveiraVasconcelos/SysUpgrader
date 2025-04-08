#!/usr/bin/env python3

import json

config_path = "/etc/sysupgrader/config.json"

# Puts entries on config.json that are missing from the default
def set_config_missing():
    defaults = json.load(open("./config.json"))
    config = json.load(open(config_path))

    for k, v in defaults.items():
       # Ignore if first level is not prsent
       if k not in config:
           pass
       else:
           # If it's present, then add missing entries
           for k2, v2 in v.items():
               if k2 not in config[k]:
                   config[k][k2] = v2

    with open(config_path, "w") as f:
        json.dump(config, f, indent=4)


def main():
    try:
        print("System Upgrade Tool - Post-install utility")
        set_config_missing()
        print("Post install completed.")
        exit(0)
    except FileNotFoundError:
        print("Run install.sh to install sysupgrader and generate default config.")
        exit(1)


if __name__ == "__main__":
    main()
