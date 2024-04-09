
import requests
import streamlit as st



def get_battlelog(player_tag, my_key):
    api_url = f'https://proxy.royaleapi.dev/v1/players/%23{player_tag[1:]}/battlelog'
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
    

my_key = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjlhNTEwOTIxLTQ1MjItNDY1ZC05NzZkLWNlMjMxMDY3ZjdjMCIsImlhdCI6MTcxMjY3NjI0MCwic3ViIjoiZGV2ZWxvcGVyL2MxNGEwOGRiLTZiMmQtYTc5OC02YTc2LWJlZDcwN2JjNzAxMiIsInNjb3BlcyI6WyJicmF3bHN0YXJzIl0sImxpbWl0cyI6W3sidGllciI6ImRldmVsb3Blci9zaWx2ZXIiLCJ0eXBlIjoidGhyb3R0bGluZyJ9LHsiY2lkcnMiOlsiNDUuNzkuMjE4Ljc5IiwiMTU4LjQyLjE3Mi4yOCJdLCJ0eXBlIjoiY2xpZW50In1dfQ.PCo3Gb06f-yZbBnlDqPSgOw8bSOhmQl_aIhhtmnqSYHyROMHhDCapveTqjK7A3tXmMvdRCVXJLH3FuwweTgl7Q'



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

player_name = 'Desi'    # PROVISIONAL





import socket

def get_ip_address():
    try:
        # Crear un socket UDP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Conectar a un servidor DNS para obtener la dirección IP
        s.connect(("8.8.8.8", 80))
        # Obtener la dirección IP del socket
        ip_address = s.getsockname()[0]
        # Cerrar el socket
        s.close()
        return ip_address
    except socket.error as e:
        st.text(e)
        return None

# Obtener y mostrar la dirección IP
ip_address = get_ip_address()
if ip_address:
    st.text(ip_address)
else:
    st.text("No se pudo obtener la dirección IP.")





if player_name[0] == '#':
    player_tag = player_name
else:
    player_tag = pred_players[player_name]
    
print(player_tag)

battles = get_battlelog(player_tag, my_key)

st.text(battles)























