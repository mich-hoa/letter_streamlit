import streamlit as st
import datetime
from streamlit_lottie import st_lottie
import requests

RELATIONSHIP_START = datetime.date(2023, 1, 1)  # update this to your actual date

def load_lottie(url):
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()
    return None

def show():
    st.markdown("<h1 style='text-align:center'>💕 Our Space</h1>", unsafe_allow_html=True)

    # Lottie heart animation
    lottie = load_lottie("https://assets2.lottiefiles.com/packages/lf20_yd8fbnml.json")
    if lottie:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st_lottie(lottie, height=200, key="heart")

    st.markdown("---")

    # Days together counter
    today = datetime.date.today()
    days = (today - RELATIONSHIP_START).days
    col1, col2 = st.columns(2)
    with col1:
        st.metric("💑 Days Together", f"{days} days")

    # Next upcoming date
    with col2:
        dates = st.session_state.get('dates', [])
        upcoming = [
            d for d in dates
            if datetime.date.fromisoformat(d['date']) >= today
        ]
        if upcoming:
            upcoming.sort(key=lambda x: x['date'])
            next_date = upcoming[0]
            days_until = (datetime.date.fromisoformat(next_date['date']) - today).days
            st.metric("📅 Next Date", next_date['title'], delta=f"in {days_until} days")
        else:
            st.metric("📅 Next Date", "None planned yet")
