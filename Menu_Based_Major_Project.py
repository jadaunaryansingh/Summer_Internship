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
    "🌍 Download Website HTML", "🔗 Post on LinkedIn","🔎 Google Search", "🗂️ File Manager", "📡 Ping API","🔐 SSH Command Executor"
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
import threading
import pyautogui
import time
if menu == "🟢 WhatsApp Message":
    num = st.text_input("Enter number with country code")
    msg = st.text_area("Message")
    wait_time = st.slider("Wait time (seconds)", 5, 20, 10)
    def send_msg():
        try:
            pw.sendwhatmsg_instantly(num, msg, wait_time=wait_time, tab_close=False)
            time.sleep(wait_time + 5)  # wait extra for page to fully load
            pyautogui.press("enter")  # simulate Enter key to send
        except Exception as e:
            st.error(str(e))

    if st.button("Send Message"):
        threading.Thread(target=send_msg).start()
        st.success("Message is being sent. Do not move your mouse or change window.")
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
# ------------------ Draw Grid Image ------------------
from streamlit_drawable_canvas import st_canvas
import streamlit as st

if menu == "🎨 Draw Grid Image":
    st.subheader("🧑‍🎨 Draw on Grid Canvas")

    canvas_result = st_canvas(
        fill_color="rgba(255, 255, 255, 0)",  # No fill
        stroke_width=2,
        stroke_color="#00FFAA",
        background_color="#000000",
        height=600,
        width=800,
        drawing_mode="freedraw",
        key="draw_canvas"
    )

    if canvas_result.image_data is not None:
        st.image(canvas_result.image_data, caption="🖼️ Your Drawing")

    st.info("Use your mouse to draw. To erase, refresh the page.")
