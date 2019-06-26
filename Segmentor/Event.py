from Constant import Constant
from Moment import Moment
from Team import Team
import matplotlib.pyplot as plt
from matplotlib import animation
from matplotlib.patches import Circle, Rectangle, Arc
from sklearn.metrics.pairwise import euclidean_distances
import numpy as np
import csv

class Event:
    """A class for handling and showing events"""

    def __init__(self, event, path_to_json, event_index):
        moments = event['moments']
        self.moments = [Moment(moment) for moment in moments]
        home_players = event['home']['players']
        guest_players = event['visitor']['players']
        players = home_players + guest_players
        player_ids = [player['playerid'] for player in players]
        player_names = [" ".join([player['firstname'],
                        player['lastname']]) for player in players]
        player_jerseys = [player['jersey'] for player in players]
        values = list(zip(player_names, player_jerseys))
        # Example: 101108: ['Chris Paul', '3']
        self.player_ids_dict = dict(zip(player_ids, values))
        self.frame = 0
        self.ball_handler = 0
        self.screener = None
        self.on_ball_defender = None
        self.ball_radius = None
        self.path_to_json = path_to_json
        self.event_index = event_index
        self.test_a = 0

    def test_func(self, i, moment, radius):
        flag = [0,0,0,1]
        # Dribbling the ball?
        if radius != self.ball_radius:
            self.ball_radius = radius
            flag[0] = 1

        # Ball in the Paint?
        if (0 <= moment.ball.x <= 19 and 17 <= moment.ball.y <= 33) or (75 <= moment.ball.x <= 94 and 17 <= moment.ball.y <= 33):
            flag[3] = 0
        if flag[3] == 1 and flag[0] == 1:
            coords=[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[moment.ball.x,moment.ball.y]]
            for j in range(10):
                coords[j][0] = moment.players[j].x
                coords[j][1] = moment.players[j].y
            distances = euclidean_distances(coords, coords)
            ball_handler = np.argmin(distances[-1][:-1])
            # Offensive player wihtin 10 feet of the ball handler
            if ball_handler < 5:
                if self.screener == None:
                    flag[1] = 1
                    self.screener = np.argmin(np.array([x for i, x in enumerate(distances[ball_handler][:5]) if i != ball_handler]))
                elif np.any(np.array([x for i, x in enumerate(distances[ball_handler][:5]) if i != ball_handler])<10) and self.screener == np.argmin(np.array([x for i, x in enumerate(distances[ball_handler][:5]) if i != ball_handler])):
                    flag[1] = 1
                    # print("Least Distance: {}".format(np.argmin(np.array([x for i, x in enumerate(distances[ball_handler][:5]) if i != ball_handler]))+1))
                else:
                    self.screener = np.argmin(np.array([x for i, x in enumerate(distances[ball_handler][:5]) if i != ball_handler]))
            else:
                if self.screener == None:
                    flag[1] = 1
                    self.screener = np.argmin(np.array([x for i, x in enumerate(distances[ball_handler][5:-1]) if i != ball_handler - 5]))
                elif np.any(np.array([x for i, x in enumerate(distances[ball_handler][5:-1]) if i != ball_handler - 5])<10) and self.screener == np.argmin(np.array([x for i, x in enumerate(distances[ball_handler][5:-1]) if i != ball_handler - 5])):
                    flag[1] = 1
                else:
                    self.screener = np.argmin(np.array([x for i, x in enumerate(distances[ball_handler][5:-1]) if i != ball_handler - 5]))

            # print("Ball Handler: {}".format(ball_handler + 1))

            # Defensive player within 12 feet from the ball handler
            if flag[1] == 1:
                if ball_handler < 5:
                    if self.on_ball_defender == None:
                        flag[2] = 1
                        self.on_ball_defender = np.argmin(np.array(distances[ball_handler][5:-1]))
                    elif np.any(np.array(distances[ball_handler][5:-1])<=12) and self.on_ball_defender == np.argmin(np.array(distances[ball_handler][5:-1])):
                        flag[2] = 1
                    else:
                        self.on_ball_defender = np.argmin(np.array(distances[ball_handler][5:-1]))
                else:
                    if self.on_ball_defender == None:
                        flag[2] = 1
                        self.on_ball_defender = np.argmin(np.array(distances[ball_handler][5:-1]))
                    elif np.any(np.array(distances[ball_handler][5:-1])<=12) and self.on_ball_defender == np.argmin(np.array(distances[ball_handler][5:-1])):
                        flag[2] = 1
                    else:
                        self.on_ball_defender = np.argmin(np.array(distances[ball_handler][5:-1]))

        if flag == [1,1,1,1]:
            self.frame += 1
            # print(self.frame)
            if self.frame == 13:
                print("Screen at {}".format(i))
                row = [self.path_to_json, self.event_index, i]
                with open('screen_segmentation.csv','a') as csvFile:
                    writer = csv.writer(csvFile)
                    writer.writerow(row)
                self.frame = 0
        else:
            self.frame = 0
            # print("Flag: {}".format(flag))

    def show(self):
        for i in range(len(self.moments)):
            moment = self.moments[i]
            if len(moment.players) < 10:
                continue
            self.test_func(i, moment, moment.ball.radius)
        return 0
