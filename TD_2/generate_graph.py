import json
import time
#edge = []
def create_graph(data):
    current_milli_time = lambda: int(round(time.time() * 1000))
    edge = []
    all_data = json.loads(data)
    user_screen_name = all_data['user']['screen_name']
    timestamp_ms = all_data['timestamp_ms']
    try:
        hashtags1 = "#"+all_data['entities']['hashtags'][0]['text']
        edge_1 = (user_screen_name, hashtags1, timestamp_ms)
        edge.append((edge_1))
        if 'hashtags1' in locals():
            hashtags2 = "#"+all_data['entities']['hashtags'][1]['text']
            edge_2 = (user_screen_name, hashtags2, timestamp_ms)
            edge.append((edge_2))
            if 'hashtags2' in locals():
                hashtags3 = "#"+all_data['entities']['hashtags'][2]['text']
                edge_3 = (user_screen_name, hashtags3, timestamp_ms)
                edge.append((edge_3))
                if 'hashtags3' in locals():
                    hashtags4 = "#"+all_data['entities']['hashtags'][3]['text']
                    edge_4 = (user_screen_name, hashtags4, timestamp_ms)
                    edge.append((edge_4))
    except:
        pass
    try:
        user_mentions_screen_name1 = all_data['entities']['user_mentions'][0]['screen_name']
        edge_5 = (user_screen_name, user_mentions_screen_name1, timestamp_ms)
        edge.append((edge_5))
        if 'user_mentions_screen_name1' in locals():
            user_mentions_screen_name2 = all_data['entities']['user_mentions'][1]['screen_name']
            edge_6 = (user_screen_name, user_mentions_screen_name2, timestamp_ms)
            edge.append((edge_6))
            if 'user_mentions_screen_name2' in locals():
                user_mentions_screen_name3 = all_data['entities']['user_mentions'][2]['screen_name']
                edge_7 = (user_screen_name, user_mentions_screen_name3, timestamp_ms)
                edge.append((edge_7))
                if 'user_mentions_screen_name3' in locals():
                    user_mentions_screen_name4 = all_data['entities']['user_mentions'][3]['screen_name']
                    edge_8 = (user_screen_name, user_mentions_screen_name4, timestamp_ms)
                    edge.append((edge_8))
    except:
        pass

    return edge