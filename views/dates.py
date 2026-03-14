import streamlit as st
import streamlit_antd_components as sac
import datetime
import uuid
from streamlit_calendar import calendar
from db import save_date

TAGS = ["Anniversary", "Milestone", "Trip", "Funny", "First", "Special"]

def show():
    st.markdown("## 📅 Our Dates")

    dates = st.session_state.get('dates', [])

    # ── Calendar view ─────────────────────────────────────
    sac.divider(label="Calendar", icon="calendar", align="center")

    events = [
        {
            "title": d["title"],
            "start": d["date"],
            "color": "#e91e8c",
        }
        for d in dates
    ]
    calendar(events=events, options={"initialView": "dayGridMonth"}, key="dates_cal")

    # ── Add new date ──────────────────────────────────────
    sac.divider(label="Add a Date", icon="plus-circle", align="center")

    with st.form("add_date_form"):
        title = st.text_input("Title (e.g. First Trip to Bali)")
        date = st.date_input("Date", value=datetime.date.today())
        tags = sac.chip(
            items=TAGS,
            label="Tags",
            multiple=True,
            key="date_tags"
        )
        note = st.text_area("Notes (optional)", height=80)
        submitted = st.form_submit_button("Save Date 💾")

        if submitted and title:
            item = {
                "id": str(uuid.uuid4()),
                "title": title,
                "date": str(date),
                "tags": tags or [],
                "note": note,
                "author": st.session_state.username,
            }
            save_date(item)
            st.session_state.dates.append(item)
            st.success(f"'{title}' saved!")
            st.rerun()

    # ── Date list ─────────────────────────────────────────
    sac.divider(label="All Dates", icon="list", align="center")

    if not dates:
        st.info("No dates yet — add your first one above!")
        return

    sorted_dates = sorted(dates, key=lambda x: x["date"], reverse=True)
    for d in sorted_dates:
        with st.container():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**{d['title']}** — {d['date']}")
                if d.get("note"):
                    st.caption(d["note"])
            with col2:
                for tag in d.get("tags", []):
                    st.markdown(
                        f"<span style='background:#fce4ec;color:#c2185b;padding:2px 8px;"
                        f"border-radius:12px;font-size:12px;margin-right:4px'>{tag}</span>",
                        unsafe_allow_html=True
                    )
        st.markdown("---")
