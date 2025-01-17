from pathlib import PosixPath
import pandas as pd
import os
from tqdm import tqdm
import logging
import sys

if not sys.warnoptions:
    import warnings
    warnings.simplefilter("ignore")
    
logging.basicConfig(level= logging.DEBUG, filename="split.log", filemode="w")

print("\n")
print("#"*5, end = '')
print("SPLITTING DATA", end='')
print("#"*5)
print("\n")

class Dataset:
    DATA_FILE_PATH = "../../datasets/Full/players_20.csv"
    OUTPUT_DIRECTORY = "../../datasets/Positionwise"

    USELESS_ATTRIBUTES = {
        'centre_backs': ['attacking_crossing', 'attacking_finishing', 'attacking_volleys', 'skill_dribbling',
                        'skill_curve', 'skill_fk_accuracy', 'skill_ball_control', 'power_shot_power',
                        'power_long_shots', 'mentality_penalties'],

        'full_backs': ['attacking_heading_accuracy', 'attacking_volleys', 'skill_curve', 'skill_fk_accuracy',
                    'power_shot_power', 'power_jumping', 'power_long_shots', 'mentality_aggression', 
                    'mentality_composure'],

        'midfielders': ['attacking_crossing', 'attacking_finishing', 'attacking_heading_accuracy', 'attacking_volleys',
                    'skill_curve', 'skill_fk_accuracy', 'mentality_penalties'],

        'wingers': ['attacking_heading_accuracy', 'attacking_volleys', 'power_shot_power', 'power_jumping', 
                    'defending_marking', 'defending_standing_tackle', 'defending_sliding_tackle'],

        'free_roamers': ['attacking_heading_accuracy', 'attacking_volleys', 'power_shot_power', 'power_jumping', 
                        'power_long_shots', 'mentality_aggression', 'mentality_interceptions', 'mentality_positioning', 
                        'defending_marking', 'defending_standing_tackle', 'defending_sliding_tackle'],                                  

        'strikers': ['attacking_crossing', 'skill_long_passing', 'mentality_aggression', 'mentality_interceptions',
                    'mentality_positioning', 'mentality_vision', 'defending_marking', 'defending_standing_tackle',
                    'defending_sliding_tackle'],
    }                                                          

    def __read_filtered_data(self, DATA_FILE_PATH):
        self.data = pd.read_csv(DATA_FILE_PATH, index_col=0)

    def __split_by_position(self):
        positionwise_data = dict()
        positionwise_data['centre_backs'] = self.data.loc[self.data['team_position'].isin(['LCB', 'RCB', 'SW', 'CB'])]
        positionwise_data['full_backs'] = self.data.loc[self.data['team_position'].isin(['LB', 'RB', 'LWB', 'RWB'])]
        positionwise_data['midfielders'] = self.data.loc[self.data['team_position'].isin(['CDM', 'RDM', 'LDM', 'CM', 'RCM', 'LCM'])]
        positionwise_data['wingers'] = self.data.loc[self.data['team_position'].isin(['LW', 'LM', 'RW', 'RM'])]
        positionwise_data['free_roamers'] = self.data.loc[self.data['team_position'].isin(['RAM', 'LAM', 'CAM'])]
        positionwise_data['strikers'] = self.data.loc[self.data['team_position'].isin(['ST', 'RS', 'LS', 'CF', 'LF', 'RF'])]
        self.positionwise_data = positionwise_data

    def __filter_split_data(self):
        for position in self.positionwise_data:
            for useless_attribute_idx in tqdm(range(len(self.USELESS_ATTRIBUTES[position])), desc = f"{position}", ncols = 100):
                useless_attribute = self.USELESS_ATTRIBUTES[position][useless_attribute_idx]
                self.positionwise_data[position].drop(useless_attribute, axis=1, inplace=True)
        #list(map(lambda position: map(lambda useless_attribute: self.positionwise_data[position].drop(useless_attribute, axis=1, inplace=True), self.USELESS_ATTRIBUTES[position]), self.positionwise_data.keys()))

    def __write_to_csv(self, OUTPUT_DIRECTORY):
        if not os.path.exists(OUTPUT_DIRECTORY):
            os.mkdir(OUTPUT_DIRECTORY)
        list(map(lambda position: self.positionwise_data[position].to_csv(f'{OUTPUT_DIRECTORY}/{position}.csv', index=True), self.positionwise_data.keys()))

    def create_datasets(self, DATA_FILE_PATH=None, OUTPUT_DIRECTORY=None):
        if not DATA_FILE_PATH:
            DATA_FILE_PATH = self.DATA_FILE_PATH
        if not OUTPUT_DIRECTORY:
            OUTPUT_DIRECTORY = self.OUTPUT_DIRECTORY

        self.__read_filtered_data(DATA_FILE_PATH=DATA_FILE_PATH)
        self.__split_by_position()
        self.__filter_split_data()
        self.__write_to_csv(OUTPUT_DIRECTORY)

    def print_data(self):
        list(map(lambda position: print(self.positionwise_data[position].to_markdown()), self.positionwise_data.keys()))
        print("\n\n\n\n")

#dataset = Dataset()
#dataset.create_datasets()
#myData.filter_data()
#myData.print_data()
Dataset().create_datasets()


