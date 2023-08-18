from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from time import time
import pandas as pd

class Model:
    def __init__(self, matches_data):
        self.matches_data = matches_data
        self.home_encoded_mapping, self.away_encoded_mapping = self.__label_encode()
        self.__split_data()


    # private func: convert the columns with string type to numeric
    def __label_encode(self):
        encoder = LabelEncoder()
        home_encoded = encoder.fit_transform(self.matches_data['HomeTeam'])
        home_encoded_mapping = dict(
            zip(encoder.classes_, encoder.transform(encoder.classes_).tolist()))
        self.matches_data['home_encoded'] = home_encoded

        encoder = LabelEncoder()
        away_encoded = encoder.fit_transform(self.matches_data['AwayTeam'])
        away_encoded_mapping = dict(
            zip(encoder.classes_, encoder.transform(encoder.classes_).tolist()))
        self.matches_data['away_encoded'] = away_encoded

        return home_encoded_mapping, away_encoded_mapping


    # private func: mapping the names in the new data to the encode
    def __mapping_team_name(self, X):
        X['home_encoded'] = self.home_encoded_mapping[X['HomeTeam']]
        X['away_encoded'] = self.away_encoded_mapping[X['AwayTeam']]


    # private func: split dataset to training data and test data
    def __split_data(self):
        self.X = self.matches_data.drop(columns=['FTR', 'HomeTeam', 'AwayTeam', 'index'])
        self.X['HR'] = -3*self.X['HR']
        self.X['AR'] = -3*self.X['AR']
        self.X['HY'] = -1*self.X['HY']
        self.X['AY'] = -1*self.X['AY']
        self.y = self.matches_data['FTR']
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.X, self.y, test_size=0.25)


    # multiple classifiers
    def model(self):
        svc_classifier = SVC(random_state=100, kernel='rbf', probability=True)
        lg_classifier = LogisticRegression(max_iter=500, multi_class="ovr")
        classifier_dict = {'svm': svc_classifier, 'lg': lg_classifier}
        return classifier_dict


    # train modelss
    def trian(self, classifier):
        # calculate the time of the classifier
        start = time()
        classifier.fit(self.X_train, self.y_train)
        end = time()
        print(classifier, "Model trained in {:2f} seconds".format(end-start))
        return classifier


    # test models
    def test(self, classifier):
        y_pred = classifier.predict(self.X_test)
        acc = sum(self.y_test == y_pred) / float(len(y_pred))
        print(classifier, ' with accuracy: ', acc)
        return acc


    # get the probabilities
    def prob(self, classifier, X_new):
        X_new['home_encoded'] = self.home_encoded_mapping[X_new['HomeTeam']]
        X_new['away_encoded'] = self.away_encoded_mapping[X_new['AwayTeam']]
        del X_new['HomeTeam']
        del X_new['AwayTeam']
        X_df = pd.DataFrame([X_new])
        X_df['HR'] = -3*X_df['HR']
        X_df['AR'] = -3*X_df['AR']
        X_df['HY'] = -1*X_df['HY']
        X_df['AY'] = -1*X_df['AY']
        # X_df = MinMaxScaler().fit_transform(X_df)
        #
        pred_probs = classifier.predict_proba(X_df)[0]
        pred_probs_dict = dict(zip(classifier.classes_, pred_probs))
        return pred_probs_dict

