# 2018 FIFA World Cup Russia
## In the following app, you can see the statistics about all national teams and players that participated in the 2018 FIFA World Cup.
### Content
- [Description](#description)
- [Installation](#installation)
- [Usage](#usage)
- [License](#licence)

### Description <a name="description"></a>
#### Thanks to the dataset from [Statsbomb](https://github.com/statsbomb/open-data), I was able to group the data by national teams and players for each team. In the app, you can see statistics grouped by matches, teams, and players. Each section has information that you can see in different types of graphs. 
#### In this project, I used Flask and mostly the Airium library, which allows me to write the logic in Python and then render an HTML file. Additionally, I used the Pygal library, which helped me to embed each different graph into the HTML file thanks to the SVG format. Finally, I used JavaScript and CSS to format the front-end.

### Instalation <a name="installation"></a>
1. Clone this repository to your local machine.
2. Install the dependencies using `pip install -r requirements.txt`.
      - To install the Matplotlib library, for example,  run `pip install Flask`.
      - If a virtual environment has not been created, create one.
3. Run the server with `python app.py`.

### Usage <a name="usage"></a>
1. Open the app.py file.
2. Select the country for which you want to view statistics.
3. Once you have selected a country, you can navigate between the 'match stats', 'team stats', and 'player stats' sections.
4. In the 'match stats' section, you can view the statistics for each match, such as possession, shots, and fouls committed. There are also two graphs accompanying each match.
5. In the 'team stats' section, you can view the overall statistics for each country, as well as a comparison of the 32 teams that participated in the 2018 World Cup in categories such as total goals, average shots on goal per match, goal difference, yellow cards, and clean sheets.
6. In the 'player stats' section, you can select a player from a country to view their statistics, including the positions they played in, minutes played, goals scored, etc. Additionally, there are comparative graphs that show the player's statistics compared to the rest of the players in the same position. On the right side of the screen, you can see if the player is among the top 20 in various categories, such as total shots on goal per 90 minutes, total fouls received, total dribbles, etc.

### License <a name="license"></a>

This project is licensed under the Creative Commons Attribution-NonCommercial 4.0 International (CC BY-NC 4.0) license.

#### What does this mean?

This license allows others to distribute, remix, and build upon your work, as long as they give credit to the original author and do not use it for commercial purposes. This means that you retain the copyright to your work and can decide how it is used. By using this license, you can ensure that your work is shared and used in ways that align with your values.

#### How to use this work

If you want to use this work for non-commercial purposes, you are free to do so as long as you give credit to the original author. If you want to use this work for commercial purposes, you must contact the author to obtain permission.
