import gradio as gr
import requests

BACKEND_URL = "http://127.0.0.1:8000"

def register_user(email, name, password):
    response = requests.post(f"{BACKEND_URL}/register", json={"email": email, "name": name, "password": password})
    if response.status_code == 200:
        return "✅ Registered successfully"
    else:
        return f"❌ Error: {response.json().get('detail')}"


def login_user(email, password):
    global auth_token
    response = requests.post(f"{BACKEND_URL}/login", json={"email": email, "password": password})
    if response.status_code == 200:
        auth_token = response.json()["access_token"]
        return "✅ Logged in successfully"
    else:
        return f"❌ Error: {response.json().get('detail')}"


def create_household(name):
    headers = {"Authorization": f"Bearer {auth_token}"}
    response = requests.post(f"{BACKEND_URL}/households", json={"name": name}, headers=headers)
    if response.status_code == 200:
        return f"✅ Household '{name}' created"
    else:
        return f"❌ Error: {response.json().get('detail')}"

def join_household(token):
    response = requests.post(f"{BACKEND_URL}/households/join", params={"token": token})
    if response.status_code == 200:
        return f"✅ {response.json()['message']}"
    else:
        return f"❌ Error: {response.json().get('detail')}"


with gr.Blocks() as demo:
    gr.Markdown("# 🏠 Roommate Manager")
    with gr.Tab("Register"):
        email = gr.Textbox(label="Email")
        name = gr.Textbox(label="Name")
        password = gr.Textbox(label="Password", type="password")
        register_btn = gr.Button("Register")
        register_output = gr.Textbox()
        register_btn.click(register_user, inputs=[email, name, password], outputs=register_output)
    with gr.Tab("Login"):
        login_email = gr.Textbox(label="Email")
        login_password = gr.Textbox(label="Password", type="password")
        login_btn = gr.Button("Login")
        login_output = gr.Textbox()
        login_btn.click(login_user, inputs=[login_email, login_password], outputs=login_output)
    with gr.Tab("Create Household"):
        household_name = gr.Textbox(label="Household Name")
        create_btn = gr.Button("Create")
        create_output = gr.Textbox()
        create_btn.click(create_household, inputs=household_name, outputs=create_output)

    with gr.Tab("Join Household"):
        join_token = gr.Textbox(label="Invite Token")
        join_btn = gr.Button("Join")
        join_output = gr.Textbox()
        join_btn.click(join_household, inputs=join_token, outputs=join_output)

demo.launch()
