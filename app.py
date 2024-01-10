from numpy import empty
import streamlit as st
from datetime import datetime, time
import time as t
import base64
import pytz
import urllib3
import pandas as pd


# normal = {
#     'be': ['08:00:00', '08:50:00', '09:50:00', '10:50:00', '11:45:00', '12:40:00', '13:30:00', '14:20:00'],
#     'ki': ['08:45:00', '09:40:00', '10:35:00', '11:35:00', '12:30:00', '13:25:00', '14:15:00', '15:05:00']
# }

# rovid = {
#     'be': ['08:00:00', '08:40:00', '09:20:00', '10:00:00', '10:40:00', '11:20:00', '11:55:00', '12:30:00'],
#     'ki': ['08:30:00', '09:10:00', '09:50:00', '10:30:00', '11:10:00', '11:50:00', '12:25:00', '13:00:00']
# }


normal = {
    'be': [time(8, 0, 0), time(8, 50, 0), time(9, 50, 0), time(10, 50, 0), time(11, 45, 0), time(12, 45, 0), time(13, 30, 0), time(14, 20, 0)],
    'ki': [time(8, 45, 0), time(9, 40, 0), time(10, 35, 0), time(11, 35, 0), time(12, 30, 0), time(13, 25, 0), time(14, 15, 0), time(15, 5, 0)]
}

rovid = {
    'be': [time(8, 0, 0), time(8, 40, 0), time(9, 20, 0), time(10, 0, 0), time(10, 40, 0), time(11, 20, 0), time(11, 55, 0), time(12, 30, 0)],
    'ki': [time(8, 30, 0), time(9, 10, 0), time(9, 50, 0), time(10, 30, 0), time(11, 10, 0), time(11, 50, 0), time(12, 25, 0), time(13, 0, 0)]
}


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


def load_sound(url):
    http = urllib3.PoolManager()
    data = http.request("GET", url, preload_content=False).read()
    b64 = base64.b64encode(data).decode()
    return b64


be_hang = load_sound(
    'https://raw.githubusercontent.com/mollac/st_ringer/master/be.mp3')
ki_hang = load_sound(
    'https://raw.githubusercontent.com/mollac/st_ringer/master/ki.mp3')


def st_css(item, value):
    st.markdown(f'<style>{item}{value}</style>', unsafe_allow_html=True)


st_css(".blank", "{display:none}")
st_css(
    "h1", "{text-align: center; font-size:3.5rem; color: rgba(184,183,143,0.8)}")
st_css(
    "h2", "{text-align: center; font-size:2.5rem; color: rgba(154,163,173,0.8)}")
st_css("p", "{text-align: center; font-size:1rem}")
st_css('div[data-testid="stMetric"]', '''{background-color: rgba(28, 131, 225, 0.1);
			border: 1px solid rgba(28, 131, 225, 0.1);
			padding: 5% 5% 5% 5%;
			border-radius: 5px;
			color: rgb(30, 103, 119);
			overflow-wrap: break-word;
            text-align: center;
            margin: auto;
            width: 60%
		}''')

st_css('div[data-testid="stMetric"] label',
       '{width: fit-content; margin: auto; font-size:2rem;')
st_css('div[data-testid="stMetric"] p',
       '{width: fit-content; margin: auto; font-size:2rem;')


st.write('# Csengető program')

with st.expander("Csengetési rend", False):
    c1, c2 = st.columns(2)
    c1.write('Normál')
    c2.write('Rövidített')
    normal = c1.data_editor(normal,
                            column_config={
                                "be": st.column_config.TimeColumn(
                                    "Becsengetés",
                                    min_value=time(8, 0, 0),
                                    max_value=time(16, 0, 0),
                                    format="hh:mm:ss"
                                ),
                            },
                            width=300)

    rovid = c2.data_editor(rovid, width=300)

time_div = st.empty()
msg_div = st.empty()
debug = st.empty()


csengetes = st.sidebar.radio(
    "Alkalkmazott csengetési rend",
    ["Normál", "Rövidített"], horizontal=True)

if csengetes == 'Normál':
    csengetesi_rend = normal
else:
    csengetesi_rend = rovid

if st.sidebar.toggle('Start'):
    while True:
        now = datetime.now(pytz.timezone('Europe/Budapest'))
        current_time = time(now.hour, now.minute, now.second)
        time_div.title(current_time)

        for i in range(len(csengetesi_rend['be'])):
            start_time = csengetesi_rend['be'][i].strftime("%H:%M:%S")
            end_time = csengetesi_rend['ki'][i].strftime("%H:%M:%S")
            if start_time < current_time.strftime("%H:%M:%S") < end_time:
                msg_div.metric(
                    label=f'{i+1}.óra', value=f'{start_time[:5]} - {end_time[:5]}')
                # msg_div.markdown(
                #     f'## *{i+1}. óra:* **{start_time[:5]} - {end_time[:5]}**')
                break
            else:
                # msg_div.header(f'SZÜNET')
                msg_div.metric(label='10 perc', value='SZÜNET')

        if current_time in csengetesi_rend['be']:
            autoplay_audio(be_hang)
        elif current_time in csengetesi_rend['ki']:
            autoplay_audio(ki_hang)

        t.sleep(1)
