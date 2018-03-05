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

# Get date
now = datetime.datetime.now()

# Reservoir Sampling Size
window_k = 400
window_sliding = int(1800000)

# Target Twitter Stream
tracking = ["bitcoin"]
languages = ["en"] # fr
window_counter = 0
c = csv.writer(open("data/%s_%s_edges_full.csv" % (now.strftime("%Y_%m_%d"), tracking[0]), "a"))
csv_header_full = ("Source", "Target", "Timestamp")
c.writerow(csv_header_full)


#consumer key, consumer secret, access token, access secret for OAuth Twitter.
consumer_key="MfKJZNJdN2cVM6Ka8xmF8Smbk"
consumer_secret="KtpAZ0sK0HdpVphCryNWTlmWwnm97X3rovkrCwOOOtGbVL2Zfo"
access_token="2207034565-3LYXBvDdzeDMXpmM4i3APZkG6qW6UGeTc8xQKHe"
access_token_secret="3jyb0b9f5gGA8sTJbq2j5IWwDAEBC7G0EBMYvb8WIpONQ"

global initial_time
initial_time = 0

class StdOutListener(StreamListener):

	""" A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
	"""

	def on_data(self, data):
		all_data = json.loads(data)
		try:
			twitter_edges_graph = create_graph(data)
			for edge in twitter_edges_graph:
				if tracking[0] in edge[1].lower():
					remove(edge)
					pass
				else:
					c.writerow(edge)
					window_reservoir_sampling = reservoir_sampling_window_stream(edge, window_k, window_sliding)
					print(window_reservoir_sampling)

		except:
			pass
		try:
			millis = round(time.time() * 1000)
			if millis > initial_time:
				print("15min")
				new_time = int(millis)+int(1)
				global initial_time
				initial_time = new_time
				global window_counter
				t = csv.writer(open("data/%s_%s_window_reservoir_edges_%s.csv" % (now.strftime("%Y_%m_%d"), tracking[0], window_counter), "a"))
				csv_header_window = ("Source", "Target", "Timestamp", "Window")
				t.writerow(csv_header_window)
				for i in window_reservoir_sampling:
					for edge in i:
						t.writerow(edge)
				window_counter+=1
		except:
			pass
		return True


	def on_error(self, status_code):
		if status_code == 420:
			#returning False in on_data disconnects the stream
			return False
    


if __name__ == '__main__':
	while True:
		try:
			l = StdOutListener()
			auth = OAuthHandler(consumer_key, consumer_secret)
			auth.set_access_token(access_token, access_token_secret)
			twitterStream = Stream(auth, l)
			twitterStream.filter(track=tracking, languages=languages, stall_warnings=True)

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