___  __/__      ____(_)_  /__  /_____________
__  /  __ | /| / /_  /_  __/  __/  _ \_  ___/
_  /   __ |/ |/ /_  / / /_ / /_ /  __/  /
/_/    ____/|__/ /_/  \__/ \__/ \___//_/  

This is a basic experience to explain window reservoir sampling with social edges on streaming data.

Previously we experiment reservoir sampling on static data, now we consider a stream of edges from Twitter and we apply the reservoir sampling.


We will be storing only the eligible elements in the memory.
Therefore expected memory usage is O(log n), or O(k log n) for samples of size k.

Before execute main.py please insert your key into the file config.py 

consumer_key=""
consumer_secret=""
access_token=""
access_token_secret="« 


This is an interactive python script, you need to specify 3 variables : 

1- Number of edges in the reservoir (eg 200)
2- Traking word to capture twitter stream
3- Experience duration


After running this program, you can run gephi to play with the network graph.
