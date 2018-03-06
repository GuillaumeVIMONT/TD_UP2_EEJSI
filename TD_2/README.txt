________         _______________      
___  __/__      ____(_)_  /__  /_____________
__  /  __ | /| / /_  /_  __/  __/  _ \_  ___/
_  /   __ |/ |/ /_  / / /_ / /_ /  __/  /
/_/    ____/|__/ /_/  \__/ \__/ \___//_/  

This is a basic experience to explain window reservoir sampling with social edges on streaming data.

Previously we experiment reservoir sampling, now we consider a stream of edges from Twitter and we apply the window sliding reservoir.

Into a window sliding reservoir, data is considered to be expired after a certain time interval.
“Sliding window” in essence is such a random sample of fixed size (say k) “moving” over the most recent elements in the data stream.

Types of Sliding Window: Time-stamp based

Windows of duration t consist of elements whose arrival timestamp is within a time interval  t of the current time. Example being Priority Sample for Sliding Window

We will be storing only the eligible elements in the memory.
Therefore expected memory usage is O(log n), or O(k log n) for samples of size k.

Before execute main.py please insert your key into the file config.py 

consumer_key=""
consumer_secret=""
access_token=""
access_token_secret="« 


This is an interactive python script, you need to specify 3 variables : 

1- Window reservoir size (eg 200)
2- Window sliding in minutes (eg 10)
3- Window export edges in minutes (eg 2)
4- Traking word to capture twitter stream


After running this program, you can run gephi to play with the network graph.



