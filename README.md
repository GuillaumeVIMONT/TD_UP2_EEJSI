# TD_UP2_EEJSI

All ressources for the TD EEJSI are into this Repo 

## About

The main goal, is to understand how we can generate social graph network from Twitter in Streaming and apply sampling method on the stream.

![](https://raw.githubusercontent.com/GuillaumeVIMONT/TD_UP2_EEJSI/master/fig1.png )

## Prerequisite :


-> Step 1: Install Anaconda

To run python script, you need to have a python environment, if you don't have this please download Anaconda.

https://repo.continuum.io/archive/Anaconda3-5.1.0-Windows-x86_64.exe

-> Step 2: Create Twitter API

To use the twitter API streaming you need to have an account with credential to interact with the Twitter API, if you don't have this please follow instructions into this tutorial.

Tutorial link => https://botwiki.org/tutorials/how-to-create-a-twitter-app/

-> Step 3: Download Twitter Program

After complete all prerequisites above, download into github the repo with all resources necessary to complete this course

Link => https://github.com/GuillaumeVIMONT/TD_UP2_EEJSI

Direct download => https://github.com/GuillaumeVIMONT/TD_UP2_EEJSI/archive/master.zip

## Part 1

Open the github folder, previously downloaded

Please go to the folder "TD_0"

This is a basic experience to explain reservoir sampling with social edges in offline mode.

Into the folder you have a data file with 100 edges and another one with 390 000 edges from a twitter capture on CNN.

Reminder :

Reservoir sampling is a family of randomized algorithms for randomly choosing a sample of k items from a list S containing n items, where n is either a very large or unknown number. Typically n is large enough that the list doesn't fit into main memory.

Run script:

Please open Anaconda Prompt and write:

`cd path/to/the/current/folder`

After it write:

`python main.py`

This is an interactive python script, to run this execute main.py you need to specify 3 variables :

1- Input file (e.g. data_100.csv)

2- Reservoir sampling size

3 - Output file ( as you like, with a .csv)

After running this program, you can run gephi to play with the network graph.

For more informations about Gephi, please read this page http://www.up2.fr/index.php?n=Main.Gephi


## Part 2

Open the github folder, previously downloaded

Please go to the folder "TD_1"

This is a basic experience to explain reservoir sampling with social edges in streaming mode.

Reminder :

Reservoir sampling is a family of randomized algorithms for randomly choosing a sample of k items from a list S containing n items, where n is either a very large or unknown number. Typically n is large enough that the list doesn't fit into main memory.

Run script:

Please open Anaconda Prompt and write:

`cd path/to/the/current/folder`

Before execute main.py please insert your key into the file config.py

`consumer_key=""`

`consumer_secret=""`

`access_token=""`

`access_token_secret=""`

After it,  write:

`python main.py`

This is an interactive python script, to run this execute main.py you need to specify 3 variables :

1- Please enter number of edges in the reservoir (eg 200)
2- Please enter tracking word (eg CNN)
3- Please enter threshold for the connected component export (eg 5)
4- Please enter duration of the capture in minutes (eg 30)

After running this program, you can run gephi to play with the network graph.

For more informations about Gephi, please read this page http://www.up2.fr/index.php?n=Main.Gephi

## Part 3

Please go to the folder "TD_2"

This is a basic experience to explain window reservoir sampling with social edges on streaming data.

Previously we experiment reservoir sampling, now we consider a stream of edges from Twitter and we apply the window sliding reservoir.

Into a window sliding reservoir, data is considered to be expired after a certain time interval.
“Sliding window” in essence is such a random sample of fixed size (say k) “moving” over the most recent elements in the data stream.

Types of Sliding Window: Time-stamp based

Windows of duration t consist of elements whose arrival timestamp is within a time interval  t of the current time. Example being Priority Sample for Sliding Window

We will be storing only the eligible elements in the memory.
Therefore expected memory usage is O(log n), or O(k log n) for samples of size k.

Before execute main.py please insert your key into the file config.py

`consumer_key=""`

`consumer_secret=""`

`access_token=""`

`access_token_secret=""`
 

This script interact with Twitter so you need to install an external python library called Tweepy.
To install it :

Open a command line terminal and execute : 

	conda install -c conda-forge tweepy

Run script:

Please open Anaconda Prompt and write:

`cd path/to/the/current/folder`

After it write:

`python main.py`


This is an interactive python script, to run this execute main.py you need to specify 4 variables : 

1- Window reservoir size (eg 200)

2- Window sliding in minutes (eg 10)

3- Window export edges in minutes (eg 2)

4- Traking word to capture twitter stream

If all it’s ok, you need to have file data into the data folder

After running this program, you can run gephi to play with the network graph.

For more informations about Gephi, please read this page http://www.up2.fr/index.php?n=Main.Gephi


## Part 4

Please go to the folder "TD_3"

This is a basic experience with Bitcoin API.
