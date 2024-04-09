
import requests
import streamlit as st



def get_battlelog(player_tag, my_key):
    api_url = f'https://bsproxy.royaleapi.dev/v1/players/%23{player_tag[1:]}/battlelog'
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
        st.text(e)
        return None
    

my_key = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjM5YTc5ZTg0LWZkN2YtNDk5Ny05ZDlhLWU4ODNmZDg4M2QxMyIsImlhdCI6MTcxMjY3NjQ3MCwic3ViIjoiZGV2ZWxvcGVyL2MxNGEwOGRiLTZiMmQtYTc5OC02YTc2LWJlZDcwN2JjNzAxMiIsInNjb3BlcyI6WyJicmF3bHN0YXJzIl0sImxpbWl0cyI6W3sidGllciI6ImRldmVsb3Blci9zaWx2ZXIiLCJ0eXBlIjoidGhyb3R0bGluZyJ9LHsiY2lkcnMiOlsiNDUuNzkuMjE4Ljc5Il0sInR5cGUiOiJjbGllbnQifV19.SM4iXgIPt5rp0F2pCPrWfSIW372OUr-0HkpmmRT1TXDkuTs2wrvV0gTLts-SaPO7h4D7Oqi9ON1srumGEk9C9g'


# CONFIGURACIÓN DE LA WEB
st.set_page_config(layout="wide", page_title="Liga Terraplanista")

pred_players = {'Matías': '#YGG02LP0',
                'Merto': '#298QCP0L8',
                'Gustabo': '#20LC9VGP',
                'Javi': '#280RP8PQ2', 
                'Oscarabajo': '#YVLPG0G',
                'Chino': '#YY88RLL0',
                'Antonio Reverte': '#YGUGQ0GU',
                'Desi': '#CLG2RRC9'}

player_name = st.selectbox('Jugador', pred_players.keys(), index=1)


if player_name[0] == '#':
    player_tag = player_name
else:
    player_tag = pred_players[player_name]
    

try:
    battles = get_battlelog(player_tag, my_key)['items']
except:
    print('Nada que mostrar...')


st.text(f'En las últimas {len(battles)} partidas...')



modes = {}
brawlers = {}
results = {}
players = {}
trophies = 0

for battle in battles:
    time = battle['battleTime']
    mode = battle['battle']['mode']
    if mode in modes:
        modes[mode] += 1
    else:
        modes[mode] = 1
    
    if mode == 'soloShowdown':
        for player in battle['battle']['players']:
            if player['tag'] == player_tag:
                continue
            if player['tag'] in players.keys():
                players[player['tag']][1] += 1
            else:
                players[player['tag']] = [player['name'], 1]
    else:
        for player in battle['battle']['teams'][0] + battle['battle']['teams'][1]:
            if player['tag'] == player_tag:
                continue
            if player['tag'] in players.keys():
                players[player['tag']][1] += 1
            else:
                players[player['tag']] = [player['name'], 1]
    
    try:
        trophies += int(battle['battle']['trophyChange'])
    except:
        pass
    
    try:
        result = battle['battle']['rank']
    except:
        result = battle['battle']['result']
    if result in results:
        results[result] += 1
    else:
        results[result] = 1


st.text(trophies)



















