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
    /* Global Keyframes */
    @keyframes spin-border {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }

    /* Product පෙන්වන කොටුව සඳහා වූ විශේෂ Animated Neon Border එක */
    .product-neon-wrapper {
        position: relative;
        width: 100%;
        border-radius: 15px;
        background: #000;
        margin-bottom: 30px;
        overflow: hidden;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 4px; /* බෝඩර් එකේ ඝනකම */
        box-shadow: 0 0 15px rgba(255, 69, 0, 0.4);
    }
    
    .product-neon-wrapper::before, .product-neon-wrapper::after {
        content: '';
        position: absolute;
        width: 250%;
        height: 250%;
        background: conic-gradient(transparent, transparent, transparent, #FF4500);
        animation: spin-border 4s linear infinite;
        z-index: 0;
    }
    
    .product-neon-wrapper::after {
        background: conic-gradient(transparent, transparent, transparent, #FFD700);
        animation-delay: -2s;
    }
    
    .product-inner-content {
        position: relative;
        background: #111; /* භාණ්ඩයේ පසුබිම */
        width: 100%;
        height: 100%;
        border-radius: 12px;
        padding: 20px;
        z-index: 10;
        color: #fff;
    }
    
    .product-inner-content h3 {
        margin-top: 0;
        color: #FFFFFF;
        font-size: 24px;
        font-weight: bold;
        text-shadow: 2px 2px 5px rgba(0,0,0,0.8);
    }
    
    .product-inner-content img.prod-img {
        width: 100%;
        border-radius: 10px;
        margin-bottom: 15px;
        border: 1px solid #333;
    }
    
    .product-buttons {
        display: flex;
        gap: 15px;
        margin-top: 20px;
    }
    
    .product-buttons a {
        flex: 1;
        display: flex;
        justify-content: center;
        align-items: center;
        text-decoration: none;
    }
    
    .product-buttons img {
        width: 100%;
        height: 110px;
        object-fit: contain;
        border-radius: 15px;
    }
    
    .btn-wa img { border: 3px solid #25D366; }
    .btn-call img { border: 3px solid #FF8C00; }

    /* Admin Panel එකේ සාමාන්‍ය කොටු සඳහා */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 15px !important;
        padding: 15px !important;
        border: 2px solid #5D6D7E !important; 
    }
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

# --- Header එක ---
header_file = "header.png" if os.path.exists("header.png") else "header.jpg"
header_b64 = get_image_base64(header_file)

# පින්තූරය පසුබිමට දැමීම
bg_style = f"background-image: url(data:image/png;base64,{header_b64}); background-size: cover; background-position: center;" if header_b64 else "background-color: #111;"

text_elements = [
    ("✨", "icon"), (" ", "space"), 
    ("C", "letter"), ("H", "letter"), ("A", "letter"), ("T", "letter"), ("H", "letter"), ("U", "letter"), ("R", "letter"), ("A", "letter"), 
    (" ", "space"), 
    ("G", "letter"), ("R", "letter"), ("O", "letter"), ("U", "letter"), ("P", "letter"), 
    (" ", "space"), ("👥", "icon")
]

spans_html = ""
for i, (char, char_type) in enumerate(text_elements):
    delay = i * 0.1
    if char_type == "space":
        spans_html += f'<span style="animation-delay: {delay}s">&nbsp;</span>\n'
    elif char_type == "icon":
        spans_html += f'<span class="icon" style="animation-delay: {delay}s">{char}</span>\n'
    else:
        spans_html += f'<span class="letter" style="animation-delay: {delay}s">{char}</span>\n'

# නිල් සහ සුදු පාට අකුරු සහිත Header එක
header_html = f"""
<style>
    .animated-border-wrapper {{
        position: relative;
        width: 100%;
        height: 220px;
        border-radius: 15px;
        background: #000;
        margin-bottom: 20px;
        overflow: hidden;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 3px; 
        box-shadow: 0 0 10px rgba(255, 165, 0, 0.3); 
    }}
    
    .animated-border-wrapper::before {{
        content: '';
        position: absolute;
        width: 200%;
        height: 200%;
        background: conic-gradient(transparent, transparent, transparent, #FFA500);
        animation: spin-border 4s linear infinite;
    }}
    
    .animated-border-wrapper::after {{
        content: '';
        position: absolute;
        width: 200%;
        height: 200%;
        background: conic-gradient(transparent, transparent, transparent, #FFA500);
        animation: spin-border 4s linear infinite;
        animation-delay: -2s;
    }}

    .header-image-container {{
        position: relative;
        width: 100%;
        height: 100%;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
        z-index: 10;
        {bg_style}
    }}
    
    #spin-text {{
        font-size: clamp(16px, 6vw, 32px); 
        font-family: 'Arial Black', Impact, sans-serif;
        font-weight: 900;
        letter-spacing: 1px;
        white-space: nowrap; 
        display: flex;
        flex-direction: row;
        align-items: center;
        justify-content: center;
        width: 100%;
    }}

    #spin-text span {{
        display: inline-block;
        opacity: 0;
        transform-origin: center;
        animation: spinFlip 5s infinite; 
    }}

    /* අකුරු වලට නිල් සහ සුදු පාට (Icy Blue Glow) ලබා දීම */
    #spin-text span.letter {{
        background: linear-gradient(0deg, #0044ff 0%, #00bfff 50%, #ffffff 100%);
        background-size: 100% 200%;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        -webkit-text-stroke: 1.5px #FFFFFF;
        
        animation-name: spinFlip, blueFlow;
        animation-duration: 5s, 2s;
        animation-iteration-count: infinite, infinite;
        animation-timing-function: ease, linear;
        animation-direction: normal, alternate;

        filter: drop-shadow(0px -2px 6px rgba(0, 191, 255, 0.8)) drop-shadow(3px 3px 5px rgba(0,0,0,1));
    }}

    #spin-text span.icon {{
        -webkit-text-stroke: 0px transparent !important; 
        color: initial !important; 
        filter: drop-shadow(2px 2px 4px rgba(0,0,0,0.8)); 
    }}

    @keyframes spinFlip {{
        0% {{ transform: rotateY(90deg) rotateX(90deg) scale(0.5); opacity: 0; }}
        15% {{ transform: rotateY(0deg) rotateX(0deg) scale(1); opacity: 1; }}
        85% {{ transform: rotateY(0deg) rotateX(0deg) scale(1); opacity: 1; }}
        100% {{ transform: rotateY(-90deg) rotateX(-90deg) scale(0.5); opacity: 0; }}
    }}

    @keyframes blueFlow {{
        0% {{ background-position: 0% 100%; }}
        100% {{ background-position: 0% 0%; }}
    }}
</style>

<div class="animated-border-wrapper">
    <div class="header-image-container">
        <div id="spin-text">
            {spans_html}
        </div>
    </div>
</div>
"""
components.html(header_html, height=240)

# --- Navigation Menu ---
menu = ["භාණ්ඩ බලන්න (Home)", "කළමනාකරුට පමණයි (Admin)"]
choice = st.sidebar.selectbox("මෙනුව තෝරන්න", menu, key="menu_selection")

# --- Login Logic ---
if choice == "කළමනාකරුට පමණයි (Admin)" and not st.session_state.logged_in:
    st.sidebar.markdown("---")
    st.sidebar.info("මුරපදය ඇතුලත් කරන්න:")
    with st.sidebar.form("login_form"):
        password = st.text_input("මුරපදය (Password)", type="password")
        if st.form_submit_button("ඇතුලත් වන්න (Enter)"):
            if password == ADMIN_PASSWORD:
                st.sidebar.success("මුරපදය නිවැරදියි! ✅")
                st.session_state.logged_in = True
                st.rerun() 
            else:
                st.sidebar.error("මුරපදය වැරදියි! නැවත උත්සාහ කරන්න.")

# --- Home Page ---
if choice == "භාණ්ඩ බලන්න (Home)":
    
    # --- Fiery Subheader ---
    fire_subheader_html = """
    <style>
        .fire-card {
            border: 2px solid #FF4500;
            border-radius: 15px;
            padding: 15px;
            background: #0a0a0a;
            text-align: center;
            box-shadow: 0 0 15px rgba(255, 69, 0, 0.4), inset 0 0 20px rgba(255, 0, 0, 0.2);
            margin-bottom: 25px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }
        .fire-text {
            font-size: clamp(20px, 5.5vw, 32px);
            font-family: 'Arial Black', Impact, sans-serif;
            font-weight: 900;
            margin: 0;
            background: linear-gradient(0deg, #ff0000 0%, #ff8c00 50%, #ffd700 100%);
            background-size: 100% 200%;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: fireFlow 1.5s infinite linear alternate;
            filter: drop-shadow(0px -2px 6px rgba(255,69,0,0.8));
        }
        @keyframes fireFlow {
            0% { background-position: 0% 100%; }
            100% { background-position: 0% 0%; }
        }
        .fire-icon {
            font-size: clamp(22px, 6vw, 35px);
            display: inline-block;
            animation: bounceGlow 2s infinite ease-in-out;
        }
        @keyframes bounceGlow {
            0%, 100% { transform: translateY(0); filter: drop-shadow(0 0 5px rgba(255,140,0,0.5)); }
            50% { transform: translateY(-5px); filter: drop-shadow(0 5px 15px rgba(255,215,0,0.9)); }
        }
    </style>
    <div class="fire-card">
        <span class="fire-icon">💎</span>
        <span class="fire-text">අපගේ නවතම PRODUCTS</span>
        <span class="fire-icon">🛍️</span>
    </div>
    """
    st.markdown(fire_subheader_html, unsafe_allow_html=True)
    
    if not st.session_state.products: 
        st.info("දැනට භාණ්ඩ කිසිවක් ඇතුලත් කර නොමැත.")
        
    for idx, p in enumerate(st.session_state.products):
        # WhatsApp සහ Call Buttons වල පින්තූර ලබා ගැනීම
        wa_b64 = get_image_base64("whatsapp_button.png")
        call_b64 = get_image_base64("call_now_1.png")
        
        # HTML සඳහා දත්ත සකස් කිරීම
        img_html = f'<img class="prod-img" src="data:image/png;base64,{p["image"]}">' if p.get('image') else ''
        desc_html = p['desc'].replace('\n', '<br>')
        
        wa_html = f'<a href="https://wa.me/{WHATSAPP_NUM}?text=මට මේ product එක ගැන දැනගන්න ඕනි: {p["name"]}" target="_blank" class="btn-wa"><img src="data:image/png;base64,{wa_b64}"></a>' if wa_b64 else ''
        call_html = f'<a href="tel:{CALL_NUM}" class="btn-call"><img src="data:image/png;base64,{call_b64}"></a>' if call_b64 else ''
        
        # Streamlit Container වෙනුවට අලුත්ම 100% වැඩ කරන Pure HTML Product Card එක
        prod_html = f"""
        <div class="product-neon-wrapper">
            <div class="product-inner-content">
                <h3>{p['name']}</h3>
                {img_html}
                <p style="font-size: 16px; margin-bottom: 10px; color: #ddd;"><strong>විස්තරය:</strong><br>{desc_html}</p>
                <p style="font-size: 18px; color: #F4D03F; margin-bottom: 10px;"><strong>මිල:</strong> රු. {p['price']}</p>
                <div class="product-buttons">
                    {wa_html}
                    {call_html}
                </div>
            </div>
        </div>
        """
        st.markdown(prod_html, unsafe_allow_html=True)

# --- Admin Page ---
elif choice == "කළමනාකරුට පමණයි (Admin)":
    if not st.session_state.logged_in:
        st.header("🔒 Admin Panel")
        st.info("👈 වම් පස මෙනුවෙන් මුරපදය ලබා දෙන්න.")
    else:
        st.header("Admin Panel (භාණ්ඩ කළමනාකරණය)")
        if st.button("ඉවත් වන්න (Logout)", on_click=logout_user): st.rerun()
        with st.form("add_product_form", clear_on_submit=True):
            st.subheader("➕ අලුත් භාණ්ඩයක්")
            p_name = st.text_input("නම")
            p_desc = st.text_area("විස්තරය")
            p_price = st.text_input("මිල (රු.)")
            p_image = st.file_uploader("ඡායාරූපය", type=["jpg", "png", "jpeg"])
            if st.form_submit_button("භාණ්ඩය ඇප් එකට දාන්න"):
                if p_name and p_price:
                    img_b64 = base64.b64encode(p_image.read()).decode() if p_image else ""
                    st.session_state.products.append({"name": p_name, "desc": p_desc, "price": p_price, "image": img_b64})
                    save_data(st.session_state.products)
                    st.success("සාර්ථකයි!")
        st.write("---")
        for i, p in enumerate(st.session_state.products):
            with st.container(border=True):
                col1, col2, col3 = st.columns([2, 1, 1])
                col1.write(f"**{p['name']}**")
                if col2.button("✏️ Edit", key=f"edit_{i}"): st.session_state.editing_index = i; st.rerun()
                if col3.button("🗑️ Delete", key=f"del_{i}"): st.session_state.products.pop(i); save_data(st.session_state.products); st.rerun()
        if st.session_state.editing_index is not None:
            idx = st.session_state.editing_index
            edit_prod = st.session_state.products[idx]
            with st.form("edit_product_form"):
                e_name = st.text_input("නම", value=edit_prod['name'])
                e_desc = st.text_area("විස්තරය", value=edit_prod['desc'])
                e_price = st.text_input("මිල", value=edit_prod['price'])
                e_image = st.file_uploader("අලුත් ඡායාරූපයක් (අවශ්‍ය නම් පමණක්)", type=["jpg", "png", "jpeg"])
                if st.form_submit_button("Save"):
                    img_b64 = base64.b64encode(e_image.read()).decode() if e_image else edit_prod['image']
                    st.session_state.products[idx] = {"name": e_name, "desc": e_desc, "price": e_price, "image": img_b64}
                    save_data(st.session_state.products); st.session_state.editing_index = None; st.rerun()
