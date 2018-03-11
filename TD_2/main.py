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
import csv
import datetime
from config import TwitterAuth

# Get date
now = datetime.datetime.now()

# Reservoir Sampling Size

window_k = input("Please enter window reservoir size (eg 200) : ")
window_k = int(window_k)

window_sliding = input("Please enter window sliding in minutes(eg 10) : ")
window_sliding = int(window_sliding)*60000

global export_time
export_time = input("Please enter export window reservoir time in minutes  (eg 2) : ")
export_time = int(export_time)*60000
# Target Twitter Stream
tracking = []
tracking.append(input("Please enter tracking word (eg CNN) : "))

print("Capture in progress")

window_counter = 0

c = csv.writer(open("data/%s_%s_edges_full.csv" % (now.strftime("%Y_%m_%d"), tracking[0]), "a"))
csv_header_full = ("Source", "Target", "Timestamp")
c.writerow(csv_header_full)

global initial_time
initial_time = 0

class StdOutListener(StreamListener):

	""" A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
	"""

	def on_data(self, data):
		all_data = json.loads(data)
		twitter_edges_graph = create_graph(data)
		if len(twitter_edges_graph) > 0:
			for edge in twitter_edges_graph:
				if tracking[0] in edge[1].lower():
					remove(edge)
					pass
				else:
					c.writerow(edge)
					window_reservoir_sampling = reservoir_sampling_window_stream(edge, window_k, window_sliding)
					print(window_reservoir_sampling)
			millis = round(time.time() * 1000)
			global initial_time
			global export_time
			if millis > initial_time:
				initial_time = int(millis)+int(export_time)
				global window_counter
				t = csv.writer(open("data/%s_%s_window_reservoir_edges_%s.csv" % (now.strftime("%Y_%m_%d"), tracking[0], window_counter), "a"))
				csv_header_window = ("Source", "Target", "Timestamp", "Window")
				t.writerow(csv_header_window)
				for i in window_reservoir_sampling:
					for edge in i:
						t.writerow(edge)
				window_counter+=1
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
c.close()
t.close()
