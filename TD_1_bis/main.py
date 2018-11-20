#import library
from __future__ import absolute_import, print_function
from http.client import IncompleteRead
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import time
import json
from generate_graph import create_graph
#from window_reservoir_sampling_edges import reservoir_sampling_window_stream
import math
import csv
import datetime
from config import TwitterAuth
import sys
import random

# Get date
now = datetime.datetime.now()

print("Before start Twitter capture we need some informations")
# Reservoir Sampling Size
window_k = input("1/3 Please enter number of edges in the reservoir (eg 200): ")
window_k = int(window_k)

# tracking Twitter Stream
tracking = input("2/3 Please enter tracking word (eg CNN) if multi keywords (eg CNN Foxnews): ")

timeout = input("3/3 Please enter duration of the capture in minutes (eg 30): ")
timeout = int(timeout)*60000
start = int(round(time.time() * 1000))

print("Capture in progress")


def write_edge_reservoir(edge_reservoir):
	now = datetime.datetime.now()
	f = open("data/%s_window_reservoir_edges.csv" % (now.strftime("%Y_%m_%d_%Hh%M")), "a")
	f.write("Source, Destination, Timestamp \n")
	for i in edge_reservoir:
		try:
			f.write("%s, %s, %s \n" %i)
		except:
			pass
	f.close()

global L, sample_window_stream, global_counter, time_counter, interval_counter
L=0
sample_window_stream = []
global_counter = 0
interval_counter = 0
time_counter = (time.time()*1000)+60000
def reservoir_sampling_window_stream(edge, k):
    global L, sample_window_stream
    L+=1
    if L < k:
        sample_window_stream.append(edge)
    else:
        j = random.randint(0, L)
        if j < k:
           sample_window_stream[j] = edge
    return sample_window_stream

class StdOutListener(StreamListener):

	""" A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
	"""
	def on_data(self, data):
		global window_k, L, global_counter, time_counter, interval_counter
		twitter_edges_graph = create_graph(data)
		if len(twitter_edges_graph) > 0:
			for edge in twitter_edges_graph:
				global_counter+=1
				interval_counter+=1
				if tracking[0] in edge[1].lower():
					remove(edge)
					pass
				else:
					window_reservoir_sampling = reservoir_sampling_window_stream(edge, window_k)
		if time.time()*1000 > time_counter:
			print("nombre de tuples global", global_counter)
			print("nombre de tuples intervalle", interval_counter)
			interval_counter = 0
			time_counter+=60000
		if time.time()*1000 > start + timeout:
			print("Nombre de tuple global", L)
			print("Taille du réservoir", len(window_reservoir_sampling))
			write_edge_reservoir(window_reservoir_sampling)
			sys.exit('Capture terminated')
		return True


	def on_error(self, status_code):
		if status_code == 420:
			#returning False in on_data disconnects the stream
			return False
    


if __name__ == '__main__':
	while True:
		try:
			l = StdOutListener()
			auth = OAuthHandler(TwitterAuth.consumer_key, TwitterAuth.consumer_secret)
			auth.set_access_token(TwitterAuth.access_token, TwitterAuth.access_token_secret)
			twitterStream = Stream(auth, l)
			twitterStream.filter(track=tracking, stall_warnings=True)

		except KeyboardInterrupt:
			#User pressed ctrl+c or cmd+c -- get ready to exit the program
			l.close()
			twitterStream.disconnect()
			break
		except IncompleteRead:
		# Oh well, reconnect and keep trucking
			continue
		except Exception:
			pass

#Close the file to store edges output
# c.close()
