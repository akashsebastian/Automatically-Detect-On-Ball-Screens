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

    def __init__(self, event, path_to_json, event_index, frame):
        self.frame_init = frame
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
        self.j = 0
        self.handler_defender = np.zeros(34)
        self.screener_defender = np.zeros(34)
        self.handler_screener = np.zeros(34)
        self.handler_basket = np.zeros(34)
        self.screener_basket = np.zeros(34)
        self.defender_basket = np.zeros(34)
        self.features = np.zeros(30)

    def calc(self, i, moment, radius, last):
        coords=[[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[moment.ball.x,moment.ball.y]]
        for j in range(10):
            coords[j][0] = moment.players[j].x
            coords[j][1] = moment.players[j].y
        distances = euclidean_distances(coords, coords)
        ball_handler = np.argmin(distances[-1][:-1])
        if ball_handler < 5:
            self.screener = np.argmin(np.array([x for i, x in enumerate(distances[ball_handler][:5]) if i != ball_handler]))
        else:
            self.screener = np.argmin(np.array([x for i, x in enumerate(distances[ball_handler][5:-1]) if i != ball_handler-5])) + 5
        if ball_handler < 5:
            self.on_ball_defender = np.argmin(np.array(distances[ball_handler][5:-1]))
        else:
            self.on_ball_defender = np.argmin(np.array(distances[ball_handler][:5]))
        if(i==last):
            s = np.argmin(self.handler_screener)
            if s == 0:
                return 
            self.features[0] = np.argmin(self.handler_defender)
            self.features[1] = (self.handler_defender[s] - self.handler_defender[0]) / s
            self.features[2] = sum(self.handler_defender[:s+1])/s
            self.features[3] = (self.handler_defender[-1] - self.handler_defender[s])/(len(self.handler_defender) - s)
            self.features[4] = sum(self.handler_defender[s:])/(len(self.handler_defender) - s)
            self.features[5] = np.argmin(self.screener_defender)
            self.features[6] = (self.screener_defender[s] - self.screener_defender[0]) / s
            self.features[7] = sum(self.screener_defender[:s+1])/s
            self.features[8] = (self.screener_defender[-1] - self.screener_defender[s])/(len(self.screener_defender) - s)
            self.features[9] = sum(self.screener_defender[s:])/(len(self.screener_defender) - s)
            self.features[10] = np.argmin(self.handler_screener)
            self.features[11] = (self.handler_screener[s] - self.handler_screener[0]) / s
            self.features[12] = sum(self.handler_screener[:s+1])/s
            self.features[13] = (self.handler_screener[-1] - self.handler_screener[s])/(len(self.handler_screener) - s)
            self.features[14] = sum(self.handler_screener[s:])/(len(self.handler_screener) - s)
            self.features[15] = np.argmin(self.handler_basket)
            self.features[16] = (self.handler_basket[s] - self.handler_basket[0]) / s
            self.features[17] = sum(self.handler_basket[:s+1])/s
            self.features[18] = (self.handler_basket[-1] - self.handler_basket[s])/(len(self.handler_basket) - s)
            self.features[19] = sum(self.handler_basket[s:])/(len(self.handler_basket) - s)
            self.features[20] = np.argmin(self.screener_basket)
            self.features[21] = (self.screener_basket[s] - self.screener_basket[0]) / s
            self.features[22] = sum(self.screener_basket[:s+1])/s
            self.features[23] = (self.screener_basket[-1] - self.screener_basket[s])/(len(self.screener_basket) - s)
            self.features[24] = sum(self.screener_basket[s:])/(len(self.screener_basket) - s)
            self.features[25] = np.argmin(self.defender_basket)
            self.features[26] = (self.defender_basket[s] - self.defender_basket[0]) / s
            self.features[27] = sum(self.defender_basket[:s+1])/s
            self.features[28] = (self.defender_basket[-1] - self.defender_basket[s])/(len(self.defender_basket) - s)
            self.features[29] = sum(self.defender_basket[s:])/(len(self.defender_basket) - s)
            # print(self.features)
            return
        # print("Screener: {} Ball Handler: {}".format(self.on_ball_defender,ball_handler))
        self.handler_defender[self.j] = distances[ball_handler][self.on_ball_defender]
        self.screener_defender[self.j] = distances[self.screener][self.on_ball_defender]
        self.handler_screener[self.j] = distances[self.screener][ball_handler]
        self.handler_basket[self.j] = min(euclidean_distances([[coords[ball_handler][0],coords[ball_handler][1]]],[[0,25]])[0][0],euclidean_distances([[coords[ball_handler][0],coords[ball_handler][1]]],[[94,25]])[0][0])
        self.screener_basket[self.j] = min(euclidean_distances([[coords[self.screener][0],coords[self.screener][1]]],[[0,25]])[0][0],euclidean_distances([[coords[self.screener][0],coords[self.screener][1]]],[[94,25]])[0][0])
        self.defender_basket[self.j] = min(euclidean_distances([[coords[self.on_ball_defender][0],coords[self.on_ball_defender][1]]],[[0,25]])[0][0],euclidean_distances([[coords[self.on_ball_defender][0],coords[self.on_ball_defender][1]]],[[94,25]])[0][0])
        # print("Distance between screener {} and defender is {} Distance:{}".format(self.screener,screener_defender[j],distances[5][6]))
        self.j += 1

    def show(self):
        if self.frame_init + 24 > len(self.moments):
            return
        for i in range(self.frame_init, self.frame_init+ 24):
            moment = self.moments[i]
            self.calc(i, moment, moment.ball.radius,self.frame_init+23)
        return self.features
