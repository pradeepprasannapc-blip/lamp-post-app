import streamlit as st
import json
import os
import base64

# --- App Configuration ---
st.set_page_config(page_title="Chathura Group", page_icon="✨", layout="centered")

# --- Custom CSS for Premium Borders with Colors ---
st.markdown("""
<style>
    /* සාමාන්‍ය බෝඩර් වල හැඩය (Product Cards සඳහා) */
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 15px !important;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2) !important;
        padding: 15px !important;
        border: 2px solid #5D6D7E !important; /* අළු පාට බෝඩර් එක */
    }
    
    /* Header එක සඳහා වෙනම පෙනුමක් (ලා නිල්/අළු) */
    .header-card {
        border: 3px solid #5DADE2; 
        border-radius: 20px;
        padding: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        margin-bottom: 20px;
        text-align: center;
    }
    
    /* Sub-header (නවතම products) සඳහා වෙනම පෙනුමක් (රන්වන් පැහැති) */
    .subheader-card {
        border: 3px solid #F4D03F;
        border-radius: 15px;
        padding: 10px;
        box-shadow: 0 3px 10px rgba(244, 208, 63, 0.3);
        margin-bottom: 25px;
        text-align: center;
        background-color: rgba(244, 208, 63, 0.05); /* ඉතාමත් ලා රන්වන් පසුබිමක් */
    }
</style>
""", unsafe_allow_html=True)

# --- Settings ---
DATA_FILE = "products.json"
WHATSAPP_NUM = "94779998189"  
CALL_NUM = "94779998189"      
ADMIN_PASSWORD = "8189"       

# --- Data Handling Functions ---
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            try:
                return json.load(f)
            except:
                return []
    return []

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

