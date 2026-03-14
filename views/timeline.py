import streamlit as st
import streamlit_antd_components as sac
from streamlit_timeline import timeline
import json

def show():
    st.markdown("## ⏳ Our Timeline")

    dates = st.session_state.get('dates', [])
    memories = st.session_state.get('memories', [])

    # Merge dates + memories into timeline events
    events = []

    for d in dates:
        events.append({
            "start_date": {"year": d["date"][:4], "month": d["date"][5:7], "day": d["date"][8:10]},
            "text": {"headline": d["title"], "text": d.get("note", "")},
            "group": "Date",
        })

    for m in memories:
        events.append({
            "start_date": {"year": m["date"][:4], "month": m["date"][5:7], "day": m["date"][8:10]},
            "text": {"headline": m["title"], "text": m.get("note", "")},
            "group": "Memory",
        })

    if not events:
        st.info("No events yet — add some dates or memories first!")
        return

    # Sort by date for the title card
    events.sort(key=lambda x: (
        x["start_date"]["year"],
        x["start_date"]["month"],
        x["start_date"]["day"]
    ))

    timeline_data = {
        "title": {
            "text": {
                "headline": "Our Story 💕",
                "text": "Every moment we've shared together."
            }
        },
        "events": events
    }

    timeline(json.dumps(timeline_data), height=600)
