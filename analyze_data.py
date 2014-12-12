import pandas
import sklearn
from sklearn.ensemble import RandomForestRegressor
import settings

class RecordModel(object):
    def __init__(self):
        self.csv_data = pandas.read_csv(settings.FILE_PATH, index_col=False)

    def create_train_data(self):
        csv_data = self.csv_data
        wins_dict = {}
        id_mapping = {}
        reverse_id_mapping = {}
        id_numbers = {}
        team_mapping = {}
        reverse_team_mapping = {}
        for team in settings.teams:
            team_wins = {}
            team_data = csv_data[csv_data["team"] == team]
            for id, row in team_data.iterrows():
                if row["year"] <= settings.MAX_YEAR:
                    team_wins[row["year"] + 1] = row["wins"]
            wins_dict[team] = team_wins
        for id, row in csv_data.iterrows():
            id_mapping[row["gm_id"]] = row["gm_name"]
            id_mapping[row["owner_id"]] = row["owner_name"]
            id_mapping[row["coach_id"]] = row["coach_name"]

        sel_frame = csv_data[["team", "year", "coach_id", "gm_id", "owner_id", "wins"]]
        sel_frame = sel_frame[(sel_frame["year"] > 1960) & (sel_frame["year"] < 2014)]
        prev_wins = []
        for id, row in sel_frame.iterrows():
            wins = wins_dict[row["team"]].get(row["year"], 8)
            prev_wins.append(wins)
        sel_frame["prev_wins"] = prev_wins

        for i, item in enumerate(id_mapping.keys()):
            id_numbers[i] = id_mapping[item]
            reverse_id_mapping[item] = i

        for i, team in enumerate(settings.teams.keys()):
            team_mapping[i] = team
            reverse_team_mapping[team] = i

        coach_num = []
        gm_num = []
        owner_num = []
        team_num = []
        for id, row in sel_frame.iterrows():
            owner_num.append(reverse_id_mapping[row["owner_id"]])
            gm_num.append(reverse_id_mapping[row["gm_id"]])
            coach_num.append(reverse_id_mapping[row["coach_id"]])
            team_num.append(reverse_team_mapping[row["team"]])

        sel_frame["coach_num"] = coach_num
        sel_frame["gm_num"] = gm_num
        sel_frame["owner_num"] = owner_num
        sel_frame["team_num"] = team_num

        self.train_data = sel_frame
        self.id_mapping = id_mapping
        self.id_numbers = id_numbers
        self.reverse_id_numbers = reverse_id_mapping
        self.reverse_team_mapping = reverse_team_mapping
        self.team_mapping = team_mapping

    def cross_validate(self):
        train_data = self.train_data
        clf = RandomForestRegressor(n_estimators=200, min_samples_leaf=4, random_state=1)
        kf = sklearn.cross_validation.KFold(len(train_data["wins"]), 3)
        real = []
        preds = []
        good_predictors = ["team_num", "coach_num", "gm_num", "owner_num", "prev_wins"]
        for train, test in kf:
            clf.fit(train_data[good_predictors].iloc[train, :], train_data["wins"].iloc[train])
            actual = train_data["wins"].iloc[test]
            pred = pandas.DataFrame(clf.predict(train_data[good_predictors].iloc[test, :]))
            real.append(actual)
            preds.append(pred)
        all_real = pandas.concat(real, axis=0).reset_index()
        all_preds = pandas.concat(preds, axis=0).reset_index()
        pred_frame = pandas.concat([all_real, all_preds], axis=1)
        print ((sum((pred_frame.iloc[:,3] - pred_frame.iloc[:,1]) ** 2))/ len(pred_frame)) ** .5