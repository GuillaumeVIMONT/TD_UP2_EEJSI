________         _______________      
___  __/__      ____(_)_  /__  /_____________
__  /  __ | /| / /_  /_  __/  __/  _ \_  ___/
_  /   __ |/ |/ /_  / / /_ / /_ /  __/  /
/_/    ____/|__/ /_/  \__/ \__/ \___//_/  

This is a basic experience to explain window reservoir sampling with social edges on streaming data.

Previously we experiment reservoir sampling, now we consider a stream of edges from Twitter and we apply the window sliding reservoir.

Into a window sliding reservoir, data is considered to be expired after a certain time interval.
“Sliding window” in essence is such a random sample of fixed size (say k) “moving” over the most recent elements in the data stream.
