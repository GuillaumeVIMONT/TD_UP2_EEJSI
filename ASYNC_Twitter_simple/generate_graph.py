import json

def create_graph(data):
    all_data = dict(data)
    edge_list = []
    user_screen_name = all_data['user']['screen_name']
    timestamp_ms = all_data['timestamp_ms']
    if len(all_data['entities']['hashtags']) > 0:
        for index, i in enumerate(all_data['entities']['hashtags']):
            edge_list.append(("@"+user_screen_name, "#"+all_data['entities']['hashtags'][index]['text'], timestamp_ms))
    if len(all_data['entities']['user_mentions']) > 0:
        for index, i in enumerate(all_data['entities']['user_mentions']):
            edge_list.append(("@"+user_screen_name, "@"+all_data['entities']['user_mentions'][index]['screen_name'], timestamp_ms))
    return edge_list