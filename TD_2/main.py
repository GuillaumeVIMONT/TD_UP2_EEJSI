#import library
from __future__ import absolute_import, print_function
from http.client import IncompleteRead
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import time
import json
from generate_graph import create_graph
from window_reservoir_sampling_edges import reservoir_sampling_window_stream
import math
# import csv
import datetime
from config import TwitterAuth
import sys

# Get date
now = datetime.datetime.now()

print("Before start Twitter capture we need some informations")
# Reservoir Sampling Size
window_k = input("1/5 Please enter number of edges in the reservoir (eg 200): ")
window_k = int(window_k)
# Lamb size window reservoir
window_sliding = input("2/5 Please enter lamb in minutes(eg 10): ")
window_sliding = int(window_sliding)*60000

# tau size window reservoir
global export_time
export_time = input("3/5 Please enter tau in minutes  (eg 2): ")
export_time = int(export_time)*60000
rate=int(window_sliding/export_time)
if isinstance(rate, int):
	pass
else:
	export_time = input("3/5 Your tau is not a multiple of lamb, please select a multiple of lamb: ")
	export_time = int(export_time)*60000
# tracking Twitter Stream
keywords_input = input("4/5 Please enter tracking word (eg CNN) if multi keywords (eg CNN Foxnews): ")
tracking = []
keywords_input = list(keywords_input.split(" "))
for j in keywords_input:
	tracking.append(str(j))
# tracking = []
# tracking.append(input("4/5 Please enter tracking word (eg CNN): "))
# Timeout Twitter stream
timeout = input("5/5 Please enter duration of the capture in minutes (eg 30): ")
timeout = int(timeout)*60000
start = int(round(time.time() * 1000))

threshold = input("6/6 Please enter threshold components size for the export file (eg 5): ")
threshold = int(threshold)

print("Capture in progress")

window_counter = 0

# c = csv.writer(open("data/%s_%s_edges_full.csv" % (now.strftime("%Y_%m_%d"), tracking[0]), "a"))
# csv_header_full = ("Source", "Target", "Timestamp")
# c.writerow(csv_header_full)

global initial_time
initial_time = 0

class StdOutListener(StreamListener):

	""" A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
	"""

	def on_data(self, data):
		global initial_time, window_k, window_sliding, export_time, window_counter
		all_data = json.loads(data)
		twitter_edges_graph = create_graph(data)
		if len(twitter_edges_graph) > 0:
			for edge in twitter_edges_graph:
				if tracking[0] in edge[1].lower():
					remove(edge)
					pass
				else:
					# c.writerow(edge)
					window_reservoir_sampling = reservoir_sampling_window_stream(edge, window_k, window_sliding, export_time, threshold, tracking)
		if time.time()*1000 > start + timeout:
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