# ------------------ Face Swap ------------------
if menu == "🔄 Face Swap":
    import cv2
    import numpy as np

    st.subheader("🔄 Face Swap with Webcam + Preview")

    def capture_image():
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        cap.release()
        if not ret:
            return None
        return frame

    def detect_and_draw(img):
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
        return img, faces

    def face_swap_images(img1, img2, faces1, faces2):
        if len(faces1) == 0 or len(faces2) == 0:
            return None, None

        x1, y1, w1, h1 = faces1[0]
        x2, y2, w2, h2 = faces2[0]

        face1 = cv2.resize(img1[y1:y1+h1, x1:x1+w1], (w2, h2))
        face2 = cv2.resize(img2[y2:y2+h2, x2:x2+w2], (w1, h1))

        img1[y1:y1+h1, x1:x1+w1] = face2
        img2[y2:y2+h2, x2:x2+w2] = face1

        path1 = "swapped1.png"
        path2 = "swapped2.png"
        cv2.imwrite(path1, img1)
        cv2.imwrite(path2, img2)

        return path1, path2

    # Image session states
    if "image1" not in st.session_state: st.session_state["image1"] = None
    if "image2" not in st.session_state: st.session_state["image2"] = None
    if "faces1" not in st.session_state: st.session_state["faces1"] = []
    if "faces2" not in st.session_state: st.session_state["faces2"] = []

    col1, col2 = st.columns(2)

    with col1:
        if st.button("📸 Capture First Image", key="capture1"):
            img = capture_image()
            if img is not None:
                img_drawn, faces = detect_and_draw(img.copy())
                st.session_state["image1"] = img
                st.session_state["faces1"] = faces
                st.image(img_drawn, caption=f"✅ First Image ({len(faces)} face(s))", channels="BGR")

    with col2:
        if st.button("📸 Capture Second Image", key="capture2"):
            img = capture_image()
            if img is not None:
                img_drawn, faces = detect_and_draw(img.copy())
                st.session_state["image2"] = img
                st.session_state["faces2"] = faces
                st.image(img_drawn, caption=f"✅ Second Image ({len(faces)} face(s))", channels="BGR")

    if st.session_state["image1"] is not None and st.session_state["image2"] is not None:
        if st.button("🔄 Swap Faces", key="swap_faces"):
            result1, result2 = face_swap_images(
                st.session_state["image1"].copy(),
                st.session_state["image2"].copy(),
                st.session_state["faces1"],
                st.session_state["faces2"]
            )
            if result1 and result2:
                st.success("✅ Face Swap Completed!")
                st.image(result1, caption="Swapped Image 1")
                st.image(result2, caption="Swapped Image 2")
            else:
                st.error("❌ Face(s) not detected in one or both images.")
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
    st.header("📡 Ping an API Endpoint")
    api_url = st.text_input("Enter API URL:", "http://127.0.0.1:5000/api/ping")
    if st.button("Ping API"):
        try:
            r = requests.get(api_url)
            try:
                st.json(r.json())  # Try rendering as JSON
            except:
                st.write(r.text)   # Fallback to plain text
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
#SSH Command Executor
if menu == "🔐 SSH Command Executor":
    st.subheader("🔐 SSH Command Center")

    ssh_host = st.text_input("Host (IP or domain)")
    ssh_port = st.number_input("Port", value=22)
    ssh_user = st.text_input("Username")
    ssh_pass = st.text_input("Password", type="password")

    # Predefined 50 commands
    commands = [
        "ls", "pwd", "whoami", "uptime", "df -h", "free -m", "top -b -n1", "ps aux",
        "cat /etc/os-release", "uname -a", "netstat -tuln", "ifconfig", "ip a", "ping -c 4 google.com",
        "history", "du -sh *", "find / -type f -name '*.log'", "journalctl -xe", "tail -n 100 /var/log/syslog",
        "date", "cal", "env", "echo $PATH", "groups", "id", "lsblk", "mount", "df -i", "uptime -p", "who",
        "last", "hostname", "ls -alh", "crontab -l", "cat /etc/passwd", "cat /etc/group", "ss -tuln", "ip r",
        "iptables -L", "firewalld --state", "nmcli dev status", "systemctl list-units --type=service",
        "systemctl status sshd", "reboot", "shutdown now", "logout", "clear", "echo Hello from SSH", "ls /home"
    ]

    if st.button("Connect & Show Options"):
        if not (ssh_host and ssh_user and ssh_pass):
            st.warning("Please fill all SSH fields.")
        else:
            st.session_state["ssh_ready"] = True

    if st.session_state.get("ssh_ready"):
        st.success("SSH connected! Choose a command to run:")

        # Display numbered command list
        st.markdown("### 🔢 Predefined Command List")
        for i, cmd in enumerate(commands, 1):
            st.text(f"{i}. {cmd}")

        col1, col2 = st.columns(2)

        with col1:
            cmd_num = st.number_input("Run Command No. (1–50)", min_value=1, max_value=50, step=1)
            run_num_cmd = st.button("Run Selected Command")

        with col2:
            custom_cmd = st.text_input("Or Enter Your Own Command")
            run_custom_cmd = st.button("Run Custom Command")

        try:
            import paramiko
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=ssh_host, port=ssh_port, username=ssh_user, password=ssh_pass)

            if run_num_cmd:
                selected_command = commands[cmd_num - 1]
                st.info(f"Running command #{cmd_num}: `{selected_command}`")
                stdin, stdout, stderr = ssh.exec_command(selected_command)
            elif run_custom_cmd and custom_cmd.strip():
                st.info(f"Running your custom command: `{custom_cmd}`")
                stdin, stdout, stderr = ssh.exec_command(custom_cmd)
            else:
                stdin = stdout = stderr = None

            if stdout:
                st.code(stdout.read().decode())
            if stderr:
                err = stderr.read().decode()
                if err:
                    st.error(err)

            ssh.close()
        except Exception as e:
            st.error(f"SSH Error: {str(e)}")

# ------------------ Run Flask in Background ------------------
def run_flask():
    app.run(port=5000)

threading.Thread(target=run_flask, daemon=True).start()
