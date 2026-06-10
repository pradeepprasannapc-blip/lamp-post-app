import streamlit as st
import streamlit.components.v1 as components
import json
import os
import base64

# --- App Configuration ---
st.set_page_config(page_title="Chathura Group", page_icon="✨", layout="centered", initial_sidebar_state="collapsed")

# --- Custom CSS ---
st.markdown("""
<style>
    /* Animated Border සඳහා අවශ්‍ය Keyframes */
    @keyframes spin-border {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    /* පොදු Animated Border Wrapper එක (උඩ පින්තූරයට සහ Product ලිස්ට් එකට) */
    .animated-border-wrapper {
        position: relative;
        width: 100%;
        border-radius: 15px;
        background: #000;
        overflow: hidden;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 3px; 
        box-shadow: 0 0 10px rgba(255, 165, 0, 0.3);
    }
    
    .animated-border-wrapper::before, .animated-border-wrapper::after {
        content: '';
        position: absolute;
        width: 200%;
        height: 200%;
        background: conic-gradient(transparent, transparent, transparent, #FFA500);
        animation: spin-border 4s linear infinite;
    }
    
    .animated-border-wrapper::after {
        animation-delay: -2s;
    }

    /* Product Inner Content */
    .product-inner-content {
        position: relative;
        background: #111;
        width: 100%;
        height: 100%;
        border-radius: 12px;
        padding: 15px;
        z-index: 10;
        color: #fff;
    }
</style>
""", unsafe_allow_html=True)

# --- Settings & Functions ---
DATA_FILE = "products.json"
WHATSAPP_NUM = "94779998189"  
CALL_NUM = "94779998189"      
ADMIN_PASSWORD = "8189"       

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

# --- Header කොටස ---
header_file = "header.png" if os.path.exists("header.png") else "header.jpg"
header_b64 = get_image_base64(header_file)
bg_style = f"background-image: url(data:image/png;base64,{header_b64}); background-size: cover; background-position: center;" if header_b64 else "background-color: #111;"

text_elements = [("✨", "icon"), (" ", "space"), ("C", "letter"), ("H", "letter"), ("A", "letter"), ("T", "letter"), ("H", "letter"), ("U", "letter"), ("R", "letter"), ("A", "letter"), (" ", "space"), ("G", "letter"), ("R", "letter"), ("O", "letter"), ("U", "letter"), ("P", "letter"), (" ", "space"), ("👥", "icon")]
spans_html = "".join([f'<span class="{t}" style="animation-delay: {i*0.1}s">{"&nbsp;" if c==" " else c}</span>' for i, (c, t) in enumerate(text_elements)])

header_html = f"""
<style>
    #spin-text {{ font-size: clamp(16px, 6vw, 32px); font-family: 'Arial Black', Impact, sans-serif; font-weight: 900; letter-spacing: 1px; white-space: nowrap; display: flex; flex-direction: row; align-items: center; justify-content: center; width: 100%; }}
    #spin-text span {{ display: inline-block; opacity: 0; transform-origin: center; animation: spinFlip 5s infinite; }}
    #spin-text span.letter {{ background: linear-gradient(0deg, #0044ff 0%, #00bfff 50%, #ffffff 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; -webkit-text-stroke: 1.5px #FFFFFF; filter: drop-shadow(0px -2px 6px rgba(0, 191, 255, 0.8)); }}
    #spin-text span.icon {{ -webkit-text-stroke: 0px transparent !important; color: initial !important; filter: drop-shadow(2px 2px 4px rgba(0,0,0,0.8)); }}
    @keyframes spinFlip {{ 0%{{transform:rotateY(90deg) rotateX(90deg) scale(0.5); opacity:0;}} 15%{{transform:rotateY(0deg) rotateX(0deg) scale(1); opacity:1;}} 85%{{transform:rotateY(0deg) rotateX(0deg) scale(1); opacity:1;}} 100%{{transform:rotateY(-90deg) rotateX(-90deg) scale(0.5); opacity:0;}} }}
</style>
<div class="animated-border-wrapper" style="height:220px; margin-bottom:20px;">
    <div class="product-inner-content" style="{bg_style} display:flex; align-items:center; justify-content:center;">
        <div id="spin-text">{spans_html}</div>
    </div>
</div>
"""
components.html(header_html, height=240)

# --- Navigation Menu ---
menu = ["භාණ්ඩ බලන්න (Home)", "කළමනාකරුට පමණයි (Admin)"]
choice = st.sidebar.selectbox("මෙනුව තෝරන්න", menu, key="menu_selection")

# --- Home Page ---
if choice == "භාණ්ඩ බලන්න (Home)":
    st.markdown("""<div class="animated-border-wrapper" style="border: 2px solid #FF4500; margin-bottom: 25px;"><div class="product-inner-content" style="text-align:center;">
        <h2 style="color:#FFD700; font-family:'Arial Black';">💎 අපගේ නවතම PRODUCTS 🛍️</h2></div></div>""", unsafe_allow_html=True)
    
    for p in st.session_state.products:
        wa_b64 = get_image_base64("whatsapp_button.png")
        call_b64 = get_image_base64("call_now_1.png")
        prod_html = f"""
        <div class="product-neon-wrapper">
            <div class="product-inner-content">
                <h3>{p['name']}</h3>
                {f'<img class="prod-img" src="data:image/png;base64,{p["image"]}">' if p.get('image') else ''}
                <p><strong>විස්තරය:</strong><br>{p['desc'].replace('\n', '<br>')}</p>
                <p><strong>මිල:</strong> රු. {p['price']}</p>
                <div class="product-buttons">
                    {f'<a href="https://wa.me/{WHATSAPP_NUM}?text=මට මේ product එක ගැන දැනගන්න ඕනි: {p["name"]}" class="btn-wa"><img src="data:image/png;base64,{wa_b64}"></a>' if wa_b64 else ''}
                    {f'<a href="tel:{CALL_NUM}" class="btn-call"><img src="data:image/png;base64,{call_b64}"></a>' if call_b64 else ''}
                </div>
            </div>
        </div>
        """
        st.markdown(prod_html, unsafe_allow_html=True)

elif choice == "කළමනාකරුට පමණයි (Admin)":
    # Admin Panel code remains same...
    pass
