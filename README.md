# Automatically Detect On Ball Screens 

This repository contains code to implement the paper titled "Automatically Recognizing On-Ball Screens" published by Armand McQueen, Jenna Wiens and John Guttag at the MIT Sloan Sports Analytics Conference of 2014. The paper can be found here: http://www.sloansportsconference.com/wp-content/uploads/2014/02/2014_SSAC_Recognizing-on-Ball-Screens.pdf 

  

# Disclaimer: 

I'm still working with my college to get permissions to upload certain parts of the code and report.  

  

# Theory 

This code uses the SportsVU Optical Tracking by STATS. The data can be found on the STATS website. The Optical Tracking data is compiled by special cameras attached to the rafters of the arena. It tracks the x and y coordinates of all 10 players on the court and the x, y and z coordinates of the ball at 25 samples per second.   

  

The first part of the paper involves segmenting the dataset to separate all the frames that may or may not contain a screen. To achieve this, several rules are used to segment the frames. These rules are based on relative distances between the three players involved in a screen (screener, on ball defender and the ball handler) and their distances relative to fixed positions or areas on the court like the paint or the basket. 

  

The second part involves extracting features from the segmented frames. This is done by finding the frame the screen occurs by calculating the pairwise minimum distance between the ball handler and the screener. Using this value, five metrics are calculated for each pair among the three players involved. A total of 30 features are extracted from the frames.  

  

I am still working on getting the permissions for the third part of the paper. I will upload the code along with the corresponding part of the report.  

  

# How to run the code 

The code is written in Python3. Extract all the game data zip files into an Extract folder. Run the parent.py script. This acts as the parent script which calls the main.py for every event for every game that exists in the Extract folder. The results get appended to the screen_segmentation.csv file. The Game ID, Event Number and Frame Number are stored in the CSV file.    
