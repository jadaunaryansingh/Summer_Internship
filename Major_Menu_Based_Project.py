# flask_streamlit_menu_app.py
import streamlit as st
from flask import Flask, jsonify
import threading
import time
import requests
import os
import shutil
import cv2
import stat
import numpy as np
from email.mime.text import MIMEText
import smtplib
from googlesearch import search
import pywhatkit as pw
from twilio.rest import Client
import stat
import time

try:
    import pwd
    import grp
except ImportError:
    pwd = None
    grp = None
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
    "🌍 Download Website HTML", "🔗 Post on LinkedIn","🔎 Google Search", "🗂 File Manager", "📡 Ping API","🔐 SSH Command Executor","🧠 Remote File Control (Cross OS)"
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
elif menu == "📧 Send Email (pywhatkit)":
    st.title("📧 Send Email using pywhatkit")

    from_email = st.text_input("Sender Email (Gmail only)")
    password = st.text_input("App Password", type="password")
    to_email = st.text_input("Receiver Email")
    subject = st.text_input("Subject")
    message = st.text_area("Message")

    if st.button("Send Email"):
        sender = from_email.strip()
        receiver = to_email.strip()
        subj = subject.strip()
        msg = message.strip()

        if not (sender and password and receiver and subj and msg):
            st.warning("⚠️ Please fill all the fields.")
        elif "@" not in receiver:
            st.error("❌ Invalid email address.")
        else:
            try:
                # ✅ Make sure this order is correct
                pw.send_mail(sender, password,subj, msg,receiver )
                st.success("✅ Email sent successfully!")
            except Exception as e:
                st.error(f"❌ Failed to send email:\n{str(e)}")

#zrks apfb yjsi kxuc
# ------------------ Post on LinkedIn ------------------
elif menu == "🔗 Post on LinkedIn":
    st.subheader("📢 Post to LinkedIn via API")

    access_token = st.text_input("🔑 Access Token", type="password")
    author_urn = st.text_input("🧾 Author URN (e.g., urn:li:person:xxxx)")
    post_text = st.text_area("📝 Your Post Text")

    if st.button("🚀 Post to LinkedIn"):
        if not access_token or not author_urn or not post_text:
            st.warning("⚠️ Please fill in all the fields.")
        else:
            try:
                headers = {
                    "Authorization": f"Bearer {access_token}",
                    "Content-Type": "application/json",
                    "X-Restli-Protocol-Version": "2.0.0"
                }

                payload = {
                    "author": author_urn,
                    "lifecycleState": "PUBLISHED",
                    "specificContent": {
                        "com.linkedin.ugc.ShareContent": {
                            "shareCommentary": {
                                "text": post_text
                            },
                            "shareMediaCategory": "NONE"
                        }
                    },
                    "visibility": {
                        "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
                    }
                }

                response = requests.post(
                    "https://api.linkedin.com/v2/ugcPosts",
                    headers=headers,
                    json=payload
                )

                if response.status_code == 201:
                    st.success("✅ Post published successfully!")
                else:
                    st.error(f"❌ Failed with status: {response.status_code}")
                    st.json(response.json())

            except Exception as e:
                st.error(f"🚨 Error: {str(e)}")


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
import os
import shutil
import stat
import time

try:
    import pwd
    import grp
except ImportError:
    pwd = None
    grp = None

