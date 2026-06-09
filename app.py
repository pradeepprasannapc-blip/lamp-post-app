import streamlit as st
import json
import os
import base64

# --- App Configuration ---
st.set_page_config(page_title="අපේ පහන් කණු", page_icon="💡", layout="centered")

# --- Settings (මෙතන ඔයාගේ විස්තර වෙනස් කරන්න) ---
DATA_FILE = "products.json"
WHATSAPP_NUM = "94770000000"  # ඔයාගේ WhatsApp නම්බර් එක (94 න් පටන් ගන්න, + එපා)
CALL_NUM = "+94770000000"     # ඔයාගේ සාමාන්‍ය ෆෝන් නම්බර් එක
ADMIN_PASSWORD = "123"        # ඇප් එකට විස්තර දාන්න ඔයා පාවිච්චි කරන පාස්වර්ඩ් එක

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

if 'products' not in st.session_state:
    st.session_state.products = load_data()

# --- App UI and Navigation ---
st.title("💡 අපේ පහන් කණු ව්‍යාපාරය")

menu = ["භාණ්ඩ බලන්න (Home)", "කළමනාකරුට පමණයි (Admin)"]
choice = st.sidebar.selectbox("මෙනුව තෝරන්න", menu)

# ---------------------------------------------------------
# 1. පාරිභෝගිකයින්ට පෙනෙන පිටුව (Public View)
# ---------------------------------------------------------
if choice == "භාණ්ඩ බලන්න (Home)":
    st.header("අපගේ නවතම පහන් කණු වර්ග")
    
    if not st.session_state.products:
        st.info("දැනට භාණ්ඩ කිසිවක් ඇතුලත් කර නොමැත. කරුණාකර පසුව පැමිණෙන්න.")
        
    for idx, p in enumerate(st.session_state.products):
        st.subheader(p['name'])
        
        # පින්තූරය පෙන්වීම
        if p.get('image'):
            try:
                img_bytes = base64.b64decode(p['image'])
                st.image(img_bytes, use_column_width=True)
            except Exception as e:
                st.error("පින්තූරය පෙන්වීමේ දෝෂයකි.")
                
        st.write(f"**විස්තරය:** {p['desc']}")
        st.write(f"**මිල:** රු. {p['price']}")
        
        # Contact Buttons
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"[💬 WhatsApp මගින් විමසන්න](https://wa.me/{WHATSAPP_NUM}?text=මට මේ පහන් කණුව ගැන දැනගන්න ඕනේ: {p['name']})")
        with col2:
            st.markdown(f"[📞 කෝල් එකක් ගන්න](tel:{CALL_NUM})")
        st.markdown("---")

# ---------------------------------------------------------
# 2. ඔයාට පමණක් පෙනෙන පිටුව (Admin Panel)
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
                        # පින්තූරය Base64 විදිහට save කරගැනීම
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
                    
        # දැනට තියෙන භාණ්ඩ මකා දැමීම (Delete option)
        st.write("---")
        st.subheader("දැනට ඇති භාණ්ඩ ඉවත් කරන්න")
        for i, p in enumerate(st.session_state.products):
            col1, col2 = st.columns([3, 1])
            col1.write(p['name'])
            if col2.button("මකන්න", key=f"del_{i}"):
                st.session_state.products.pop(i)
                save_data(st.session_state.products)
                st.rerun()

    elif password != "":
        st.error("මුරපදය වැරදියි!")
