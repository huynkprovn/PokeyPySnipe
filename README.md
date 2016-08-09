PokeyPySnipe
============

PokeyPySnipe is a tool which allows you to capture Pokemon at specific coordinates without being soft banned. It works by teleporting to the location of the pokemon, engaging it, teleporting back to your starting position, and then capturing it.

Features
--------

- Snipe Pokemon at specific coordinates
- Only capture Pokemon above a certain CP
- See stats for your trainer, including capture rate and distance walked
- View all your Pokemon, including their IVs and CP level
- Batch release and evolve Pokemon

Requirements
------------

- [Python 2.7](https://www.python.org/downloads/release/python-2712/)


Instructions
------------

- Open Command Prompt/Terminal/equivalent
- Navigate to the root of the PokeyPySnipe directory
- Run ```pip install -r requirements.txt``` 
- Navigate to the ```pogo``` directory
- Edit ```config.ini.example``` with your options and rename to ```config.ini```
- Run ```python snipe.py```
- Open http://127.0.0.1:5100 in your browser

Troubleshooting
---------------
- On Windows, you may need to copy requirements.txt to ```C:/python27/scripts``` to be able to run ```pip install```
- On Windows, you may receive the error ```failed to build xxhash```. If this happens, install the Microsoft Visual C++ Compiler for Python 2.7 from https://www.microsoft.com/en-us/download/details.aspx?id=44266

--------------

Thanks to https://github.com/rubenvereecken/pokemongo-api for providing the API used by PokeyPySnipe, and to all the developers who worked on the Unknown6 solution - PokeyPySnipe uses the encrypt dll/so files from http://pgoapi.com.
