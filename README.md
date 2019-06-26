# Automatically Detect On Ball Screens 

This repository contains code to implement the paper titled "Automatically Recognizing On-Ball Screens" published by Armand McQueen, Jenna Wiens and John Guttag at the MIT Sloan Sports Analytics Conference of 2014. The paper can be found here: http://www.sloansportsconference.com/wp-content/uploads/2014/02/2014_SSAC_Recognizing-on-Ball-Screens.pdf 

A detailed description of the project can be found here: https://medium.com/@akashsebastian/automatically-recognizing-on-ball-screens-using-stats-sportvu-optical-tracking-data-and-machine-14ed144d6d50

# How to run the code

The code is written in python 3. To run the segmentor, run the parent.py file in the Segmentor folder. Extract all the games which need to be segmented to a folder named Extract in that directory. To run the feature extraction, run the main.py file from the Train_NBA folder after manually categorizing segmented data from screen_segmentation_csv and name it train.csv. The new csv with all the features will be stored in train_fin.csv. To run the SVM, run ml.py. 
