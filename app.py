import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Load credentials from Streamlit secrets
credentials_dict = st.secrets["google_credentials"]
credentials = ServiceAccountCredentials.from_json_keyfile_dict(credentials_dict, ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"])
client = gspread.authorize(credentials)

# Attempt to open the specific spreadsheet
try:
    spreadsheet = client.open("Pinnwand")  # Replace with your spreadsheet name
    worksheet = spreadsheet.sheet1
except Exception as e:
    st.error(f"Error opening spreadsheet: {e}")

def add_input_to_sheet(input_text):
    worksheet.append_row([input_text])

def get_all_inputs():
    return worksheet.col_values(1)

def main():
    st.title("PinBoard")

    st.header("Dein Text")
    user_input = st.text_area("Tippe einen kurzen Text ein")

    if st.button("Senden"):
        if user_input.strip():
            add_input_to_sheet(user_input)
            st.success("Text hinzugefügt!")
        else:
            st.error("Please enter some text")

    st.header("🧾")

    all_inputs = get_all_inputs()
    if all_inputs:
        for input_text in all_inputs:
            st.markdown(f"> {input_text}")
            st.markdown("<hr>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
