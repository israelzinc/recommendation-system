# Recommendation System
Recommendation System built to test the concepts of a paper to be published.

## Pre-Requisites

- Python 3.5 or higher
- MongoDB 3.x

## Datasets

All the datasets can be found in different pages

BBC-Sports
Reuters
20-News
OHSUMED
Yelp

### Format

Before running the scripts, you need to format the datasets so that it can be read by the program

## Installing

The program is python interpreted, so you don't need any kind of installation, however some python libraries may be missing, which requires you to install the required libraries. To this kind of usage, a requirements.txt file is provided in this repository. You can install the dependencies using pip. Simply run the following command:

pip3 install -r requirements.txt

## Running

Testing the scripts can be divided into two steps: The first one being the creation of the models itself, and the second being the actual test phase.

### Creating the models

To create the models, run:

python3 trainning_module.py "folderName" "trainName"

folderName: is the folder that contains all the train set in the format class.number.txt (Only txt files accepted)

trainName: is the name of the model, you need to train the model with the correct train/test set to have good accuracy

## Testing the models

To test the models, run:

python3 testing_module.py "folderName" "trainName"

folderName: is the folder that contains all the test set in the format class.number.txt (Only txt files accepted)

trainName: is the name of the model, you need to train the model with the correct train/test set to have good accuracy

## Running all at once

You can run both train and test for different datasets at once.
For this case you need to create a file called order.txt that will contain the dataset names. The script assumes the dataset folder is datasets and you have a structure like the following datasets/train and datasets/test for train and test respectively.

For that, run the following script:

python3 complete_test.py

## Auxiliary Scripts
