
###############################################################################
#                                Encode labels                                #
###############################################################################
import pandas as pd
import numpy as np
import string
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from sklearn.preprocessing import LabelEncoder

def search_island(current_longitude='A',
                  current_latitude=1,
                  search_island="Mermaid's Hideaway"):

    # load data
    dataset = pd.read_csv('Sea_of_thieves_islands.csv')

    # encode labels with text to represent a position
    encoder = LabelEncoder()
    encoder = encoder.fit(dataset['Long'])
    dataset['Long'] = encoder.transform(dataset['Long'])

    # position column
    dataset['Position'] = list(zip(dataset['Long'], dataset['Lat']))

    # encoder
    current_longitude = encoder.transform([current_longitude])[0]
    my_pos = np.array([current_longitude, current_latitude])

    # island position
    island_pos = np.array([
        dataset.loc[dataset['Name'] == search_island]['Position'].values[0][0],
        dataset.loc[dataset['Name'] == search_island]['Position'].values[0][1]
    ])

    # distance
    dist_x = my_pos[0] - island_pos[0]
    dist_y = my_pos[1] - island_pos[1]

    # compass direction
    if dist_x == 0:
        direction_x = 150
    elif dist_x > 0:
        direction_x = (abs(dist_x) / 25) * 150
    else:
        direction_x = 150 + (abs(dist_x) / 25) * 150

    if dist_y == 0:
        direction_y = 150
		
    # its inverted because of the map being inverted too
    elif dist_y < 0:
        direction_y = 150 + (abs(dist_y) / 25) * 150
    else:
        direction_y = (abs(dist_y) / 25) * 150

    # draw chart
    plt.figure(1)

    # map
    plt.scatter(dataset['Long'], dataset['Lat'], marker='.')
    plt.scatter(my_pos[0], my_pos[1], marker='^', c='r')
    plt.scatter(island_pos[0], island_pos[1], marker='o', c='r')
    plt.arrow(my_pos[0], my_pos[1], dist_x * -1, dist_y * -1, head_width=0.5, head_length=0.5)
    plt.title('World Map')
    plt.xticks([x for x in range(26)], list(string.ascii_uppercase))
    plt.yticks([x for x in range(26)], [x for x in range(26)])
    plt.axis([-1, 26, -1, 26])
    plt.grid(True)
    plt.gca().invert_yaxis()

    # compass
    plt.figure(2)
    plt.imshow(mpimg.imread('compass.png'))
    plt.plot([150, direction_x], [150, direction_y], c='r')

    plt.show()


# Find direction
search_island('W', 9, "The Sunken Grove")
