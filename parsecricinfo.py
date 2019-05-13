import os
from selenium import webdriver
from bs4 import BeautifulSoup


class cricinfo:
    def __init__(self):
        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--ignore-certificate-errors')
        self.options.add_argument('--incognito')
        self.options.add_argument('--headless')
        self.chrome_loc = os.path.join(r'C:\Users\gpanwar2\webdriver','chromedriver.exe')
        self.before = None
        self.topevent = dict()
        self.__menu__()

    def __menu__(self):
        os.system('cls')
        print ('*'*100)
        print ('Option    ', 'DESCRIPTION')
        print ('-'*100)
        print ('1         ', 'get top event')
        print ('0         ', 'exit')
        print ('*'*100)
        self.topevent = dict()
        choice = input('select you choice: ')
        if choice == '1':
            self.get_topevent()
        

    def get_topevent(self):
        driver = webdriver.Chrome(self.chrome_loc,chrome_options=self.options)
        driver.get('http://www.espncricinfo.com/')
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        driver.close()
        top_event_score = soup.find_all(class_='scoreboard')
        os.system('cls')
        print ('*'*100)
        print ('OPTION    ','STATUS         ','TEAMS               ', 'DESCRIPTION')
        print ('-'*100)
        i = 1
        for top in top_event_score:            
            series = top.find_all(class_='scoreLabel')[0].get('data-id')
            match = top.find_all(class_='cscore')[0].get('data-id')
            teams = top.find_all(class_='cscore_name--abbrev')[0].text + ' vs ' + top.find_all(class_='cscore_name--abbrev')[1].text
            teams = str(teams)+' '*(20-len(str(teams)))
            status = top.find_all(class_='cscore_date-time')[0].text.replace('\n','')
            status = status.replace(' ','')
            status = str(status)+' '*(15-len(str(status)))
            description = top.find_all(class_='cscore_info-overview')[0].text
            description = description.replace('\n','').strip()
            sno = str(i)+' '*(10-len(str(i)))
            self.topevent[i] = [series, match, status, teams, description]
            print (sno, status, teams, description)
            i += 1
        print ('*'*100)
        choice = input('select you choice: ')
        try:
            series = self.topevent[int(choice)][0]
            match = self.topevent[int(choice)][1]
            description = self.topevent[int(choice)][4]
        except:
            print ('wrong choice')
        else:
            status = self.topevent[int(choice)][2]
            if 'AM' in status or 'PM' in status:
                print ('match will start at ', status)
                return
            self.get_match(series, match, description)

    def get_match(self, series, match, description):
        driver = webdriver.Chrome(self.chrome_loc,chrome_options=self.options)
        driver.get('http://www.espncricinfo.com/series/'+series+'/scorecard/'+match)
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')
        driver.close()
        os.system('cls')
        get_match_summary = soup.find_all(class_='gameHeader')
        print ('*'*100)
        print('-'*100)
        for summary in get_match_summary:
            match_desc = summary.find_all(class_='cscore_info-overview')
            print(description)
            print('-'*43 + 'S U M M A R Y' + '-'*44)
            if description == match_desc[0].text.strip():
                teams_name = summary.find_all(class_='cscore_name--long')
                team_score = summary.find_all(class_='cscore_score')
                current_match = summary
                team1, team2 = teams_name[0].text, teams_name[1].text
                team1 = str(team1)+' '*(20-len(str(team1)))
                team2 = str(team2)+' '*(20-len(str(team2)))
                team1_score = team_score[0].text
                team2_score = team_score[1].text
                game_summary = summary.find_all(class_='cscore_notes_game')
                print(team1, team1_score)
                print(team2, team2_score)
                print(game_summary)
                print('-'*100)
                print('-'*41 + 'S C O R E C A R D' + '-'*42)
                scorecard = current_match.parent.find_all(class_='layout-bc')
                scorecard = scorecard[0].find_all(class_='col-b')
                scorecard = scorecard[0].find_all('article')
                team1_scoreboard = scorecard[0]
                team2_scoreboard = scorecard[1]
                self.__get_scoreboard__(team1_scoreboard)
                print('-'*100)
                print('-'*100)
                self.__get_scoreboard__(team2_scoreboard)
                break
        print('-'*100)
        print ('*'*100)

    def __get_scoreboard__(self,obj):
        header = obj.find_all(class_='accordion-header')
        print(header[0].text)
        print('-'*100)
        batsman_section = obj.find_all(class_='scorecard-section batsmen')
        batsman_header = batsman_section[0].find_all(class_='wrap header')
        print(self.__print_batsmanscore__(batsman_header[0]))
        print('-'*100)
        batsman_header = batsman_section[0].find_all(class_='wrap batsmen')
        for b in batsman_header:
            print(self.__print_batsmanscore__(b))

        extras = batsman_section[0].find_all(class_='wrap extras')
        extras = extras[0].find_all(class_='cell')
        extras = extras[0].text + ' '*60 + extras[1].text
        print(extras)
        print('-'*100)
        extras = batsman_section[0].find_all(class_='wrap total')
        extras = extras[0].find_all(class_='cell')
        extras = extras[0].text + ' '*60 + extras[1].text
        print(extras)
        bowler_heading = 'BOWLING' + ' '*35
        bowler_heading += 'O     ' + 'M     ' + 'R     ' + 'W     ' + 'ECON  '
        print('-'*100)
        print(bowler_heading)
        bowler_section = obj.find_all(class_='scorecard-section bowling')
        bowler = bowler_section[0].find_all('tbody')
        bowler = bowler[0].find_all('tr')
        print('-'*100)
        for b in bowler:
            print(self.__print_bowlerscore__(b))

    def __print_batsmanscore__(self,obj):
        headers = obj.find_all(class_='cell batsmen')[0].text
        heading = str(headers)+' '*(20-len(str(headers)))
        commentary = obj.find_all(class_='cell commentary')[0].text
        commentary = str(commentary)+' '*(50-len(str(commentary)))
        heading += commentary
        runs = obj.find_all(class_='cell runs')
        for run in runs:
            r = str(run.text)+' '*(5-len(str(run.text)))
            heading += r
        return heading

    def __print_bowlerscore__(self,obj):
        details = obj.find_all('td')
        rtn = ''
        rtn += str(details[0].text)+' '*(42-len(str(details[0].text)))
        rtn += str(details[2].text)+' '*(6-len(str(details[2].text)))
        rtn += str(details[3].text)+' '*(6-len(str(details[3].text)))
        rtn += str(details[4].text)+' '*(6-len(str(details[4].text)))
        rtn += str(details[5].text)+' '*(6-len(str(details[5].text)))
        rtn += str(details[6].text)+' '*(6-len(str(details[6].text)))
        return rtn               
        
        

def main():
    myObj = cricinfo()

    
if __name__ == "__main__":
    main()
