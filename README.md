# WarframeBot
## Overall Description
This is a currently in-progress project that aims to provide information regarding a mechanic in the video game Warframe. The initial premise was to allow users to directly query a Discord bot to find out what relics are needed to find specific items within the game. 

Relics are basically small treasure boxes that can be opened to find various components to build powerful items in the game. They can be opened via short gameplay stints (usually 5-10 minutes each). Players usually have to individually look up which relics are needed for each component - this can get quite annoying to do and keep track of. This bot will allow users to quickly find out what relics they need by requesting full item names (eg. "Trinity Prime Systems") or full item sets (eg. "Trinity Prime). The bot will output a formatted list for each relevant component and their respective relics. This will allow users to quickly query the bot and get desired results by using the Discord in-game overlay for fast access to queries and results. 

The main motivation for this project was to become more familiar with common software development practices like testing and problem solving. I also wanted to get more exposure to NoSQL (MongoDB for JSON documents), creating accurate queries for the database and query testing. Practicing writing clean, well-documented and commented code was also a major motivator. As of 05/03/2023, the bot is currently working in a prototype form. More testing and further refining is required but the proof-of-concept is currently working. 

## Technologies Used
MongoDB PyMongo API
MongoDB Compass
Discord.py API
Python 3.10

## Future Plans
Eventually I want the bot to be able to perform various other utility functions related to the game. One plan is to allow users to ask the bot when a bi-weekly item trader will be coming (or, if he has already arrived, how much longer he will remain and where). It would also be nice to allow users to query items that are not "primed" - some items contain components but cannot be found in relics like "primed" items. This is a long-shot goal - this can get quite complex and would likely require either web scraping or a brand new MongoDB collection or collections made from scratch using the official drop tables. 
