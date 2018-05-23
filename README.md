# Recommendation System
Recommendation System built to test the concepts of a paper to be published.

## Pre-Requisites

# Software

- Python 3.5 or higher
- MongoDB 3.4.9 or higher

# Word-embedder
You will also need a word embedder. Theoretically you can use any word-embedder of your preference that gensim supports. Some code adaptations may be required if you wanna use some other than google's Word2vec

Google's can be downloaded from: https://code.google.com/archive/p/word2vec/

# Datasets

The datasets used in the paper can be found in different pages listed bellow (as for May 2018):

BBC-Sports: http://mlg.ucd.ie/datasets/bbc.html
Reuters: https://archive.ics.uci.edu/ml/datasets/Reuters-21578+Text+Categorization+Collection
20-News: https://archive.ics.uci.edu/ml/datasets/Twenty+Newsgroups
OHSUMED: http://davis.wpi.edu/xmdv/datasets/ohsumed
Yelp: https://www.yelp.com/dataset/challenge

# Format

Before running the scripts, you need to format the datasets so that it can be read by the program. The format is the `class name` followed by a dot, `a number`, and the `.txt` extension. For example, if you were to convert 5 files from a train folder, the first one being from classA, the following three from classB and the last one from classC, you would have the following structure after conversion:

```
classA.1.txt
classB.1.txt
classB.2.txt
classB.3.txt
classC.1.txt
```

We provide some auxiliary scripts to help you convert the datasets to the desired format, check the **Scripts** section.

## Installing

The program is python interpreted, so you don't need any kind of installation, however some python libraries may be missing, which requires you to install the required libraries. To this kind of usage, a requirements.txt file is provided in this repository. You can install the dependencies using pip. Simply run the following command:

`pip3 install -r requirements.txt`

## Running

Testing the scripts can be divided into two steps: The first one being the creation of the models itself, and the second being the actual test phase.

### Creating the models

To create the models, run:

`python3 trainning_module.py "trainFolder" "datasetName"`

* trainFolder: The folder that contains all the train samples in the format `class.number.txt` (Only txt files accepted)
* datasetName: The dataset that the train/test set belongs. It will use the models referent to the dataset.

### Testing the models

To test the models, run:

`python3 testing_module.py "testFolder" "datasetName"`

* testFolder: The folder that contains all the test samples in the format `class.number.txt` (Only txt files accepted)
* datasetName: The dataset that the train/test set belongs. It will use the models referent to the dataset.

### Running Train and Test at once

You can run both stages train and test at once.
For this case, you need to run:

`python3 main.py "trainFolder" "testFolder" "datasetName" `

* trainFolder: The folder that contains all the train samples in the format `class.number.txt` (Only txt files accepted)
* testFolder: The folder that contains all the test samples in the format `class.number.txt` (Only txt files accepted)
* datasetName: The dataset that the train/test set belongs. It will use the models referent to the dataset.


### Running multiple datasets at once

You can run both train and test for different datasets at once.
For this case you need to create a file called `order.txt` that will contain the dataset names and the order they will be executed. The script assumes the dataset folder is ***datasets*** and you have the following folder structure:

```
.
+--+--_datasets
      +--_train
         +--_"trainClassA.1.txt"
         +--_"trainClassA.2.txt"
         +--_"trainClassB.1.txt"
      +--_test
         +--_"testClassA.1.txt"
         +--_"testClassA.2.txt"
         +--_"testClassB.1.txt"
```

To run the script, use the following command:

`python3 complete_test.py`

There's an `order.txt` sample file included.

## Auxiliary Scripts

We provide auxiliary shell scripts to help you convert datasets to the our format. They are located at the scripts folder
