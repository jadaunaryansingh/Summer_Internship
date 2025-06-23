import streamlit as st
import os
import shutil
st.title("Advanced File Management")
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
        old = os.path.join(cwd, selected)
        new = os.path.join(cwd, new_name)
        os.rename(old, new)
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
        path = os.path.join(cwd, file_name)
        open(path, 'w').close()
        st.success("File Created")
elif action == "Create Folder":
    folder_name = st.text_input("Folder Name")
    if st.button("Create Folder"):
        path = os.path.join(cwd, folder_name)
        os.makedirs(path, exist_ok=True)
        st.success("Folder Created")
elif action == "Move":
    dest = st.text_input("Destination Path")
    if st.button("Move"):
        src = os.path.join(cwd, selected)
        shutil.move(src, dest)
        st.success("Moved")
elif action == "View File":
    path = os.path.join(cwd, selected)
    if os.path.isfile(path) and path.endswith(('.txt', '.py', '.log')):
        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        st.text_area("Content", content, height=300)
    else:
        st.warning("Not a viewable text file")
