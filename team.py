
class Team:

    photo = {'Fiorentina': 'http://www.legaseriea.it/uploads/default'
                           '/attachments/squadre/squadre_m/15/images/logo'
                           '/510/original/fiorentina-2018.png',
             'Inter': 'http://www.legaseriea.it/uploads/default'
                      '/attachments/squadre/squadre_m/8/images/logo'
                      '/28/original/inter.png',
             'Lazio': 'http://www.legaseriea.it/uploads/default'
                      '/attachments/squadre/squadre_m/14/images/logo'
                      '/30/original/lazio.png',
             'Roma': 'http://www.legaseriea.it/uploads/default'
                     '/attachments/squadre/squadre_m/20/images/logo'
                     '/486/original/roma-400.png',
             'Torino': 'http://www.legaseriea.it/uploads/default'
                       '/attachments/squadre/squadre_m/17/images/logo'
                       '/37/original/torino.png',
             'Napoli': 'http://www.legaseriea.it/uploads/default'
                       '/attachments/squadre/squadre_m/12/images/logo'
                       '/32/original/napoli.png',
             'Chievo': 'http://www.legaseriea.it/uploads/default'
                       '/attachments/squadre/squadre_m/16/images/logo'
                       '/464/original/chievo.png',
             'Sassuolo': 'http://www.legaseriea.it/uploads/default'
                         '/attachments/squadre/squadre_m/18/images/logo'
                         '/36/original/sassuolo.png',
             'Sampdoria': 'http://www.legaseriea.it/uploads/default'
                          '/attachments/squadre/squadre_m/10/images/logo'
                          '/227/original/sampdoria.png',
             'Atalanta': 'http://www.legaseriea.it/uploads/default'
                         '/attachments/squadre/squadre_m/3/images/logo'
                         '/20/original/atalanta.png',
             'Milan': 'http://www.legaseriea.it/uploads/default'
                      '/attachments/squadre/squadre_m/9/images/logo'
                      '/164/original/milan.png',
             'Juventus': 'http://www.legaseriea.it/uploads/default'
                         '/attachments/squadre/squadre_m/1/images/logo'
                         '/489/original/juventus400.png',
             'Udinese': 'http://www.legaseriea.it/uploads/default'
                        '/attachments/squadre/squadre_m/22/images/logo'
                        '/38/original/udinese.png',
             'Genoa': 'http://www.legaseriea.it/uploads/default'
                      '/attachments/squadre/squadre_m/21/images/logo'
                      '/27/original/genoa.png',
             'Verona': 'http://www.legaseriea.it/uploads/default'
                       '/attachments/squadre/squadre_m/19/images/logo'
                       '/477/original/hellas400.png',
             'Bologna': 'http://www.legaseriea.it/uploads/default'
                        '/attachments/squadre/squadre_m/6/images/logo'
                        '/21/original/bologna.png',
             'Cagliari': 'http://www.legaseriea.it/uploads/default'
                         '/attachments/squadre/squadre_m/28/images/logo'
                         '/223/original/cagliari_bg.png',
             'Crotone': 'http://www.legaseriea.it/uploads/default'
                        '/attachments/squadre/squadre_m/39/images/logo'
                        '/91/original/crotone.png',
             'SPAL': 'http://www.legaseriea.it/uploads/default'
                     '/attachments/squadre/squadre_m/75/images/logo'
                     '/471/original/spal400.png',
             'Benevento': 'http://www.legaseriea.it/uploads/default'
                          '/attachments/squadre/squadre_m/86/images/logo'
                          '/474/original/benevento400.png'}

    short_name = {'ACF Fiorentina': 'Fio',
                  'FC Internazionale Milano': 'Int',
                  'SS Lazio': 'Laz',
                  'AS Roma': 'Rom',
                  'Torino FC': 'Tor',
                  'SSC Napoli': 'Nap',
                  'AC Chievo Verona': 'Chi',
                  'US Sassuolo Calcio': 'Sas',
                  'UC Sampdoria': 'Sam',
                  'Atalanta BC': 'Ata',
                  'AC Milan': 'Mil',
                  'Juventus FC': 'Juv',
                  'Udinese Calcio': 'Udi',
                  'Genoa CFC': 'Gen',
                  'Hellas Verona FC': 'Ver',
                  'Bologna FC 1909': 'Bol',
                  'Cagliari Calcio': 'Cag',
                  'FC Crotone': 'Cro',
                  'SPAL 2013': 'SPA',
                  'Benevento Calcio': 'Ben',
                  'Frosinone Calcio': 'Fro',
                  'Empoli FC': 'Emp',
                  'Parma Calcio 1913': 'Par'}

    long_name = {'ACF Fiorentina': 'Fiorentina',
                 'FC Internazionale Milano': 'Inter',
                 'SS Lazio': 'Lazio',
                 'AS Roma': 'Roma',
                 'Torino FC': 'Torino',
                 'SSC Napoli': 'Napoli',
                 'AC Chievo Verona': 'Chievo',
                 'US Sassuolo Calcio': 'Sassuolo',
                 'UC Sampdoria': 'Sampdoria',
                 'Atalanta BC': 'Atalanta',
                 'AC Milan': 'Milan',
                 'Juventus FC': 'Juventus',
                 'Udinese Calcio': 'Udinese',
                 'Genoa CFC': 'Genoa',
                 'Hellas Verona FC': 'Verona',
                 'Bologna FC 1909': 'Bologna',
                 'Cagliari Calcio': 'Cagliari',
                 'FC Crotone': 'Crotone',
                 'SPAL 2013': 'SPAL',
                 'Benevento Calcio': 'Benevento',
                 'Frosinone Calcio': 'Frosinone',
                 'Empoli FC': 'Empoli',
                 'Parma Calcio 1913': 'Parma'}

    @staticmethod
    def get_name(teamname):
        if teamname in Team.short_name:
            return Team.short_name[teamname].upper()
        else:
            return teamname

    @staticmethod
    def get_longname(teamname):
        if teamname in Team.long_name:
            return Team.long_name[teamname]
        else:
            return teamname

    @staticmethod
    def get_photourl(teamname):
        if teamname in Team.photo:
            return Team.photo[teamname]
        else:
            return teamname
