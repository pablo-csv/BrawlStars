
import requests
import streamlit as st
import json
import base64



# Define la función para descargar los datos en formato JSON o TXT
def descargar_datos(data, filename, format):
    if format == "JSON":
        formatted_data = json.dumps(data, indent=4)
        mime_type = "file/json"
        file_extension = "json"
    elif format == "TXT":
        formatted_data = '\n'.join([f"{k}: {v}" for d in data for k, v in d.items()])
        mime_type = "file/txt"
        file_extension = "txt"
    else:
        st.error("Formato no válido")
        return

    b64 = base64.b64encode(formatted_data.encode()).decode()
    href = f'<a href="data:{mime_type};base64,{b64}" download="{filename}.{file_extension}">Descargar {format}</a>'
    st.markdown(href, unsafe_allow_html=True)


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
                'Oscarabajo': '#YVLPG0G',
                'Chino': '#YY88RLL0',
                'Desi': '#CLG2RRC9'}

player_name = st.selectbox('Jugador (en modo ordenador, también admite tags empezados por # de jugadores no predeterminados)', pred_players.keys(), index=1)


if player_name[0] == '#':
    player_tag = player_name
else:
    player_tag = pred_players[player_name]
    

try:
    battles = get_battlelog(player_tag, my_key)['items']
except:
    print('Nada que mostrar...')



modes = {}
brawlers = {}
results = {'victory': 0, 'defeat': 0}
players = {}
trophies_won = 0
trophies_lost = 0

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
                brawler = player['brawler']['name']
                continue
            if player['tag'] in players.keys():
                players[player['tag']][1] += 1
            else:
                players[player['tag']] = [player['name'], 1]
    else:
        for player in battle['battle']['teams'][0] + battle['battle']['teams'][1]:
            if player['tag'] == player_tag:
                brawler = player['brawler']['name']
                continue
            if player['tag'] in players.keys():
                players[player['tag']][1] += 1
            else:
                players[player['tag']] = [player['name'], 1]

    try:
        if brawler in brawlers:
            brawlers[brawler] += 1
        else:
            brawlers[brawler] = 1
    except:
        pass
    
    try:
        trophies = int(battle['battle']['trophyChange'])
        if trophies > 0:
            trophies_won += trophies
        elif trophies < 0:
            trophies_lost -= trophies
    except:
        pass
    
    try:
        result = str(battle['battle']['rank'])
    except:
        result = battle['battle']['result']
    if result in results:
        results[result] += 1
    else:
        results[result] = 1


st.text(f'En las últimas {len(battles)} partidas...')

st.write(' ')

st.write(f'  Trofeos ganados: {trophies_won}')
st.write(f'  Trofeos perdidos: {trophies_lost}')
if (trophies_won - trophies_lost) >= 0:
    st.write(f'  Balance de trofeos: +{trophies_won - trophies_lost} ☝️🤓')
else:
    st.write(f'  Balance de trofeos: {trophies_won - trophies_lost} 😂')

st.write(' ')

st.text('En modos de equipo:')
st.write(f"  {results['victory']} victorias")
st.write(f"  {results['defeat']} derrotas")

st.write(' ')

st.text('En modos individuales:')
for rank, number in dict(sorted(results.items())).items():
    if len(rank) == 1:
        if number == 1:
            st.write(f"  Puesto {rank}: {number} vez")
        else:
            st.write(f"  Puesto {rank}: {number} veces")

st.write(' ')

st.text('Jugadores favoritos:')
for player, info in players.items():
    if info[1] >= 2:
        st.write(f'{info[0]}: {info[1]} partidas compartidas')

st.write(' ')

st.text('Modos favoritos:')
for mode, number in modes.items():
    if number == 1:
        st.write(f'{mode}: jugado {number} vez')
    else:
        st.write(f'{mode}: jugado {number} veces')

st.write(' ')

st.text('Brawlers favoritos:')
for brawler, number in brawlers.items():
    if number == 1:
        st.write(f'{brawler}: {number} partida')
    else:
        st.write(f'{brawler}: {number} partidas')


st.write(' ')
st.write(' ')

# Botones para descargar los datos en diferentes formatos
formato = st.selectbox("Selecciona el formato de descarga:", ["JSON", "TXT"])
if st.button(f"Descargar datos en formato {formato}"):
    descargar_datos(battles, f"partidas_{player_tag}", formato)
















