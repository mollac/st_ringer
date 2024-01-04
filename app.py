from numpy import empty
import streamlit as st
import time
from datetime import datetime
import base64
import pytz
import urllib3


normal = {
    'be': ['08:00:00', '08:50:00', '09:50:00', '10:50:00', '11:45:00', '12:40:00', '13:30:00', '14:20:00'],
    'ki': ['08:45:00', '09:40:00', '10:35:00', '11:35:00', '12:30:00', '13:25:00', '14:15:00', '15:05:00']
}
rovid = {
    'be': ['08:00:00', '08:40:00', '09:20:00', '10:00:00', '10:40:00', '11:20:00', '11:55:00', '12:30:00'],
    'ki': ['08:30:00', '09:10:00', '09:50:00', '10:30:00', '11:10:00', '11:50:00', '12:25:00', '13:00:00']
}


def load_sound(url):
    http = urllib3.PoolManager()
    data = http.request("GET", url, preload_content=False).read()
    b64 = base64.b64encode(data).decode()
    return b64


def autoplay_audio(audio):
    md = f"""
    <div class="blank">
        <audio controls autoplay="true">
        <source src="data:audio/mp3;base64,{audio}" type="audio/mp3">
        </audio>
    </div>
    """

    st.markdown(
        md,
        unsafe_allow_html=True
    )


def st_css(item, value):
    st.markdown(f'<style>{item}{value}</style>', unsafe_allow_html=True)


# st_css("a", "{text-decoration:none;}")
# st_css("a:hover", "{text-decoration:none; color:red;")
# # st_css("#MainMenu", "{visibility: hidden;}")
# st_css("footer", "{visibility: visible}")
# st_css(".css-12oz5g7", "{padding-top: 0rem;}")
# st_css("tbody th", "{display:none}")
st_css(".blank", "{display:none}")
st_css("h1", "{text-align: center; font-size:4.5rem}")
st_css("p", "{text-align: center; font-size:1rem}")

st.write('# Csengető program')
with st.expander("Órabeosztások", False):
    c1, c2 = st.columns(2)
    c1.write('Normál')
    c2.write('Rövidített')
    normal = c1.data_editor(normal, width=300)

    rovid = c2.data_editor(rovid, width=300)

time_div = st.empty()
msg_div = st.empty()


csengetes = st.sidebar.radio(
    "Alkalkmazott csengetési rend",
    ["Normál", "Rövidített"], horizontal=True)

if csengetes == 'Normál':
    csengetesi_rend = normal
else:
    csengetesi_rend = rovid

be_hang = load_sound(
    'https://raw.githubusercontent.com/mollac/st_ringer/master/be.mp3')
ki_hang = load_sound(
    'https://raw.githubusercontent.com/mollac/st_ringer/master/ki.mp3')


if st.sidebar.toggle('Start'):
    while True:
        now = datetime.now(pytz.timezone('Europe/Budapest'))
        current_time = now.strftime("%H:%M:%S")

        time_div.title(current_time)

        if current_time in csengetesi_rend['be']:
            msg_div.header('ÓRA VAN')
            autoplay_audio(be_hang)
        elif current_time in csengetesi_rend['ki']:
            msg_div.header('SZÜNET VAN')
            autoplay_audio(ki_hang)

        time.sleep(1)
