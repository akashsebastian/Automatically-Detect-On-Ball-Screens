from Game import Game
import pandas as pd
# import argparse
#
# parser = argparse.ArgumentParser(description='Process arguments about an NBA game.')
# parser.add_argument('--path', type=str,
#                     help='a path to json file to read the events from',
#                     required = True)
# parser.add_argument('--event', type=int, default=0,
#                     help="""an index of the event to create the animation to
#                             (the indexing start with zero, if you index goes beyond out
#                             the total number of events (plays), it will show you the last
#                             one of the game)""")
#
# args = parser.parse_args()
train = pd.read_csv('train.csv')
for index,row in train.iterrows():
    print("Game ID: {}, Event Index: {}, Frame Number: {} {}/{}".format(row.Game_ID,row.Event_Number,row.Frame_Number,index,len(train)))
    game = Game(path_to_json=row.Game_ID, event_index=row.Event_Number, frame=row.Frame_Number)
    game.read_json()
    features = game.start()
    if features is None:
        continue
    for i in range(len(features)):
        str_col = 'f' + str(i)
        train.at[index,str_col] = features[i]
train = train.dropna(axis=0)
train.to_csv('train_fin.csv',index=False)
