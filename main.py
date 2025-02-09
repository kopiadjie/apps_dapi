import streamlit as st
import pandas as pd
from pyzbar.pyzbar import decode
from PIL import Image
from github import Github
import os

TOKEN = os.getenv("GITHUB_TOKEN")  # Pastikan Anda telah mengatur variabel ini di sistem Anda
g = Github(TOKEN)

REPO_NAME = "kopiadjie/apps_dapi"
repo = g.get_repo(REPO_NAME)



REPO_NAME = 'apps_dapi'
FILE_PATH = 'data.csv'


# Function to load data from GitHub
def load_data():
    contents = repo.get_contents(FILE_PATH)
    data = pd.read_csv(contents.download_url)
    return data

# Function to save data to GitHub
def save_data(data):
    repo.update_file(FILE_PATH, "Update data", data.to_csv(index=False), repo.get_contents(FILE_PATH).sha)

# Streamlit App
st.title("Aplikasi Streamlit dengan Barcode dan GitHub Integration")

# User Page
st.sidebar.title("User Page")
barcode_image = st.sidebar.file_uploader("Upload Barcode untuk Masuk", type=["png", "jpg", "jpeg"])

if barcode_image:
    barcode = decode(Image.open(barcode_image))
    if barcode:
        st.sidebar.success("Barcode berhasil dibaca!")
        user_id = barcode[0].data.decode("utf-8")
        st.sidebar.write(f"User ID: {user_id}")

        # User Input Form
        with st.form("user_input_form"):
            name = st.text_input("Nama")
            message = st.text_area("Kata-kata")
            submit_button = st.form_submit_button("Submit")

            if submit_button:
                data = load_data()
                new_data = pd.DataFrame([[user_id, name, message]], columns=["User ID", "Nama", "Kata-kata"])
                data = pd.concat([data, new_data], ignore_index=True)
                save_data(data)
                st.success("Data berhasil disimpan!")
    else:
        st.sidebar.error("Barcode tidak valid!")

# Admin Page
st.sidebar.title("Admin Page")
admin_password = st.sidebar.text_input("Masukkan Password Admin", type="password")

if admin_password == "admin123":  # Ganti dengan password yang lebih aman
    st.title("Admin Dashboard")
    data = load_data()
    st.write(data)
else:
    st.sidebar.error("Password salah!")