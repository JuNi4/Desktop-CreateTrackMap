# Desktop CreateTrackMap

A dekstop port of the web based Minecraft mod [Create Track Map](https://modrinth.com/mod/create-track-map)
It utilises the api of the mod to display the create train network.
If the api is unreachable it will display localy cached track data.

## How to use
Install the requirements with `pip install -r requirements.txt`

Run the create track map with `python main.py`

On the first launch a config.ini will be created. You will need to change the ip addres of the CTM API if the map is not hosted localy

Once you changed the settings, restart the programm and everything should be working