# The Odyssey of Link | Into the Retro-Verse

A game created for the Summer of GameDev 2023 game jam, inspired by the theme _Retro Remix_. It's a 2D platformer, drawing inspiration from the original Super Mario Bros. game and featuring characters from various retro game classics. The game is built using the JorCademy Engine.

## Table of Contents
- [Game Structure](#game-structure)
- [Dependencies](#dependencies)
- [Running the Application](#running-the-application)
- [Maintenance](#maintenance)
- [Known issues](#known-issues)
- [Contact](#contact)

---

## Game Structure
The game is comprised of the following files and folders. The folders contain classes for game logic and assets. The `main.py` file initiates the game. Detailed descriptions of these files are omitted, as they pertain more to the engine itself than to gameplay development.


```
├── JorCademy-Engine
│   ├── Environment
│   ├── GameObject
│   ├── LICENSE
│   ├── Level
│   ├── Loot
│   ├── Maps
│   ├── Pipfile
│   ├── Pipfile.lock
│   ├── Support
│   ├── UI
│   ├── __pycache__
│   ├── assets
│   ├── events.py
│   ├── game.py
│   ├── jorcademy.py
│   ├── main.py
│   ├── primitives.py
│   └── readme.md
├── readme.md
└── venv
    ├── bin
    ├── include
    ├── lib
    └── pyvenv.cfg
```

## Dependencies
The game relies on the JorCademy Engine, built atop the Pygame and Pygbag libraries. Since these libraries aren't included in the standard Python installation, they must be installed separately using pip. Refer to the [JorCademy Engine's Dependencies section](JorCademy-Engine/readme.md#dependencies) for installation instructions.

## Running the Application
To launch the application locally, use the following terminal command:

```bash
python3 JorCademy-Engine/main.py
```
If this command fails, you can try python `JorCademy-Engine/main.py` or simply `JorCademy-Engine/main.py`, depending on your Python version and operating system.

## Maintenance
This project will be actively maintained until the conclusion of the game jam on 19/08/2023. Afterward, no further updates are expected.

## Credits

### Art
This game uses assets made by the following artists:
- GoldStud: https://www.spriters-resource.com/submitter/GoldStud/
- Mr. C: https://www.spriters-resource.com/submitter/Mr.+C/
- Random Talking Bush: https://www.spriters-resource.com/submitter/Random+Talking+Bush/
- MisterMike: https://www.spriters-resource.com/submitter/MisterMike/
- Nintendo: Many of the above artists' assets are based on Nintendo games, so Nintendo is also credited.

### Music
The game features captivating music composed by the following artists:
- AdhesiveWombat: https://www.youtube.com/watch?v=mRN_T6JkH-c&list=PLwJjxqYuirCLkq42mGw4XKGQlpZSfxsYd
- Density & Time: https://www.youtube.com/watch?v=OuRvOCf9mJ4&list=PLwJjxqYuirCLkq42mGw4XKGQlpZSfxsYd&index=3
- Jeremy Blake: https://www.youtube.com/watch?v=l7SwiFWOQqM&list=PLwJjxqYuirCLkq42mGw4XKGQlpZSfxsYd&index=5
- Jeremy Korpas: https://www.youtube.com/watch?v=fvEdXY_NqNE&list=PLwJjxqYuirCLkq42mGw4XKGQlpZSfxsYd&index=6
- Vibe Mountain: https://www.youtube.com/watch?v=pXdrz1pB35Q&list=PLwJjxqYuirCLkq42mGw4XKGQlpZSfxsYd&index=22
- Karl Casey @ White Bat Audio: https://www.youtube.com/watch?v=wyjb-TcqhwQ

- [ keysofmoonmusic](https://www.youtube.com/c/KeysofMoonMusic)

The final track is promoted by BreakingCopyright:

[ • 💌 Royalty Free Romantic Piano Music -...](https://www.youtube.com/watch?v=3S8CXHs2yyo&t=0s)

## Known issues
The game is currently in the last stage of development. The following issues are known and will be fixed before the game jam deadline:
- Click events are not very responsive. This means that the player must likely click the 
button multiple times to get a response. This is a known issue with the JorCademy Engine, 
and will be fixed in a future update.

## Contact
If you have any questions or feedback, feel free to reach out: nickjordan2002@gmail.com
