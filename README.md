# System Upgrade Tool (sut)
Simple utility to upgrade all system packages from all package managers at once.

# Usage
``` bash
sudo sut
```
No args required. All configurations are on config file.

# Instalation
```bash
git clone https://github.com/BrenoMartinsDeOliveiraVasconcelos/SysUpgrader.git
cd SysUpgrader
sudo chmod +x install.sh
sudo bash ./install.sh
```
For updating, just rerun the script. It will not replace current config file.

# Configuration
The configuration file is stored at `/etc/sysupgrader/config.json`

Following `json` syntax, to add or edit an entry the user must format it like stated bellow.

```json
{
    "package_manager" : {
        "path": "/path/to/binary/file",
        "commands": ["first execution args", "second execution args", "..."]
    }
}
```

**Warning: Make sure that only users allowed to run as root can edit the config file. The script can be DANGEROUS if misused.**
