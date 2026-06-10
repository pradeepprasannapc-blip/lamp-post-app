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
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 15px !important;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2) !important;
        padding: 15px !important;
        border: 2px solid #5D6D7E !important; 
    }
    .subheader-card {
        border: 3px solid #F4D03F; border-radius: 15px; padding: 10px;
        box-shadow: 0 3px 10px rgba(244, 208, 63, 0.3); margin-bottom: 25px;
        text-align: center; background-color: rgba(244, 208, 63, 0.05); 
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

# --- නව Header එක (අකුරු ෆෝන් එකට ගැලපෙන ලෙස සාදා ඇත) ---
header_file = "header.png" if os.path.exists("header.png") else "header.jpg"
header_b64 = get_image_base64(header_file)

# පින්තූරය පසුබිමට දැමීම
bg_style = f"background-image: url(data:image/png;base64,{header_b64}); background-size: cover; background-position: center;" if header_b64 else "background-color: #111;"

# අකුරු සහ අයිකන් වෙන් කර HTML සැකසීම
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

header_html = f"""
<style>
    .header-image-container {{
        position: relative;
        width: 100%;
        height: 220px;
        border-radius: 15px;
        border: 3px solid #5DADE2;
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        margin-bottom: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        overflow: hidden;
        {bg_style}
    }}
    
    #spin-text {{
        /* ෆෝන් ස්ක්‍රීන් එකට හරියටම ගැලපෙන්න සයිස් එක හැදුවා */
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

    /* අකුරු වලට පමණක් ලා නිල් පාට බෝඩර් එක සහ සුදු පාට දැමීම */
    #spin-text span.letter {{
        color: #FFFFFF;
        -webkit-text-stroke: 1.5px #5DADE2; /* පින්තූරය වටේ තියෙන බෝඩර් එකේ පාට */
        text-shadow: 2px 2px 0 #000, -1px -1px 0 #000, 4px 4px 10px rgba(0,0,0,0.8);
    }}

    /* Emojis වල ඔරිජිනල් පාට පෙනීමට */
    #spin-text span.icon {{
        -webkit-text-stroke: 0px transparent !important; 
        color: initial !important; 
        filter: drop-shadow(2px 2px 4px rgba(0,0,0,0.8)); /* අයිකන් වලට සාමාන්‍ය සෙවනැල්ලක් */
    }}

    @keyframes spinFlip {{
        0% {{ transform: rotateY(90deg) rotateX(90deg) scale(0.5); opacity: 0; }}
        15% {{ transform: rotateY(0deg) rotateX(0deg) scale(1); opacity: 1; }}
        85% {{ transform: rotateY(0deg) rotateX(0deg) scale(1); opacity: 1; }}
        100% {{ transform: rotateY(-90deg) rotateX(-90deg) scale(0.5); opacity: 0; }}
    }}
</style>

<div class="header-image-container">
    <div id="spin-text">
        {spans_html}
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
    st.markdown("<div class='subheader-card'><h3 style='margin: 0; color: #3498DB;'>💎 අපගේ නවතම PRODUCTS 🛍️</h3></div>", unsafe_allow_html=True)
    if not st.session_state.products: st.info("දැනට භාණ්ඩ කිසිවක් ඇතුලත් කර නොමැත.")
    for idx, p in enumerate(st.session_state.products):
        with st.container(border=True):
            st.subheader(p['name'])
            if p.get('image'): st.image(base64.b64decode(p['image']), use_column_width=True)
            st.write(f"**විස්තරය:** {p['desc']}")
            st.write(f"**මිල:** රු. {p['price']}")
            col1, col2 = st.columns(2)
            wa_b64 = get_image_base64("whatsapp_button.png")
            call_b64 = get_image_base64("call_now_1.png")
            with col1:
                if wa_b64: st.markdown(f'<a href="https://wa.me/{WHATSAPP_NUM}?text=මට මේ product එක ගැන දැනගන්න ඕනි: {p["name"]}" target="_blank" style="display:flex; justify-content:center; align-items:center; width:100%; height:110px; border: 3px solid #25D366; border-radius: 20px; text-decoration:none;"><img src="data:image/png;base64,{wa_b64}" style="width:85%; height:85%; object-fit:contain;"></a>', unsafe_allow_html=True)
            with col2:
                if call_b64: st.markdown(f'<a href="tel:{CALL_NUM}" style="display:flex; justify-content:center; align-items:center; width:100%; height:110px; border: 3px solid #FF8C00; border-radius: 20px; text-decoration:none;"><img src="data:image/png;base64,{call_b64}" style="width:85%; height:85%; object-fit:contain;"></a>', unsafe_allow_html=True)

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