if menu == "🗂 File Manager":
    st.title("🗂 Guided File Manager")

    # Step 1: OS Selection
    os_mode = st.selectbox("🖥 Operating System", ["Windows", "Linux"])

    # Step 2: Task Selection
    task = st.selectbox("⚙ Task You Want to Perform", [
        "View Directory", "Rename", "Delete", "Move", "Create File", "Create Folder", "View File", "Change Directory"
    ])

    # Step 3: Directory Selection
    cwd = st.session_state.get("cwd", os.getcwd())
    new_dir = st.text_input("📁 Current Directory", value=cwd)
    if new_dir != cwd and os.path.isdir(new_dir):
        st.session_state["cwd"] = new_dir
        cwd = new_dir

    try:
        files = os.listdir(cwd)
    except Exception as e:
        st.error(f"Unable to read directory: {e}")
        files = []

    files = sorted(files)
    selected_item = st.selectbox("📂 Select a File/Folder", files) if files else None
    selected_path = os.path.join(cwd, selected_item) if selected_item else None

    # Show directory listing (if task is View Directory)
    if task == "View Directory":
        st.subheader("📄 Directory Content")
        show_hidden = st.checkbox("Show Hidden Files", value=False)
        visible_files = [f for f in files if show_hidden or not f.startswith('.')]

        for file in visible_files:
            path = os.path.join(cwd, file)
            try:
                stats = os.stat(path)
                mode = stat.filemode(stats.st_mode)
                size = stats.st_size
                mtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(stats.st_mtime))

                if os_mode == "Linux" and pwd and grp:
                    try:
                        owner = pwd.getpwuid(stats.st_uid).pw_name
                        group = grp.getgrgid(stats.st_gid).gr_name
                    except:
                        owner = group = "unknown"
                else:
                    owner = group = "user"

                st.text(f"{mode} {owner}:{group} {size}B {mtime}  {file}")
            except Exception as e:
                st.text(f"[Error reading {file}]: {e}")

    # Rename
    elif task == "Rename" and selected_path:
        new_name = st.text_input("📝 New Name")
        if st.button("Rename"):
            try:
                os.rename(selected_path, os.path.join(cwd, new_name))
                st.success("Renamed successfully!")
                st.experimental_rerun()
            except Exception as e:
                st.error(f"Rename failed: {e}")

    # Delete
    elif task == "Delete" and selected_path:
        if st.button("Delete"):
            try:
                if os.path.isfile(selected_path):
                    os.remove(selected_path)
                else:
                    shutil.rmtree(selected_path)
                st.success("Deleted successfully!")
                st.experimental_rerun()
            except Exception as e:
                st.error(f"Delete failed: {e}")

    # Move
    elif task == "Move" and selected_path:
        dest = st.text_input("📦 Destination Path")
        if st.button("Move"):
            try:
                shutil.move(selected_path, dest)
                st.success("Moved successfully!")
                st.experimental_rerun()
            except Exception as e:
                st.error(f"Move failed: {e}")

    # Create File
    elif task == "Create File":
        file_name = st.text_input("📄 New File Name")
        if st.button("Create File"):
            try:
                open(os.path.join(cwd, file_name), 'w').close()
                st.success("File created!")
                st.experimental_rerun()
            except Exception as e:
                st.error(f"File creation failed: {e}")

    # Create Folder
    elif task == "Create Folder":
        folder_name = st.text_input("📁 New Folder Name")
        if st.button("Create Folder"):
            try:
                os.makedirs(os.path.join(cwd, folder_name), exist_ok=True)
                st.success("Folder created!")
                st.experimental_rerun()
            except Exception as e:
                st.error(f"Folder creation failed: {e}")

    # View File
    elif task == "View File" and selected_path:
        if os.path.isfile(selected_path) and selected_path.endswith(('.txt', '.py', '.log', '.md')):
            try:
                with open(selected_path, 'r', encoding='utf-8', errors='ignore') as f:
                    st.text_area("📖 File Content", f.read(), height=300)
            except Exception as e:
                st.error(f"Cannot read file: {e}")
        else:
            st.warning("Selected item is not a readable text file.")

    # Change Directory
    elif task == "Change Directory" and selected_path:
        if os.path.isdir(selected_path):
            if st.button("Enter Directory"):
                st.session_state["cwd"] = selected_path
                st.experimental_rerun()
        else:
            st.warning("Selected item is not a directory.")
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
#--------------Remotely access File Manager Windows-----------
if menu == "🧠 Remote File Control (Cross OS)":
    import requests

    st.title("🧠 Aryan's Remote File Manager")

    # === Agent Script (Remote PC File Manager) ===
    agent_code = '''
import os
import shutil
import socket
import platform
from flask import Flask, request, jsonify

app = Flask(__name__)
current_os = platform.system()
cwd = os.getcwd()

@app.route('/')
def home():
    return f"🖥 Agent running on {socket.gethostname()} ({current_os})"

@app.route('/list', methods=['GET'])
def list_dir():
    global cwd
    path = request.args.get('path', cwd)
    try:
        cwd = path
        files = os.listdir(path)
        return jsonify({"success": True, "cwd": cwd, "files": files})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/rename', methods=['POST'])
def rename_file():
    data = request.json
    try:
        os.rename(data['old_path'], data['new_path'])
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/delete', methods=['POST'])
def delete_file():
    data = request.json
    try:
        if os.path.isfile(data['path']):
            os.remove(data['path'])
        else:
            shutil.rmtree(data['path'])
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/move', methods=['POST'])
def move_file():
    data = request.json
    try:
        shutil.move(data['source'], data['destination'])
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/create_file', methods=['POST'])
def create_file():
    data = request.json
    try:
        open(data['path'], 'w').close()
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/create_folder', methods=['POST'])
def create_folder():
    data = request.json
    try:
        os.makedirs(data['path'], exist_ok=True)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/view_file', methods=['GET'])
def view_file():
    path = request.args.get('path')
    try:
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        return jsonify({"success": True, "content": content})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/change_directory', methods=['POST'])
def change_directory():
    global cwd
    data = request.json
    try:
        os.chdir(data['path'])
        cwd = os.getcwd()
        return jsonify({"success": True, "cwd": cwd})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

if __name__ == '__main__':
    print(f"✅ Agent running on {current_os}")
    print("🌐 Listening on port 7860 (use your private IP address)")
    app.run(host='0.0.0.0', port=7860)
'''

    st.info("💡 Step 1: Ask your friend to run the agent script using `python remote_agent.py` on their system.")
    st.download_button("⬇️ Download Remote Agent Script", agent_code, file_name="remote_agent.py")

    st.markdown("---")
    st.header("🔌 Step 2: Connect to Remote PC")

    remote_ip = st.text_input("Enter Friend's IP Address", "127.0.0.1")
    base_url = f"http://{remote_ip}:7860"

    try:
        ping = requests.get(f"{base_url}/")
        st.success("✅ Connected to: " + ping.text)
    except:
        st.warning("⚠️ Could not connect. Ensure agent is running on remote PC.")

    task = st.selectbox("⚙️ Choose Task", [
        "View Directory", "Rename", "Delete", "Move",
        "Create File", "Create Folder", "View File", "Change Directory"
    ])

    st.markdown("### 🔧 Task Controls")

    if task == "View Directory":
        path = st.text_input("Directory to View", "/")
        if st.button("View"):
            r = requests.get(f"{base_url}/list", params={"path": path})
            data = r.json()
            if data["success"]:
                st.success(f"📁 Contents of: {data['cwd']}")
                for f in data["files"]:
                    st.text(f)
            else:
                st.error(data["error"])

    elif task == "Rename":
        old = st.text_input("Old Path")
        new = st.text_input("New Path")
        if st.button("Rename"):
            r = requests.post(f"{base_url}/rename", json={"old_path": old, "new_path": new})
            st.success("✅ Renamed!") if r.json()["success"] else st.error(r.json()["error"])

    elif task == "Delete":
        path = st.text_input("Path to Delete")
        if st.button("Delete"):
            r = requests.post(f"{base_url}/delete", json={"path": path})
            st.success("✅ Deleted!") if r.json()["success"] else st.error(r.json()["error"])

    elif task == "Move":
        source = st.text_input("Source Path")
        dest = st.text_input("Destination Path")
        if st.button("Move"):
            r = requests.post(f"{base_url}/move", json={"source": source, "destination": dest})
            st.success("✅ Moved!") if r.json()["success"] else st.error(r.json()["error"])

    elif task == "Create File":
        file_path = st.text_input("Full File Path to Create")
        if st.button("Create File"):
            r = requests.post(f"{base_url}/create_file", json={"path": file_path})
            st.success("✅ File Created!") if r.json()["success"] else st.error(r.json()["error"])

    elif task == "Create Folder":
        folder_path = st.text_input("Folder Path to Create")
        if st.button("Create Folder"):
            r = requests.post(f"{base_url}/create_folder", json={"path": folder_path})
            st.success("✅ Folder Created!") if r.json()["success"] else st.error(r.json()["error"])

    elif task == "View File":
        file_path = st.text_input("File Path to View")
        if st.button("View File"):
            r = requests.get(f"{base_url}/view_file", params={"path": file_path})
            data = r.json()
            if data["success"]:
                st.text_area("📖 File Content", data["content"], height=300)
            else:
                st.error(data["error"])

    elif task == "Change Directory":
        new_dir = st.text_input("Directory Path to Switch To")
        if st.button("Change Directory"):
            r = requests.post(f"{base_url}/change_directory", json={"path": new_dir})
            data = r.json()
            if data["success"]:
                st.success(f"✅ Changed to: {data['cwd']}")
            else:
                st.error(data["error"])

# ------------------ Run Flask in Background ------------------
def run_flask():
    app.run(port=5000)

threading.Thread(target=run_flask, daemon=True).start()
