import streamlit as st
import streamlit_antd_components as sac
import datetime
import uuid
import base64
from db import save_memory

TAGS = ["Trip", "Anniversary", "Milestone", "Funny", "Everyday", "Special"]

def show():
    st.markdown("## 📸 Memories")

    memories = st.session_state.get('memories', [])

    # ── Upload new memory ─────────────────────────────────
    with st.expander("➕ Add a Memory", expanded=False):
        with st.form("add_memory_form"):
            title = st.text_input("Title")
            note = st.text_area("Description", height=80)
            mem_date = st.date_input("Date", value=datetime.date.today())
            tags = sac.chip(items=TAGS, label="Tags", multiple=True, key="mem_tags")
            photo = st.file_uploader("Photo (optional)", type=["jpg", "jpeg", "png"])
            submitted = st.form_submit_button("Save Memory 💾")

            if submitted and title:
                photo_b64 = None
                if photo:
                    photo_b64 = base64.b64encode(photo.read()).decode()

                item = {
                    "id": str(uuid.uuid4()),
                    "title": title,
                    "note": note,
                    "date": str(mem_date),
                    "tags": tags or [],
                    "photo": photo_b64,
                    "author": st.session_state.username,
                }
                save_memory(item)
                st.session_state.memories.append(item)
                st.success(f"Memory '{title}' saved!")
                st.rerun()

    sac.divider(label="Gallery", icon="images", align="center")

    if not memories:
        st.info("No memories yet — add your first one above!")
        return

    sorted_mems = sorted(memories, key=lambda x: x["date"], reverse=True)

    # ── Photo grid (3 per row) ────────────────────────────
    for i in range(0, len(sorted_mems), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j >= len(sorted_mems):
                break
            mem = sorted_mems[i + j]
            with cols[j]:
                if mem.get("photo"):
                    img_bytes = base64.b64decode(mem["photo"])
                    st.image(img_bytes, width=300)
                else:
                    st.markdown(
                        "<div style='height:140px;background:#fce4ec;border-radius:8px;"
                        "display:flex;align-items:center;justify-content:center;"
                        "font-size:40px'>📷</div>",
                        unsafe_allow_html=True
                    )
                st.markdown(f"**{mem['title']}**")
                st.caption(mem["date"])
                for tag in mem.get("tags", []):
                    st.markdown(
                        f"<span style='background:#fce4ec;color:#c2185b;padding:2px 6px;"
                        f"border-radius:10px;font-size:11px;margin-right:3px'>{tag}</span>",
                        unsafe_allow_html=True
                    )
                if st.button("View", key=f"mem_{mem['id']}"):
                    st.session_state.selected_memory = mem["id"]
                    st.rerun()

    # ── Full memory modal ─────────────────────────────────
    if "selected_memory" in st.session_state:
        mem = next((m for m in memories if m["id"] == st.session_state.selected_memory), None)
        if mem:
            with st.expander("📖 Memory Detail", expanded=True):
                if mem.get("photo"):
                    st.image(base64.b64decode(mem["photo"]), width=600)
                st.markdown(f"### {mem['title']}")
                st.caption(f"{mem['date']} · by {mem.get('author', '')}")
                st.write(mem.get("note", ""))
                if st.button("Close", key="close_mem"):
                    del st.session_state.selected_memory
                    st.rerun()
