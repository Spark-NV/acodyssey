# Game Tweak Pack - Modular Version

A generic tweak utility for games, originally made by Vahndaar for Assassin's Creed Odyssey, It started as a simpel python script then i decided to add a gui then decided to make it support as many games as i want.
So now it supports multiple games through json files.


## Features

### Configuration-Driven
- **tweaks.json**: All tweak definitions are stored in a JSON file
- **Easy to Add Tweaks**: Simply add new entries to existing JSON files or create new ones.
- **No Code Changes**: Adding new tweaks doesn't require modifying Python code

### GUI
- **Collapsible Sections**: Organized tweak categories

## Usage

Either run the python script or use the compiled exe.

to run the python script, type this into cmd:
   ```
   python main.py
   ```

## Adding New Tweaks

To add a new game, you can manually create a new tweak configuration file in `config/game_tweaks/` following the format of the existing files. Each game configuration includes a `default` flag - set this to `true` for the game you want to be selected by default when the application starts.
or you can you the gui and use the add/edit button, doing this will create the json for you.


## Notice

This definitly has become a universal program for me to start adding all my games that i have multiple different mods/tweaks for. it is probably buggy and should just been made in c but o well.


## 📝 Changelog

### Version 1.0  REMAKE
- Completely remade the gui and functionality supporting multiple games.(Vahndaar tweaks still implemented)

### Version 1.0.2.5
- Changed script to a tkinter GUI based script for ease of use.
- Added infinite breathing underwater.
- Added infinite boat rowe stamina.

### Version 1.0.2.4
- Added Steam executable finding logic, tool will now find odyssey when installed with steam automatically.
  
### Version 1.0.2.3
- Fixed loot drop tweak functionality
- Improved file entry system - now only requires path input if auto-detection fails ie: dont have to give c:path/ACOdyssey.exe you can just give c:path/ and it will find the exe within that path.



## License

Educational/Personal Use Only

## Credits

Vahndaar: https://next.nexusmods.com/profile/vahndaar
Original: https://www.nexusmods.com/assassinscreedodyssey/mods/12