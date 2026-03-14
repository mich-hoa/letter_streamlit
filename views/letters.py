import streamlit as st
import streamlit_antd_components as sac
from streamlit_modal import Modal
import datetime
import uuid
from db import save_letter

TAGS = ["Love", "Apology", "Gratitude", "Funny", "Milestone", "Just Because"]

def show():
    st.markdown("## 💌 Letters")

    letters = st.session_state.get('letters', [])

    # ── Write new letter ──────────────────────────────────
    with st.expander("✍️ Write a New Letter", expanded=False):
        with st.form("letter_form"):
            title = st.text_input("Title")
            recipient = st.text_input("To")
            tags = sac.chip(items=TAGS, label="Tags", multiple=True, key="letter_tags")
            content = st.text_area("Letter Content", height=250)
            submitted = st.form_submit_button("Send Letter 💌")

            if submitted and title and content and recipient:
                item = {
                    "id": str(uuid.uuid4()),
                    "title": title,
                    "content": content,
                    "recipient": recipient,
                    "tags": tags or [],
                    "author": st.session_state.username,
                    "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }
                save_letter(item)
                st.session_state.letters.append(item)
                st.success(f"Letter '{title}' sent!")
                st.rerun()
            elif submitted:
                st.error("Please fill in all fields.")

    sac.divider(label="All Letters", icon="envelope", align="center")

    if not letters:
        st.info("No letters yet — write your first one above!")
        return

    sorted_letters = sorted(letters, key=lambda x: x["date"], reverse=True)

    # ── Letter cards (3 per row) ──────────────────────────
    modal = Modal("💌 Letter", key="letter_modal", max_width=700)

    for i in range(0, len(sorted_letters), 3):
        cols = st.columns(3)
        for j in range(3):
            if i + j >= len(sorted_letters):
                break
            letter = sorted_letters[i + j]
            with cols[j]:
                preview = letter["content"][:120] + "..." if len(letter["content"]) > 120 else letter["content"]
                st.markdown(f"""
                <div style="border:1px solid #f8bbd0;border-radius:12px;padding:16px;
                            background:linear-gradient(135deg,#fff9fb,#fce4ec);
                            margin-bottom:12px;min-height:180px">
                    <h4 style="color:#c2185b;margin:0 0 6px">💌 {letter['title']}</h4>
                    <p style="font-size:12px;color:#888;margin:0">
                        To: {letter['recipient']} · From: {letter['author']}<br>{letter['date'][:10]}
                    </p>
                    <hr style="border-color:#f8bbd0">
                    <p style="font-size:13px;white-space:pre-line">{preview}</p>
                </div>
                """, unsafe_allow_html=True)

                for tag in letter.get("tags", []):
                    st.markdown(
                        f"<span style='background:#fce4ec;color:#c2185b;padding:2px 7px;"
                        f"border-radius:10px;font-size:11px;margin-right:3px'>{tag}</span>",
                        unsafe_allow_html=True
                    )

                if st.button("Read Full Letter", key=f"open_{letter['id']}"):
                    st.session_state.open_letter_id = letter["id"]
                    modal.open()

    # ── Modal for full letter ─────────────────────────────
    if modal.is_open() and "open_letter_id" in st.session_state:
        letter = next((l for l in letters if l["id"] == st.session_state.open_letter_id), None)
        if letter:
            with modal.container():
                st.markdown(f"### 💌 {letter['title']}")
                st.caption(f"To: {letter['recipient']} · From: {letter['author']} · {letter['date'][:10]}")
                st.markdown("---")
                st.markdown(
                    f"<div style='white-space:pre-line;line-height:1.8;font-size:15px'>"
                    f"{letter['content']}</div>",
                    unsafe_allow_html=True
                )
