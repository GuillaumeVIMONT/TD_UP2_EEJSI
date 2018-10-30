import json
import time

def create_graph(data):
	edge_list = []
	hashtags_list = []
	user_mentions_list = []
	all_data = json.loads(data)
	user_screen_name = all_data['user']['screen_name']
	timestamp_ms = all_data['timestamp_ms']
	if len(all_data['entities']['hashtags']) > 0:
		a=0
		for i in all_data['entities']['hashtags']:
			hashtags_list.append(all_data['entities']['hashtags'][a]['text'])
			a+=1
		a=0
	if len(all_data['entities']['user_mentions']) > 0:
		b=0
		for i in all_data['entities']['user_mentions']:
			user_mentions_list.append(all_data['entities']['user_mentions'][b]['screen_name'])
			b+=1
		b=0
	if len(hashtags_list) > 0:
		for i in hashtags_list:
			edge_list.append((user_screen_name, "#"+i, timestamp_ms))
	if len(user_mentions_list) > 0:
		for i in user_mentions_list:
			edge_list.append((user_screen_name, i, timestamp_ms))
	return edge_list