def get_image_base64(filepath):
    if os.path.exists(filepath):
        with open(filepath, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

if 'products' not in st.session_state:
    st.session_state.products = load_data()

# --- App UI and Navigation ---

# 1. Header පින්තූරය සහ නම අලුත් වර්ණ ගැන්වූ බෝඩර් එකක් ඇතුළත (HTML මගින්)
header_html = """
<div class="header-card">
"""
st.markdown(header_html, unsafe_allow_html=True)

image_path = "header.png" 
if os.path.exists(image_path):
    st.image(image_path, use_column_width=True)
elif os.path.exists("header.jpg"):
    st.image("header.jpg", use_column_width=True)

# නම එකම පේළියක පෙන්වීමට h2 පාවිච්චි කර ඇත (h1 වලට වඩා ටිකක් කුඩායි)
st.markdown("<h2 style='text-align: center; font-family: serif; margin-top: 10px; margin-bottom: 5px; font-weight: bold;'>✨ CHATHURA GROUP 🏛️</h2>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True) # Header බෝඩර් එක අවසන් කිරීම


menu = ["භාණ්ඩ බලන්න (Home)", "කළමනාකරුට පමණයි (Admin)"]
choice = st.sidebar.selectbox("මෙනුව තෝරන්න", menu)

# ---------------------------------------------------------
# 1. පාරිභෝගිකයින්ට පෙනෙන පිටුව
# ---------------------------------------------------------
if choice == "භාණ්ඩ බලන්න (Home)":
    
    # "අපගේ නවතම PRODUCTS" සඳහා රන්වන් පැහැති බෝඩර් එක
    st.markdown("""
    <div class="subheader-card">
        <h3 style='margin: 0; color: #3498DB;'>💎 අපගේ නවතම PRODUCTS 🛍️</h3>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.products:
        st.info("දැනට භාණ්ඩ කිසිවක් ඇතුලත් කර නොමැත. කරුණාකර පසුව පැමිණෙන්න.")
        
    for idx, p in enumerate(st.session_state.products):
        
        # සෑම භාණ්ඩයක්ම Streamlit container (අළු පාට බෝඩර්) එකක් ඇතුළත
        with st.container(border=True):
            st.subheader(p['name'])
            
            if p.get('image'):
                try:
                    img_bytes = base64.b64decode(p['image'])
                    st.image(img_bytes, use_column_width=True)
                except Exception as e:
                    st.error("පින්තූරය පෙන්වීමේ දෝෂයකි.")
                    
            st.write(f"**විස්තරය:** {p['desc']}")
            st.write(f"**මිල:** රු. {p['price']}")
            
            st.write("") 
            
            col1, col2 = st.columns(2)
            
            with col1:
                wa_b64 = get_image_base64("whatsapp_button.png")
                wa_msg = f"මට මේ product එක ගැන දැනගන්න ඕනි: {p['name']}"
                if wa_b64:
                    wa_html = f'<a href="https://wa.me/{WHATSAPP_NUM}?text={wa_msg}" target="_blank" style="display:flex; justify-content:center; align-items:center; width:100%; height:110px; border: 3px solid #25D366; border-radius: 20px; text-decoration:none; box-sizing:border-box;"><img src="data:image/png;base64,{wa_b64}" style="width:85%; height:85%; object-fit:contain;"></a>'
                    st.markdown(wa_html, unsafe_allow_html=True)
                else:
                    st.markdown(f"[💬 WhatsApp මගින් විමසන්න](https://wa.me/{WHATSAPP_NUM}?text={wa_msg})")
                    
            with col2:
                call_b64 = get_image_base64("call_now_1.png")
                if call_b64:
                    call_html = f'<a href="tel:{CALL_NUM}" style="display:flex; justify-content:center; align-items:center; width:100%; height:110px; border: 3px solid #FF8C00; border-radius: 20px; text-decoration:none; box-sizing:border-box;"><img src="data:image/png;base64,{call_b64}" style="width:85%; height:85%; object-fit:contain;"></a>'
                    st.markdown(call_html, unsafe_allow_html=True)
                else:
                    st.markdown(f"[📞 කෝල් එකක් ගන්න](tel:{CALL_NUM})")

# ---------------------------------------------------------
# 2. Admin Panel
# ---------------------------------------------------------
elif choice == "කළමනාකරුට පමණයි (Admin)":
    st.header("Admin Panel (භාණ්ඩ ඇතුලත් කිරීම)")
    
    password = st.text_input("මුරපදය (Password) ඇතුලත් කරන්න", type="password")
    
    if password == ADMIN_PASSWORD:
        st.success("සාර්ථකයි! ඔබට දැන් භාණ්ඩ ඇතුලත් කළ හැක.")
        
        with st.form("add_product_form", clear_on_submit=True):
            p_name = st.text_input("පහන් කණුවේ නම")
            p_desc = st.text_area("විස්තරය")
            p_price = st.text_input("මිල (රු.)")
            p_image = st.file_uploader("ඡායාරූපයක් තෝරන්න", type=["jpg", "png", "jpeg"])
            
            submit = st.form_submit_button("භාණ්ඩය ඇප් එකට දාන්න")
            
            if submit:
                if p_name and p_price:
                    img_b64 = ""
                    if p_image is not None:
                        img_b64 = base64.b64encode(p_image.read()).decode()
                        
                    new_product = {
                        "name": p_name,
                        "desc": p_desc,
                        "price": p_price,
                        "image": img_b64
                    }
                    
                    st.session_state.products.append(new_product)
                    save_data(st.session_state.products)
                    st.success(f"'{p_name}' සාර්ථකව ඇතුලත් කරන ලදී! 'භාණ්ඩ බලන්න' පිටුවට ගොස් පරීක්ෂා කරන්න.")
                else:
                    st.error("කරුණාකර නම සහ මිල අනිවාර්යයෙන් ඇතුලත් කරන්න.")
                    
        st.write("---")
        st.subheader("දැනට ඇති භාණ්ඩ ඉවත් කරන්න")
        for i, p in enumerate(st.session_state.products):
            with st.container(border=True): 
                col1, col2 = st.columns([3, 1])
                col1.write(p['name'])
                if col2.button("මකන්න", key=f"del_{i}"):
                    st.session_state.products.pop(i)
                    save_data(st.session_state.products)
                    st.rerun()

    elif password != "":
        st.error("මුරපදය වැරදියි!")
