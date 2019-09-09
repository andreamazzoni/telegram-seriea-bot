from datetime import datetime
from dateutil import tz
from cache import Cache
from team import Team


class FootballData:

    def __init__(self, hostname, token):
        self.cache = Cache(3600)
        self.base_url = hostname + '/v2/'
        self.headers = {'X-Auth-Token': token}
        self.competition = 'competitions/SA'

    def load_tla(self):
        resp = self.get_data(self.competition + "/teams")
        teams = resp.json()['teams']
        self.tla = dict()
        for team in teams:
            self.tla[team['name']] = team['tla']

    def get_data(self, resource):
        return self.cache.get_content(self.base_url + resource, self.headers)

    def get_data_from_url(self, resource):
        return self.cache.get_content(resource, self.headers)

    def get_teamname(self, teamname):
        return Team.get_name(teamname)

    def get_longteamname(self, teamname):
        return Team.get_longname(teamname)

    def get_matchday(self):
        resp = self.get_data(self.competition)
        return resp.json()['currentSeason']['currentMatchday']

    def ranking(self, matchday):
        if matchday == 0:
            matchday = self.get_matchday()

        resp = self.get_data(
            self.competition + '/standings?matchday=' + str(matchday))
        ranking = resp.json()['standings'][0]['table']

        ret = '*Ranking (Matchday ' + str(matchday) + ')*\n'
        ret += '`'

        self.load_tla()

        for i in range(0, 20):
            ret += str(i + 1).ljust(2) + ' ' + \
                self.tla[ranking[i]['team']['name']]
            ret += ' ' + str(ranking[i]['points'])
            ret += ' [' + str(ranking[i]['goalsFor']) + '|' + \
                str(ranking[i]['goalsAgainst']) + '|'
            ret += str(ranking[i]['goalDifference']) + ']' + '\n'
        ret += '`'
        return ret

    def matchday(self):
        matchday = self.get_matchday()

        resp = self.get_data(self.competition +
                             '/matches?matchday=' + str(matchday))
        matches = resp.json()['matches']

        date = datetime.strptime(
            matches[0]['utcDate'], '%Y-%m-%dT%H:%M:%SZ')
        ret = '*Matchday ' + \
            str(matches[0]['matchday']) + ':* _' + \
            date.strftime('%d/%m/%Y') + '_\n'

        self.load_tla()

        for match in matches:

            hometeam = self.tla[match['homeTeam']['name']]
            awayteam = self.tla[match['awayTeam']['name']]

            ret += '`' + hometeam + ' - ' + awayteam + ' '

            score_home = str(match['score']['fullTime']['homeTeam'])
            if score_home == 'None':
                score_home = str(0)

            score_away = str(match['score']['fullTime']['awayTeam'])
            if score_away == 'None':
                score_away = str(0)

            ret += score_home + '-' + score_away

            if match['status'] in ('FINISHED'):
                ret += '`\n'

            if match['status'] in ('IN_PLAY', 'PAUSED'):
                ret += '`  Live!\n'

            if match['status'] in ('TIMED', 'SCHEDULED'):
                utc = datetime.strptime(match['utcDate'], '%Y-%m-%dT%H:%M:%SZ')
                from_zone = tz.gettz('UTC')
                to_zone = tz.gettz('Europe/Rome')
                utc = utc.replace(tzinfo=from_zone)
                date = utc.astimezone(to_zone)

                # date = datetime.datetime.strptime(match['utcDate'], '%Y-%m-%dT%H:%M:%SZ')
                # date += datetime.timedelta(hours=2)
                stringdate = date.strftime('%a') + ' ' + date.strftime('%H:%M') + ' '
                ret += ' ' + stringdate + '`\n'

            if match['status'] in ('POSTPONED'):
                ret += ' Postponed`\n'

            if match['status'] in ('CANCELED'):
                ret += ' Canceled`\n'

        return ret

    def matchday_cl(self):
        self.competition = 'competitions/CL'
        return self.matchday()

    def matchday_sa(self):
        self.competition = 'competitions/SA'
        return self.matchday()

    def players(self, teamName):
        resp = self.get_data(self.competition + '/teams')
        count = resp.json()['count']
        teams = resp.json()['teams']
        ret = ''
        for i in range(0, count):
            teamname = self.get_longteamname(teams[i]['name'])
            if teamname.lower() == teamName.lower():
                team_id = teams[i]['id']
                ret = '*' + teamname + ' players:* \n'
        if ret != '':
            resp = self.get_data('/teams/' + str(team_id))
            players = resp.json()['squad']
            for player in players:
                player_name = player['name']
                player_number = str(player['shirtNumber'])
                if player_number == 'None':
                    player_number = '-'
                ret += '`' + player_number.ljust(2) + ' ' + player_name + '`\n'
        else:
            ret = 'Wrong team name'
        return ret

    def player(self, teamName, playerNumber):
        resp = self.get_data(self.competition + '/teams')
        teams = resp.json()['teams']

        team_id = None
        for team in teams:
            teamname = self.get_longteamname(team['name'])
            if teamname.lower() == teamName.lower():
                team_id = team['id']

        if team_id is None:
            return 'Wrong team name'

        resp = self.get_data('/teams/' + str(team_id))
        players = resp.json()['squad']

        ret = ''
        for player in players:
            shirtNumber = player['shirtNumber']
            if str(shirtNumber) == str(playerNumber):
                ret = '*' + player['name'] + '*\n'
                ret += '`Position: ' + player['position'] + '`\n'
                ret += '`Number: ' + str(shirtNumber) + '`\n'
                ret += '`Birth date: ' + player['dateOfBirth'] + '`\n'
                ret += '`Nationality: ' + player['nationality'] + '`\n'

        if ret == '':
            ret = 'Wrong player number'

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
