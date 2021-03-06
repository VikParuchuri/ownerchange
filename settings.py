import os

BASE_DIR = os.path.dirname(__file__)
FILE_PATH = os.path.join(BASE_DIR, "data", "nfl.csv")
JSON_PATH = os.path.join(BASE_DIR, "data", "teams")
JSON_METADATA_FILE = os.path.join(BASE_DIR, "data", "meta.json")

teams = {
            "crd": "Arizona Cardinals",
            "atl": "Atlanta Falcons",
            "rav": "Baltimore Ravens",
            "buf": "Buffalo Bills",
            "car": "Carolina Panthers",
            "chi": "Chicago Bears",
            "cin": "Cincinnati Bengals",
            "cle": "Cleveland Browns",
            "dal": "Dallas Cowboys",
            "den": "Denver Broncos",
            "det": "Detroit Lions",
            "gnb": "Green Bay Packers",
            "htx": "Houston Texans",
            "clt": "Indianapolis Colts",
            "jax": "Jacksonville Jaguars",
            "kan": "Kansas City Chiefs",
            "mia": "Miami Dolphins",
            "min": "Minnesota Vikings",
            "nwe": "New England Patriots",
            "nor": "New Orleans Saints",
            "nyg": "New York Giants",
            "nyj": "New York Jets",
            "rai": "Oakland Raiders",
            "phi": "Philadelphia Eagles",
            "pit": "Pittsburgh Steelers",
            "sdg": "San Diego Chargers",
            "sfo": "San Francisco 49ers",
            "sea": "Seattle Seahawks",
            "ram": "St Louis Rams",
            "tam": "Tampa Bay Buccaneers",
            "oti": "Tennessee Titans",
            "was": "Washington Redskins"
}

MAX_YEAR = 2013