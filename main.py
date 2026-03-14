import streamlit as st
import os
from dotenv import load_dotenv
from streamlit_option_menu import option_menu
from db import load_letters, load_memories, load_dates

load_dotenv()

user1 = os.getenv('USER_1')
user2 = os.getenv('USER_2')
share = os.getenv('SHARE')
pass1 = os.getenv('PASSWORD_1')
pass2 = os.getenv('PASSWORD_2')
password = os.getenv('PASSWORD')

st.set_page_config(page_title="Our Space 💕", page_icon="💕", layout="wide")

USERS = {
    share: password,
    user1: pass1,
    user2: pass2,
}

# ── Auth ──────────────────────────────────────────────────
def login(username, pwd):
    if USERS.get(username) == pwd:
        st.session_state.logged_in = True
        st.session_state.username = username
        return True
    return False

def logout():
    st.session_state.logged_in = False
    st.session_state.username = ""
    for key in ['letters', 'memories', 'dates']:
        st.session_state.pop(key, None)

# ── Session defaults ──────────────────────────────────────
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""

# ── Login page ────────────────────────────────────────────
if not st.session_state.logged_in:
    st.markdown("<h1 style='text-align:center'>💕 Our Space</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align:center;color:#888'>A private space for the two of us</p>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        with st.form("login_form"):
            username = st.text_input("Username")
            pwd = st.text_input("Password", type="password")
            if st.form_submit_button("Login 💌"):
                if login(username, pwd):
                    st.rerun()
                else:
                    st.error("Wrong username or password")
    st.stop()

# ── Load data once per session ────────────────────────────
if 'letters' not in st.session_state:
    st.session_state.letters = load_letters()
if 'memories' not in st.session_state:
    st.session_state.memories = load_memories()
if 'dates' not in st.session_state:
    st.session_state.dates = load_dates()

# ── Sidebar styling ───────────────────────────────────────
st.markdown("""
<style>
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #fff0f5 0%, #fce4ec 100%);
}
[data-testid="stSidebar"] * {
    font-family: 'Georgia', serif;
}
</style>
""", unsafe_allow_html=True)

# ── Sidebar nav ───────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style="text-align:center;padding:12px 0 4px">
        <div style="font-size:36px">💕</div>
        <div style="font-family:'Georgia',serif;font-size:20px;
                    color:#c2185b;font-weight:bold;letter-spacing:1px">
            Our Space
        </div>
        <div style="font-size:13px;color:#e91e8c;margin-top:4px">
            hey, {st.session_state.username} 🌸
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

    page = option_menu(
        menu_title=None,
        options=["Home", "Dates", "Memories", "Letters", "Timeline"],
        icons=["house-heart", "calendar-heart", "images", "envelope-heart", "clock-history"],
        default_index=0,
        styles={
            "container": {"background-color": "transparent", "padding": "0"},
            "icon": {"color": "#e91e8c", "font-size": "16px"},
            "nav-link": {
                "font-family": "Georgia, serif",
                "font-size": "15px",
                "color": "#880e4f",
                "border-radius": "10px",
                "margin": "2px 0",
            },
            "nav-link-selected": {
                "background-color": "#f8bbd0",
                "color": "#880e4f",
                "font-weight": "bold",
            },
        }
    )

    st.markdown("---")
    if st.button("🚪 Logout", use_container_width=True):
        logout()
        st.rerun()

# ── Route to pages ────────────────────────────────────────
if page == "Home":
    from views.home import show
    show()
elif page == "Dates":
    from views.dates import show
    show()
elif page == "Memories":
    from views.memories import show
    show()
elif page == "Letters":
    from views.letters import show
    show()
elif page == "Timeline":
    from views.timeline import show
    show()
