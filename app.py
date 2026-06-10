import streamlit as st
import streamlit.components.v1 as components
import json
import os
import base64

# --- App Configuration ---
st.set_page_config(page_title="Chathura Group", page_icon="✨", layout="centered", initial_sidebar_state="collapsed")

# Hide the Streamlit footer, menu and secondary buttons
hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            [data-testid="stToolbar"] {visibility: hidden;}
            [data-testid="stDecoration"] {visibility: hidden;}
            button[kind="secondary"] {visibility: hidden;}
            div[data-testid="stStatusWidget"] {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# --- Custom CSS ---
st.markdown("""
<style>
    @keyframes spin-border {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    .product-neon-wrapper {
        position: relative; width: 100%; border-radius: 15px; background: #000;
        margin-bottom: 30px; overflow: hidden; display: flex;
        align-items: center; justify-content: center; padding: 4px;
        box-shadow: 0 0 15px rgba(255, 69, 0, 0.4);
    }
    .product-neon-wrapper::before, .product-neon-wrapper::after {
        content: ''; position: absolute; width: 250%; height: 250%;
        background: conic-gradient(transparent, transparent, transparent, #FF4500);
        animation: spin-border 4s linear infinite; z-index: 0;
    }
    .product-neon-wrapper::after { background: conic-gradient(transparent, transparent, transparent, #FFD700); animation-delay: -2s; }
    .product-inner-content {
        position: relative; background: #111; width: 100%; height: 100%;
        border-radius: 12px; padding: 20px; z-index: 10; color: #fff;
    }
    .product-buttons { display: flex; gap: 15px; margin-top: 20px; }
    .product-buttons a { flex: 1; height: 85px; display: flex; justify-content: center; align-items: center; border-radius: 15px; overflow: hidden; }
    .btn-wa { border: 3px solid #25D366; }
    .btn-call { border: 3px solid #FF8C00; }
</style>
""", unsafe_allow_html=True)

# --- Settings ---
DATA_FILE = "products.json"
WHATSAPP_NUM = "94779998189"  
CALL_NUM = "94779998189"      
ADMIN_PASSWORD = "8189"       

# --- Functions ---
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try: return json.load(f)
            except: return []
    return []

def save_data(data):
    with open(DATA_FILE, "w") as f: json.dump(data, f)

def get_image_base64(filepath):
    if os.path.exists(filepath):
        with open(filepath, "rb") as img_file: return base64.b64encode(img_file.read()).decode()
    return None

def logout_user():
    st.session_state.logged_in = False
    st.session_state.menu_selection = "භාණ්ඩ බලන්න (Home)"

# --- Session States ---
if 'products' not in st.session_state: st.session_state.products = load_data()
if 'logged_in' not in st.session_state: st.session_state.logged_in = False
if 'menu_selection' not in st.session_state: st.session_state.menu_selection = "භාණ්ඩ බලන්න (Home)"
if 'editing_index' not in st.session_state: st.session_state.editing_index = None

# --- Home Page ---
if st.session_state.menu_selection == "භාණ්ඩ බලන්න (Home)":
    # Header logic remains same...
    if not st.session_state.products: st.info("දැනට භාණ්ඩ කිසිවක් ඇතුලත් කර නොමැත.")
    for idx, p in enumerate(st.session_state.products):
        wa_b64 = get_image_base64("whatsapp_button.png")
        call_b64 = get_image_base64("call_now_1.png")
        img_html = f'<img class="prod-img" style="width:100%; border-radius:10px; margin-bottom:15px;" src="data:image/png;base64,{p["image"]}">' if p.get('image') else ''
        prod_html = f"""
        <div class="product-neon-wrapper">
            <div class="product-inner-content">
                <h3>{p['name']}</h3>
                {img_html}
                <p><strong>විස්තරය:</strong><br>{p['desc'].replace('\n', '<br>')}</p>
                <p style="color: #F4D03F;"><strong>මිල:</strong> රු. {p['price']}</p>
                <div class="product-buttons">
                    <a href="https://wa.me/{WHATSAPP_NUM}?text=මට මේ භාණ්ඩය ගැන දැනගන්න ඕනි: {p['name']}" class="btn-wa"><img src="data:image/png;base64,{wa_b64}" style="transform:scale(1.45)"></a>
                    <a href="tel:{CALL_NUM}" class="btn-call"><img src="data:image/png;base64,{call_b64}" style="transform:scale(1.15)"></a>
                </div>
            </div>
        </div>
        """
        st.markdown(prod_html, unsafe_allow_html=True)

# --- Navigation & Admin Logic ---
st.sidebar.markdown("---")
menu = ["භාණ්ඩ බලන්න (Home)", "කළමනාකරුට පමණයි (Admin)"]
choice = st.sidebar.selectbox("මෙනුව තෝරන්න", menu, key="menu_selection")

if choice == "කළමනාකරුට පමණයි (Admin)":
    if not st.session_state.logged_in:
        password = st.sidebar.text_input("මුරපදය (Password)", type="password")
        if st.sidebar.button("ඇතුලත් වන්න"):
            if password == ADMIN_PASSWORD:
                st.session_state.logged_in = True
                st.rerun()
    else:
        st.header("Admin Panel")
        if st.button("Logout"): logout_user(); st.rerun()
        # (Admin functions here...)
