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
    .header-card {
        border: 3px solid #5DADE2; border-radius: 20px; padding: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.3); margin-bottom: 20px;
        text-align: center; background-color: rgba(93, 173, 226, 0.05);
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

# --- UI ---
header_file = "header.png" if os.path.exists("header.png") else "header.jpg"
header_b64 = get_image_base64(header_file)
st.markdown(f"""
    <div class="header-card">
        {'<img src="data:image/png;base64,'+header_b64+'" style="width:100%; border-radius:10px; margin-bottom: 15px; object-fit: cover;">' if header_b64 else ''}
        <h2 style='text-align: center; font-family: serif; margin-top: 0px; margin-bottom: 5px; font-weight: bold;'>✨ CHATHURA GROUP 👥</h2>
    </div>
""", unsafe_allow_html=True)

menu = ["භාණ්ඩ බලන්න (Home)", "කළමනාකරුට පමණයි (Admin)"]
choice = st.sidebar.selectbox("මෙනුව තෝරන්න", menu, key="menu_selection")

# --- Logic ---
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
                if st.form_submit_button("Save"):
                    st.session_state.products[idx] = {"name": e_name, "desc": e_desc, "price": e_price, "image": edit_prod['image']}
                    save_data(st.session_state.products); st.session_state.editing_index = None; st.rerun()
