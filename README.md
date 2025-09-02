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


You have a few options to run this, depending on your preference.

---

### Option 1: Run from Source (Python required)

This option is for users who have Python installed and want to run the script directly.

1.  **Download:**
    *   Navigate to the `source/` directory in the repository.
    *   Download the `main.py` file and all other folders within the `source` directory.
    *   Or clone the repository to get all files at once.
2.  **Run:**
    *   Open your command line or terminal.
    *   Navigate to the directory where you saved the files.
    *   Execute the script by typing:
        ```
        python main.py
        ```

---

### Option 2: Use the Portable Executable

This is a single file that can be run without any installation or dependencies.

1.  **Download:**
    *   Navigate to the `exe/` directory.
    *   Download the `portable main.exe` file.
2.  **Run:**
    *   Simply double-click the downloaded `main.exe` file to run it.
    *   **Note:** Windows Defender may flag this file as a potential threat. This is a false positive that occurs because the application needs to extract its libraries into a temporary location at runtime, a behavior that can be mistaken for malicious activity.

---

### Option 3: Use the Standard Executable

This version is much less likely to trigger antivirus warnings but requires keeping two items together.

1.  **Download:**
    *   Navigate to the `exe/` directory.
    *   Download the `main.zip` file.
2.  **Run:**
    *   Extract the entire contents of `main.zip` into a folder.
    *   Ensure the `main.exe` file and the `_internal` folder are kept in the same directory.
    *   Double-click `main.exe` to start the program.


## Adding New Tweaks

To add a new game, you can manually create a new tweak configuration file in `config/game_tweaks/` following the format of the existing files. Each game configuration includes a `default` flag - set this to `true` for the game you want to be selected by default when the application starts.
or you can you the gui and use the add/edit button, doing this will create the json for you.


## Notice

This definitly has become a universal program for me to start adding all my games that i have multiple different mods/tweaks for. it is probably buggy and should just been made in c but o well.

It should also be said the portable exe gets detected by some as a trojen, this is due to the nature of the way the exe is compiled.

If your scared to run the exe your free to get the python files in the source directory, look over them and run it that way, or compile the python files yourself into an exe using this command:
pyinstaller --onefile main.py

or as stated in usage, you can get the zip and extract it and run the exe in it as it wasnt compiled into a single exe it wont get flagged.


## 📝 Changelog

### Version 1.0  REMAKE
- Completely remade the gui and functionality supporting multiple games.(Vahndaar tweaks still implemented)


---


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
