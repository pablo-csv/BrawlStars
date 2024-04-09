
import requests
import streamlit as st

def get_battlelog(player_tag, my_key):
    api_url = f'https://api.brawlstars.com/v1/players/%23{player_tag[1:]}/battlelog'
    headers = {
        'Authorization': f'Bearer {my_key}',
        'Accept': 'application/json'
    }
    
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()  # Raise an exception for 4XX or 5XX errors
        battlelog = response.json()
        return battlelog
    except requests.exceptions.RequestException as e:
        print("Error:", e)
        return None
    

my_key = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImY3ZDcyYzA0LTYyY2YtNGU5Yy1iMDE5LTA4Y2IzYzg5ZWYwMSIsImlhdCI6MTcxMjY3Mjc0Miwic3ViIjoiZGV2ZWxvcGVyL2MxNGEwOGRiLTZiMmQtYTc5OC02YTc2LWJlZDcwN2JjNzAxMiIsInNjb3BlcyI6WyJicmF3bHN0YXJzIl0sImxpbWl0cyI6W3sidGllciI6ImRldmVsb3Blci9zaWx2ZXIiLCJ0eXBlIjoidGhyb3R0bGluZyJ9LHsiY2lkcnMiOlsiMTU4LjQyLjE3Mi4yOCJdLCJ0eXBlIjoiY2xpZW50In1dfQ.e2DU_v7pfH5nRIEC1Sh5J95oQ1AKvqx1wJegsddGdOpA9eJN2ce1hp3q6S2T1-NNUW_T4u1-pBLstGg8elMsyg'



# CONFIGURACIÓN DE LA WEB
st.set_page_config(layout="wide", page_title="Liga Terraplanista")

player_name = st.selectbox('Jugador', pred_players.keys(), index=1)


pred_players = {'Matías': '#YGG02LP0',
                'Merto': '#298QCP0L8',
                'Gustabo': '#20LC9VGP',
                'Javi': '#280RP8PQ2', 
                'Oscarabajo': '#YVLPG0G',
                'Chino': '#YY88RLL0',
                'Antonio Reverte': '#YGUGQ0GU',
                'Desi': '#CLG2RRC9'}

player_name = 'Desi'    # PROVISIONAL

if player_name[0] == '#':
    player_tag = player_name
else:
    player_tag = pred_players[player_name]
    
print(player_tag)

battles = get_battlelog(player_tag, my_key)

print(battles)























