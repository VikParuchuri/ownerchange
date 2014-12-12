import requests
import bs4
import os
import time
import logging
import sys
import traceback
import settings
log = logging.getLogger(__name__)

class TeamInfo(object):
    def __init__(self, team):
        self.team = team
        self.team_name = settings.teams[team]
        self.exec_url = "http://www.pro-football-reference.com/teams/{0}/executives.htm".format(team)
        self.record_url = "http://www.pro-football-reference.com/teams/{0}/".format(team)

    def get_record_data(self):
        resp = requests.get(self.record_url)
        html = resp.content
        soup = bs4.BeautifulSoup(html)
        stats_table = [str(e) for e in list(soup.select("#team_index tr"))]
        all_rows = []
        for tr in stats_table:
            try:
                s = bs4.BeautifulSoup(tr)
                tds = [str(e) for e in list(s.select("td"))]
                if len(tds) != 28:
                    continue
                row = [self.team]
                row.append(bs4.BeautifulSoup(tds[0]).select("a")[0].get_text())

                for item in [3,4,5,7,8,9]:
                    row.append(bs4.BeautifulSoup(tds[item]).get_text())

                for item in [10,12,13,14]:
                    row.append(bs4.BeautifulSoup(tds[item]).select("a")[0]["title"])
                    row.append(bs4.BeautifulSoup(tds[item]).select("a")[0]["href"])

                for td in tds[15:]:
                    row.append(bs4.BeautifulSoup(td).get_text())

                all_rows.append(row)
            except Exception:
                print "Error parsing record data"
                traceback.print_exc()

        self.record_data = all_rows

    def parse_exec_table(self, table):
        all_rows = {}
        final_rows = []
        for tr in table:
            try:
                s = bs4.BeautifulSoup(tr)
                tds = [str(e) for e in list(s.select("td"))]
                if len(tds) != 5:
                    continue
                exec_name = bs4.BeautifulSoup(tds[0]).select("a")[0].get_text()
                exec_link = bs4.BeautifulSoup(tds[0]).select("a")[0]["href"]
                start_year = bs4.BeautifulSoup(tds[2]).get_text()
                end_year = bs4.BeautifulSoup(tds[3]).get_text()
                title = bs4.BeautifulSoup(tds[4]).get_text()

                for i in xrange(int(start_year),(int(end_year) + 1)):
                    year = str(i)
                    if year in all_rows:
                        continue

                    row = [year, exec_name, exec_link, title]
                    all_rows[year] = row
            except Exception:
                print "Error parsing exec table"
                traceback.print_exc()

        for year in sorted(all_rows.keys()):
            final_rows.append(all_rows[year])
        return final_rows

    def get_exec_data(self):
        resp = requests.get(self.exec_url)
        html = resp.content
        soup = bs4.BeautifulSoup(html)
        exec_table = [str(e) for e in list(soup.select("#executives tr"))]
        owner_table = [str(e) for e in list(soup.select("#owners tr"))]

        self.owner_data = self.parse_exec_table(owner_table)
        self.exec_data = self.parse_exec_table(exec_table)

    def get_all_data(self):
        self.get_record_data()
        self.get_exec_data()

        all_data = []
        for row in self.record_data:
            full_row = row
            exec_row = []
            owner_row = []
            for erow in self.exec_data:
                if erow[0] == row[1]:
                    exec_row = erow[1:]
                    break

            for orow in self.owner_data:
                if orow[0] == row[1]:
                    owner_row = orow[1:]
                    break

            if len(owner_row) == 3 and len(exec_row) == 3:
                full_row += owner_row
                full_row += exec_row
                all_data.append(full_row)

        self.all_data = all_data

def get_all_data():
    full_data = []
    for team in settings.teams:
        time.sleep(2)
        print team
        try:
            team_info = TeamInfo(team)
            team_info.get_all_data()
            full_data += team_info.all_data
        except Exception:
            print "Error parsing team"
            traceback.print_exc()

    rows = [",".join(["\"{0}\"".format(e) for e in row]) for row in full_data]
    rows.insert(0, ",".join(["\"{0}\"".format(e) for e in ["team", "year", "wins", "losses", "ties", "points_for", "points_against", "points_diff", "coach_name", "coach_id", "passer_name", "passer_id", "rusher_name", "rusher_id", "receiver_name", "receiver_id", "off_points", "off_yards", "def_points", "def_yards", "takeaway_giveaway_ratio", "point_differential_rank", "yard_differential_rank", "teams_in_league", "margin_of_victory", "strength_of_schedule", "simple_rating_system", "offensive_srs", "defensive_srs", "owner_name", "owner_id", "owner_title", "gm_name", "gm_id", "gm_title"]]))
    csv_string = "\n".join(rows)
    f = open(settings.FILE_PATH, 'w+')
    f.write(csv_string)
    f.close()
