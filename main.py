import streamlit as st
import pandas as pd
import datetime
import uuid
import os
import json
import time

from dotenv import load_dotenv

load_dotenv()

user1 = os.getenv('USER_1')
user2 = os.getenv('USER_2')
share = os.getenv('SHARE')

pass1 = os.getenv('PASSWORD_1')
pass2 = os.getenv('PASSWORD_2')
password = os.getenv('PASSWORD')


# Set page configuration
st.set_page_config(
    page_title="Letter Writing App",
    page_icon="✉️",
    layout="wide"
)

# Initialize session state variables if they don't exist
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'users' not in st.session_state:
    # In a real app, you'd use a database or secure file
    st.session_state.users = {
        share: password,
        user1: pass1,
        user2: pass2
    }
if 'letters' not in st.session_state:
    # Try to load existing letters from file
    if os.path.exists("text/letters.json"):
        with open("text/letters.json", "r") as f:
            st.session_state.letters = json.load(f)
    else:
        st.session_state.letters = []
if 'show_notification' not in st.session_state:
    st.session_state.show_notification = False
if 'notification_message' not in st.session_state:
    st.session_state.notification_message = ""

# Function to save letters to file
def save_letters():
    with open("letters.json", "w") as f:
        json.dump(st.session_state.letters, f)

# Login function
def login(username, password):
    if username in st.session_state.users and st.session_state.users[username] == password:
        st.session_state.logged_in = True
        st.session_state.username = username
        return True
    return False

# Logout function
def logout():
    st.session_state.logged_in = False
    st.session_state.username = ""

# Function to add a new letter
def add_letter(title, content, recipient):
    letter = {
        "id": str(uuid.uuid4()),
        "author": st.session_state.username,
        "title": title,
        "content": content,
        "recipient": recipient,
        "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    st.session_state.letters.append(letter)
    save_letters()
    
    # Set notification
    st.session_state.show_notification = True
    st.session_state.notification_message = f"Letter '{title}' has been successfully submitted!"

# Function to format text for HTML display with preserved formatting
def format_text_for_html(text, preview=False, max_length=100):
    # Replace newlines with HTML line breaks
    formatted_text = text.replace("\n", "<br>")
    
    # If this is a preview, truncate the text
    if preview and len(text) > max_length:
        # Find the last space before max_length to avoid cutting words
        last_space = formatted_text[:max_length].rfind(" ")
        if last_space > 0:
            formatted_text = formatted_text[:last_space] + "..."
        else:
            formatted_text = formatted_text[:max_length] + "..."
    
    return formatted_text

# Function to display notification
def show_notification():
    if st.session_state.show_notification:
        # Create a notification at the top of the page
        notification = st.empty()
        with notification.container():
            st.success(st.session_state.notification_message)
        
        # Reset notification state after 3 seconds
        st.session_state.show_notification = False
        st.session_state.notification_message = ""

# Main app layout
def main():
    # Show notification if needed
    show_notification()
    
    st.title("✉️ Letter Writing App")
    
    # Sidebar for navigation
    with st.sidebar:
        st.header("Navigation")
        if st.session_state.logged_in:
            st.write(f"Welcome, {st.session_state.username}!")
            page = st.radio("Go to", ["Write Letter", "View Letters"])
            if st.button("Logout"):
                logout()
                st.rerun()
        else:
            page = "Login"
    
    # Login page
    if page == "Login":
        st.header("Login")
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")
            
            if submit:
                if login(username, password):
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid username or password")
    
    # Write letter page
    elif page == "Write Letter":
        st.header("Write a New Letter")
        with st.form("letter_form"):
            title = st.text_input("Letter Title")
            recipient = st.text_input("Recipient")
            content = st.text_area("Letter Content", height=300)
            submit = st.form_submit_button("Submit Letter")
            
            if submit:
                if title and content and recipient:
                    add_letter(title, content, recipient)
                    st.rerun()
                else:
                    st.error("Please fill in all fields")
    
    # View letters page
    elif page == "View Letters":
        st.header("Letter Cards")
        
        # Filter options
        filter_col1, filter_col2 = st.columns(2)
        with filter_col1:
            filter_option = st.selectbox(
                "Filter by:",
                ["All Letters", "My Letters", "By Recipient"]
            )
        
        with filter_col2:
            if filter_option == "By Recipient":
                recipients = list(set([letter["recipient"] for letter in st.session_state.letters]))
                selected_recipient = st.selectbox("Select Recipient:", recipients if recipients else ["No recipients"])
        
        # Filter letters based on selection
        filtered_letters = st.session_state.letters
        if filter_option == "My Letters":
            filtered_letters = [letter for letter in filtered_letters if letter["author"] == st.session_state.username]
        elif filter_option == "By Recipient" and recipients:
            filtered_letters = [letter for letter in filtered_letters if letter["recipient"] == selected_recipient]
        
        # Display letters as cards
        if not filtered_letters:
            st.info("No letters to display")
        else:
            # Sort letters by date (newest first)
            filtered_letters = sorted(filtered_letters, key=lambda x: x["date"], reverse=True)
            
            # Create rows of cards (3 per row)
            for i in range(0, len(filtered_letters), 3):
                cols = st.columns(3)
                for j in range(3):
                    if i + j < len(filtered_letters):
                        letter = filtered_letters[i + j]
                        with cols[j]:
                            with st.container():
                                # Format the preview text with preserved formatting
                                preview_text = format_text_for_html(letter["content"], preview=True, max_length=100)
                                
                                st.markdown(f"""
                                <div style="
                                    border: 1px solid #ddd;
                                    border-radius: 10px;
                                    padding: 15px;
                                    margin-bottom: 20px;
                                    background-color: #f9f9f9;
                                ">
                                    <h3>{letter["title"]}</h3>
                                    <p><strong>To:</strong> {letter["recipient"]}</p>
                                    <p><strong>From:</strong> {letter["author"]}</p>
                                    <p><strong>Date:</strong> {letter["date"]}</p>
                                    <hr>
                                    <div style="white-space: pre-line;">{preview_text}</div>
                                </div>
                                """, unsafe_allow_html=True)
                                
                                if st.button(f"View Full Letter", key=letter["id"]):
                                    st.session_state.selected_letter = letter["id"]
                                    st.rerun()
        
        # Display full letter in modal-like container
        if 'selected_letter' in st.session_state:
            letter_id = st.session_state.selected_letter
            letter = next((l for l in st.session_state.letters if l["id"] == letter_id), None)
            
            if letter:
                with st.expander("Full Letter", expanded=True):
                    st.title(letter["title"])
                    st.write(f"**To:** {letter['recipient']}")
                    st.write(f"**From:** {letter['author']}")
                    st.write(f"**Date:** {letter['date']}")
                    st.markdown("---")
                    
                    # Display the letter content with preserved formatting
                    st.markdown(f"""
                    <div style="
                        white-space: pre-line;
                        background-color: white;
                        padding: 20px;
                        border-radius: 5px;
                        border: 1px solid #eee;
                        margin-top: 10px;
                    ">
                    {letter["content"]}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if st.button("Close"):
                        del st.session_state.selected_letter
                        st.rerun()

# Run the app
if __name__ == "__main__":
    main()
