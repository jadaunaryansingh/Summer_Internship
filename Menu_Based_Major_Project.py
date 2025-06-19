# flask_streamlit_menu_app.py

import streamlit as st
from flask import Flask, jsonify
import threading
import time
import requests
import os
import shutil
import cv2
import numpy as np
from email.mime.text import MIMEText
import smtplib
from googlesearch import search
import pywhatkit as pw
from twilio.rest import Client

# ------------------ Flask API with Decorators ------------------

app = Flask(__name__)

def log_decorator(func):
    def wrapper(*args, **kwargs):
        print(f"Calling function: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

@app.route("/api/ping")
@log_decorator
def ping():
    return jsonify({"message": "pong"})

# ------------------ Streamlit Interface ------------------

st.set_page_config(page_title="Mega Menu App", layout="wide")
st.title("🚀 Multi-Tool Mega App (Flask + Streamlit)")

menu = st.sidebar.selectbox("Choose Feature", [
    "📞 Twilio Call", "💬 Send SMS", "🟢 WhatsApp Message",
    "📧 Send Email (pywhatkit)", "🎨 Draw Grid Image", "🔄 Face Swap",
    "🌍 Download Website HTML", "🔗 Post on LinkedIn", "🕵️ Anonymous Email 1",
    "📩 Anonymous Email 2", "🔎 Google Search", "🗂️ File Manager", "📡 Ping API"
])

# ------------------ Twilio Call ------------------
if menu == "📞 Twilio Call":
    acc = st.text_input("Account SID")
    tok = st.text_input("Auth Token", type="password")
    from_num = st.text_input("Twilio Number")
    to_num = st.text_input("To Number")
    if st.button("Call"):
        try:
            client = Client(acc, tok)
            call = client.calls.create(
                twiml='<Response><Say>Hi! This is a test call.</Say></Response>',
                to=to_num, from_=from_num)
            st.success(f"Call started: {call.sid}")
        except Exception as e:
            st.error(str(e))

# ------------------ Send SMS ------------------
if menu == "💬 Send SMS":
    acc = st.text_input("Account SID")
    tok = st.text_input("Auth Token", type="password")
    from_num = st.text_input("Twilio Number")
    to_num = st.text_input("To Number")
    msg = st.text_area("Message")
    if st.button("Send SMS"):
        try:
            client = Client(acc, tok)
            message = client.messages.create(body=msg, from_=from_num, to=to_num)
            st.success(f"Message SID: {message.sid}")
        except Exception as e:
            st.error(str(e))

# ------------------ WhatsApp Message ------------------
if menu == "🟢 WhatsApp Message":
    num = st.text_input("Enter number with country code")
    msg = st.text_area("Message")
    time_hr = st.number_input("Hour", 0, 23, 12)
    time_min = st.number_input("Minute", 0, 59, 30)
    if st.button("Send Message"):
        try:
            pw.sendwhatmsg(num, msg, int(time_hr), int(time_min), wait_time=5)
            st.success("Message sent (or scheduled) successfully!")
        except Exception as e:
            st.error(str(e))

# ------------------ Send Email (pywhatkit) ------------------
if menu == "📧 Send Email (pywhatkit)":
    from_email = st.text_input("Sender Email")
    password = st.text_input("App Password", type="password")
    to_email = st.text_input("Receiver Email")
    subject = st.text_input("Subject")
    message = st.text_area("Message")
    if st.button("Send Email"):
        try:
            pw.send_mail(from_email, password, to_email, subject, message)
            st.success("Email sent successfully!")
        except Exception as e:
            st.error(str(e))

# ------------------ Post on LinkedIn ------------------
if menu == "🔗 Post on LinkedIn":
    token = st.text_input("Access Token")
    urn = st.text_input("LinkedIn URN (person)")
    text = st.text_area("Post Text")
    if st.button("Post"):
        headers = {
            "Authorization": f"Bearer {token}",
            "X-Restli-Protocol-Version": "2.0.0",
            "Content-Type": "application/json"
        }
        data = {
            "author": f"urn:li:person:{urn}",
            "lifecycleState": "PUBLISHED",
            "specificContent": {
                "com.linkedin.ugc.ShareContent": {
                    "shareCommentary": {"text": text},
                    "shareMediaCategory": "NONE"
                }
            },
            "visibility": {
                "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
            }
        }
        try:
            r = requests.post("https://api.linkedin.com/v2/ugcPosts", headers=headers, json=data)
            st.code(r.text)
        except Exception as e:
            st.error(str(e))

# ------------------ Anonymous Email 1 ------------------
if menu == "🕵️ Anonymous Email 1":
    sender = st.text_input("Sender Email")
    to = st.text_input("Recipient Email")
    body = st.text_area("Message")
    password = st.text_input("App Password", type="password")
    if st.button("Send Anonymous Email 1"):
        msg = MIMEText(body)
        msg["Subject"] = "Anonymous Message"
        msg["From"] = sender
        msg["To"] = to
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(sender, password)
            server.send_message(msg)
            server.quit()
            st.success("Email sent anonymously!")
        except Exception as e:
            st.error(str(e))

# ------------------ Anonymous Email 2 ------------------
if menu == "📩 Anonymous Email 2":
    sender = st.text_input("Sender Email")
    to = st.text_input("Recipient Email")
    body = st.text_area("Message")
    password = st.text_input("App Password", type="password")
    if st.button("Send Anonymous Email 2"):
        msg = MIMEText(body)
        msg["Subject"] = "Anonymous Message"
        msg["From"] = f"Anonymous <{sender}>"
        msg["To"] = to
        try:
            server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            server.login(sender, password)
            server.sendmail(sender, to, msg.as_string())
            server.quit()
            st.success("Email sent anonymously!")
        except Exception as e:
            st.error(str(e))
# ------------------ Draw Grid Image ------------------
def generate_grid_image():
    width, height = 800, 600
    image = np.zeros((height, width, 3), dtype=np.uint8)
    for x in range(0, width, 40):
        cv2.line(image, (x, 0), (x, height), (30, 30, 30), 1)
    for y in range(0, height, 40):
        cv2.line(image, (0, y), (width, y), (30, 30, 30), 1)
    path = "grid_image.png"
    cv2.imwrite(path, image)
    return path

if menu == "🎨 Draw Grid Image":
    st.image(generate_grid_image())

# ------------------ Face Swap ------------------
def face_swap():
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    cap = cv2.VideoCapture(0)
    ret1, img1 = cap.read()
    cv2.waitKey(1000)
    ret2, img2 = cap.read()
    cap.release()
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    faces1 = face_cascade.detectMultiScale(gray1, 1.3, 5)
    faces2 = face_cascade.detectMultiScale(gray2, 1.3, 5)
    if len(faces1) == 0 or len(faces2) == 0:
        return None, None
    x1, y1, w1, h1 = faces1[0]
    x2, y2, w2, h2 = faces2[0]
    face1 = cv2.resize(img1[y1:y1+h1, x1:x1+w1], (w2, h2))
    face2 = cv2.resize(img2[y2:y2+h2, x2:x2+w2], (w1, h1))
    img1[y1:y1+h1, x1:x1+w1] = face2
    img2[y2:y2+h2, x2:x2+w2] = face1
    cv2.imwrite("swapped1.png", img1)
    cv2.imwrite("swapped2.png", img2)
    return "swapped1.png", "swapped2.png"

if menu == "🔄 Face Swap":
    if st.button("Swap Faces"):
        img1, img2 = face_swap()
        if img1:
            st.image(img1)
            st.image(img2)
        else:
            st.error("No faces detected.")

# ------------------ Download Website HTML ------------------
def download_html(url):
    try:
        res = requests.get(url)
        with open("website.html", "w", encoding="utf-8") as f:
            f.write(res.text)
        return "website.html"
    except Exception as e:
        return str(e)

if menu == "🌍 Download Website HTML":
    url = st.text_input("Enter URL", "https://www.geeksforgeeks.org")
    if st.button("Download"):
        file = download_html(url)
        if os.path.exists(file):
            with open(file, encoding="utf-8") as f:
                st.code(f.read()[:1000])
        else:
            st.error(file)

# ------------------ Google Search ------------------
if menu == "🔎 Google Search":
    query = st.text_input("Search Query", "Python programming tutorials")
    if st.button("Search"):
        try:
            results = list(search(query, num_results=5))
            for url in results:
                st.write(url)
        except Exception as e:
            st.error(str(e))

# ------------------ Ping Flask API ------------------
if menu == "📡 Ping API":
    if st.button("Ping /api/ping"):
        try:
            r = requests.get("http://127.0.0.1:5000/api/ping")
            st.json(r.json())
        except Exception as e:
            st.error(str(e))

# ------------------ File Manager ------------------
if menu == "🗂️ File Manager":
    cwd = st.session_state.get("cwd", os.getcwd())
    new_dir = st.text_input("Current Directory", value=cwd)
    if new_dir != cwd:
        if os.path.isdir(new_dir):
            st.session_state["cwd"] = new_dir
            cwd = new_dir
        else:
            st.error("Invalid directory")

    files = os.listdir(cwd)
    selected = st.selectbox("Select Item", files)
    action = st.radio("Action", ["Rename", "Delete", "Change Directory", "Create File", "Create Folder", "Move", "View File"])

    if action == "Rename":
        new_name = st.text_input("New Name")
        if st.button("Rename"):
            os.rename(os.path.join(cwd, selected), os.path.join(cwd, new_name))
            st.success("Renamed")

    elif action == "Delete":
        if st.button("Delete"):
            path = os.path.join(cwd, selected)
            if os.path.isfile(path):
                os.remove(path)
            else:
                shutil.rmtree(path)
            st.success("Deleted")

    elif action == "Change Directory":
        path = os.path.join(cwd, selected)
        if os.path.isdir(path) and st.button("Enter Directory"):
            st.session_state["cwd"] = path
            st.experimental_rerun()

    elif action == "Create File":
        file_name = st.text_input("File Name")
        if st.button("Create File"):
            open(os.path.join(cwd, file_name), 'w').close()
            st.success("File Created")

    elif action == "Create Folder":
        folder_name = st.text_input("Folder Name")
        if st.button("Create Folder"):
            os.makedirs(os.path.join(cwd, folder_name), exist_ok=True)
            st.success("Folder Created")

    elif action == "Move":
        dest = st.text_input("Destination Path")
        if st.button("Move"):
            shutil.move(os.path.join(cwd, selected), dest)
            st.success("Moved")

    elif action == "View File":
        path = os.path.join(cwd, selected)
        if os.path.isfile(path) and path.endswith(('.txt', '.py', '.log')):
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                st.text_area("Content", f.read(), height=300)
        else:
            st.warning("Not a viewable text file")

# ------------------ Run Flask in Background ------------------
def run_flask():
    app.run(port=5000)

threading.Thread(target=run_flask, daemon=True).start()
