import requests
from bs4 import BeautifulSoup
from datetime import datetime

from src.models.match import Match


class FixtureProccessor:
    def __init__(self) -> None:
        pass
    
    def scrape(self):
        url = "https://www.skysports.com/manchester-city-fixtures"

        response = requests.get(url)        
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        fixtures_body = soup.find(name='div', class_='fixres__body')
        days = fixtures_body.find_all(name='h4', class_='fixres__header2')
        match_titles = fixtures_body.find_all(name='h5',class_= 'fixres__header3')
        matches = fixtures_body.find_all(name='div',class_= 'fixres__item')


        #ensure that the lists have equal lengths
        #TODO:
        games = []

        for i in range(0,matches.__len__()):
            
            #extract the opponent for each match
            opponent_item = matches[i].find(name='span' ,class_='matches__item-col matches__participant matches__participant--side2')
            opponent_span = opponent_item.find(name='span', class_='swap-text__target')
            opponent = opponent_span.text

            if opponent != 'Manchester City':
                #Extract times
                time_span_parent = matches[i].find(name='span' ,class_='matches__item-col matches__status')
                time_span = time_span_parent.find(name='span' ,class_='matches__date')

                time = time_span.text

                match_dic = {
                    "match":match_titles[i].text.strip(),
                    "date": days[i].text.strip(),
                    "time": time.strip(),
                    "opponent": opponent.strip()
                }

                games.append(match_dic)

        return games

    def deserialize_fixtures(self,games):
        matches = []
        for game in games:
            date_str = game['date']+ ' ' + game['time']
            date = self.fix_date(dt=date_str)
            match = Match(opponent=game['opponent'],date_time= date, league= game['match'])
            matches.append(match)
        return matches
    
    def fix_date(self, dt: str):
        if dt.count('th') > 0:
            new_dt = dt.replace('th','')
            return datetime.strptime(new_dt, '%A %d %B %H:%M')
        elif dt.count('rd')  > 0:
            new_dt = dt.replace('rd','')
            return datetime.strptime(new_dt, '%A %d %B %H:%M')
        elif dt.count('nd')  > 0:
            new_dt = dt.replace('nd','')
            return datetime.strptime(new_dt, '%A %d %B %H:%M')
        elif dt.count('st')  > 0:
            new_dt = dt.replace('st','')
            return datetime.strptime(new_dt, '%A %d %B %H:%M')

    def addNotionEvents(self, matches):
        for m in matches:
            print(m.opponent)

    def procces_fixtures(self):
        games = self.scrape()
        deserialized_games =self.deserialize_fixtures(games)
        self.addNotionEvents(deserialized_games)