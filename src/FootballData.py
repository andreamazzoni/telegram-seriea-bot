import datetime
from Cache import Cache
from Team import Team


class FootballData:

    competition = 'competitions/456'
    token = 'bfd9185cc48048a9b4bbb8f6ac67e905'
    headers = {'X-Auth-Token': token}

    def __init__(self, hostname):
        self.cache = Cache(3600)
        self.team = Team()
        self.base_url = hostname + '/v1/'

    def get_data(self, resource):
        return self.cache.get_content(self.base_url + resource, self.headers)

    def get_data_from_url(self, resource):
        return self.cache.get_content(resource, self.headers)

    def get_teamname(self, teamname):
        return self.team.get_name(teamname)

    def get_longteamname(self, teamname):
        return self.team.get_longname(teamname)

    def get_matchday(self):
        resp = self.get_data(self.competition)
        return resp.json()['currentMatchday']

    def ranking(self, matchday):
        if matchday == 0:
            matchday = self.get_matchday()

        resp = self.get_data(
            self.competition + '/leagueTable?matchday=' + str(matchday))
        ranking = resp.json()['standing']
        ret = '*Ranking (Matchday ' + str(matchday) + ')*\n'
        ret += '`'
        for i in range(0, 20):
            ret += str(i + 1).ljust(2) + ' ' + \
                self.get_teamname(ranking[i]['teamName']).ljust(4)
            ret += ' ' + str(ranking[i]['points'])
            ret += ' [' + str(ranking[i]['goals']) + '|' + \
                str(ranking[i]['goalsAgainst']) + '|'
            ret += str(ranking[i]['goalDifference']) + ']' + '\n'
        ret += '`'
        return ret

    def matchday(self, matchday):
        if matchday == 0:
            matchday = self.get_matchday()
        else:
            matchday = matchday

        resp = self.get_data(self.competition +
                             '/fixtures?matchday=' + str(matchday))
        fixtures = resp.json()['fixtures']
        count = resp.json()['count']

        if count == 0:
            return 'Matchday out of range'

        date = datetime.datetime.strptime(
            fixtures[0]['date'], '%Y-%m-%dT%H:%M:%SZ')
        ret = '*Matchday ' + \
            str(fixtures[0]['matchday']) + ':* _' + \
            date.strftime('%d/%m/%Y') + '_\n'
        for i in range(0, count):

            homeTeam = self.get_teamname(fixtures[i]['homeTeamName'])
            awayTeam = self.get_teamname(fixtures[i]['awayTeamName'])

            ret += '`' + homeTeam + ' - ' + awayTeam + ' '

            if fixtures[i]['status'] in ('IN_PLAY', 'FINISHED'):
                ret += str(fixtures[i]['result']['goalsHomeTeam']) + '-' + \
                    str(fixtures[i]['result']['goalsAwayTeam']) + '`\n'

            if fixtures[i]['status'] in ('TIMED', 'SCHEDULED'):
                date = datetime.datetime.strptime(
                    fixtures[i]['date'], '%Y-%m-%dT%H:%M:%SZ')
                date += datetime.timedelta(hours=1)
                stringdate = date.strftime(
                    '%a') + ' ' + date.strftime('%H:%M') + ' '
                ret += stringdate + '`\n'

            if fixtures[i]['status'] in ('POSTPONED'):
                ret += ' Postponed`\n'

            if fixtures[i]['status'] in ('CANCELED'):
                ret += ' Canceled`\n'

        return ret

    def players(self, teamName):
        resp = self.get_data(self.competition + '/teams')
        count = resp.json()['count']
        teams = resp.json()['teams']
        ret = ''
        for i in range(0, count):
            teamname = self.get_longteamname(teams[i]['name'])
            if teamname.lower() == teamName.lower():
                players_url = teams[i]['_links']['players']['href']
                ret = '*' + teamname + ' players:* \n'
        if ret != '':
            resp = self.get_data_from_url(players_url)
            count = resp.json()['count']
            players = resp.json()['players']
            for j in range(0, count):
                player_name = players[j]['name']
                player_number = str(players[j]['jerseyNumber'])
                if player_number == 'None':
                    player_number = '-'
                ret += '`' + player_number.ljust(2) + ' ' + player_name + '`\n'
        else:
            ret = 'Wrong team name'
        return ret

    def player(self, teamName, playerNumber):
        resp = self.get_data(self.competition + '/teams')
        count = resp.json()['count']
        teams = resp.json()['teams']

        players_url = ''
        for i in range(0, count):
            teamname = self.get_longteamname(teams[i]['name'])
            if teamname.lower() == teamName.lower():
                players_url = teams[i]['_links']['players']['href']

        if players_url != '':
            resp = self.get_data_from_url(players_url)
            count = resp.json()['count']
            players = resp.json()['players']

            ret = ''
            for j in range(0, count):
                if str(players[j]['jerseyNumber']) == playerNumber:
                    ret = '*' + players[j]['name'] + '*\n'
                    ret += '`Position: ' + players[j]['position'] + '`\n'
                    ret += '`Number: ' + \
                        str(players[j]['jerseyNumber']) + '`\n'
                    ret += '`Birth date: ' + players[j]['dateOfBirth'] + '`\n'
                    ret += '`Nationality: ' + players[j]['nationality'] + '`\n'
                    ret += '`Contract until: ' + \
                        players[j]['contractUntil'] + '`\n'

            if ret == '':
                ret = 'Wrong player number'

        else:
            ret = 'Wrong team name'
        return ret

    # Not exposed commands
    def leader(self):
        resp = self.get_data(self.competition + '/leagueTable')
        ranking = resp.json()['standing']
        ret = self.photo[self.team2[ranking[0]['teamName']]]
        return ret

    def pic(self, teamName):
        for key, value in self.photo.items():
            if key.lower() == teamName.lower():
                return self.photo[key]
        ret = 'Wrong team name'
        return ret
