import streamlit as st
import streamlit.components.v1 as components
import json
import os
import base64

# --- App Configuration ---
st.set_page_config(page_title="Chathura Group", page_icon="✨", layout="centered")

# --- Custom CSS for Premium Borders with Colors ---
st.markdown("""
<style>
    div[data-testid="stVerticalBlockBorderWrapper"] {
        border-radius: 15px !important;
        box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2) !important;
        padding: 15px !important;
        border: 2px solid #5D6D7E !important; 
    }
    
    .header-card {
        border: 3px solid #5DADE2; 
        border-radius: 20px;
        padding: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        margin-bottom: 20px;
        text-align: center;
        background-color: rgba(93, 173, 226, 0.05);
    }
    
    .subheader-card {
        border: 3px solid #F4D03F;
        border-radius: 15px;
        padding: 10px;
        box-shadow: 0 3px 10px rgba(244, 208, 63, 0.3);
        margin-bottom: 25px;
        text-align: center;
        background-color: rgba(244, 208, 63, 0.05); 
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

# --- Session States ---
if 'products' not in st.session_state:
    st.session_state.products = load_data()
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'menu_selection' not in st.session_state:
    st.session_state.menu_selection = "භාණ්ඩ බලන්න (Home)"
if 'editing_index' not in st.session_state:
    st.session_state.editing_index = None
if 'close_sidebar' not in st.session_state:
    st.session_state.close_sidebar = False

# Logout Function
def logout_user():
    st.session_state.logged_in = False
    st.session_state.menu_selection = "භාණ්ඩ බලන්න (Home)"
    st.session_state.editing_index = None

# --- App UI and Navigation ---

# Header පින්තූරය සහ නම
header_file = "header.png" if os.path.exists("header.png") else "header.jpg"
header_b64 = get_image_base64(header_file)

if header_b64:
    header_html = f"""
    <div class="header-card">
        <img src="data:image/png;base64,{header_b64}" style="width:100%; border-radius:10px; margin-bottom: 15px; object-fit: cover;">
        <h2 style='text-align: center; font-family: serif; margin-top: 0px; margin-bottom: 5px; font-weight: bold;'>✨ CHATHURA GROUP 👥</h2>
    </div>
    """
else:
    header_html = """
    <div class="header-card">
        <h2 style='text-align: center; font-family: serif; margin-top: 5px; margin-bottom: 5px; font-weight: bold;'>✨ CHATHURA GROUP 👥</h2>
    </div>
    """
st.markdown(header_html, unsafe_allow_html=True)

menu = ["භාණ්ඩ බලන්න (Home)", "කළමනාකරුට පමණයි (Admin)"]
choice = st.sidebar.selectbox("මෙනුව තෝරන්න", menu, key="menu_selection")

# --- Sidebar Login (පැත්තෙන් Password ගැසීමට) ---
if choice == "කළමනාකරුට පමණයි (Admin)" and not st.session_state.logged_in:
    st.sidebar.markdown("---")
    st.sidebar.info("කරුණාකර ඇතුලත් වීමට මුරපදය ලබා දෙන්න.")
    
    with st.sidebar.form("login_form"):
        password = st.text_input("මුරපදය (Password)", type="password")
        submit_login = st.form_submit_button("ඇතුලත් වන්න (Enter)")
        
        if submit_login:
            if password == ADMIN_PASSWORD:
                st.session_state.logged_in = True
                st.session_state.close_sidebar = True # ලොග් වූ වහාම Sidebar එක වැසීමට
                st.rerun() 
            else:
                st.sidebar.error("මුරපදය වැරදියි! නැවත උත්සාහ කරන්න.")

# ---------------------------------------------------------
# 1. පාරිභෝගිකයින්ට පෙනෙන පිටුව
# ---------------------------------------------------------
if choice == "භාණ්ඩ බලන්න (Home)":
    
    st.markdown("""
    <div class="subheader-card">
        <h3 style='margin: 0; color: #3498DB;'>💎 අපගේ නවතම PRODUCTS 🛍️</h3>
    </div>
    """, unsafe_allow_html=True)
    
    if not st.session_state.products:
        st.info("දැනට භාණ්ඩ කිසිවක් ඇතුලත් කර නොමැත. කරුණාකර පසුව පැමිණෙන්න.")
        
    for idx, p in enumerate(st.session_state.products):
        
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
    
    # නව සහ වඩාත් සාර්ථක Auto Close Sidebar JS Script එක (Time delay එකක් සහිතව)
    if st.session_state.close_sidebar:
        components.html(
            """
            <script>
                // තත්පර බාගයක් (500ms) පරක්කු කරලා තමයි Sidebar එක වහන්නේ
                setTimeout(function() {
                    var doc = window.parent.document;
                    
                    // ක්‍රමය 1: Close sidebar බොත්තම හොයාගෙන click කිරීම
                    var buttons = doc.querySelectorAll('button');
                    for (var i = 0; i < buttons.length; i++) {
                        if (buttons[i].getAttribute('aria-label') === 'Close sidebar') {
                            buttons[i].click();
                            return;
                        }
                    }
                    
                    // ක්‍රමය 2: ෆෝන් වලදී Sidebar එකට පිටින් තියෙන අඳුරු පසුබිම Click කිරීම
                    var overlay = doc.querySelector('[data-testid="stSidebar"] + div');
                    if (overlay) {
                        overlay.click();
                    }
                }, 500);
            </script>
            """,
            height=0,
            width=0,
        )
        st.session_state.close_sidebar = False
    
    if not st.session_state.logged_in:
        st.info("👈 කරුණාකර වම් පසින් ඇති මෙනුවෙන් මුරපදය (Password) ඇතුලත් කර 'Enter' ඔබන්න.")
                
    else:
        st.header("Admin Panel (භාණ්ඩ කළමනාකරණය)")
        
        col1, col2 = st.columns([3, 1])
        with col2:
            st.button("ඉවත් වන්න (Logout)", on_click=logout_user)
                
        st.success("සාර්ථකයි! ඔබට දැන් භාණ්ඩ ඇතුලත් කළ හැක.")
        
        # --- Add New Product Form ---
        with st.form("add_product_form", clear_on_submit=True):
            st.subheader("➕ අලුත් භාණ්ඩයක් ඇතුලත් කරන්න")
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
        st.subheader("දැනට ඇති භාණ්ඩ කළමනාකරණය (Edit & Delete)")
        
        # --- Edit Product Form ---
        if st.session_state.editing_index is not None:
            idx = st.session_state.editing_index
            if idx < len(st.session_state.products):
                edit_prod = st.session_state.products[idx]
                st.info(f"✏️ ඔබ දැන් වෙනස් කරන්නේ: **{edit_prod['name']}**")
                
                with st.form("edit_product_form"):
                    e_name = st.text_input("නම", value=edit_prod['name'])
                    e_desc = st.text_area("විස්තරය", value=edit_prod['desc'])
                    e_price = st.text_input("මිල (රු.)", value=edit_prod['price'])
                    e_image = st.file_uploader("අලුත් ඡායාරූපයක් අවශ්‍ය නම් පමණක් තෝරන්න", type=["jpg", "png", "jpeg"])

                    colA, colB = st.columns(2)
                    submit_edit = colA.form_submit_button("සේව් කරන්න (Save)")
                    cancel_edit = colB.form_submit_button("අවලංගු කරන්න (Cancel)")

                    if submit_edit:
                        if e_name and e_price:
                            img_b64 = edit_prod['image'] 
                            if e_image is not None:
                                img_b64 = base64.b64encode(e_image.read()).decode()

                            st.session_state.products[idx] = {
                                "name": e_name,
                                "desc": e_desc,
                                "price": e_price,
                                "image": img_b64
                            }
                            save_data(st.session_state.products)
                            st.session_state.editing_index = None
                            st.success("සාර්ථකව වෙනස් කරන ලදී!")
                            st.rerun()
                        else:
                            st.error("නම සහ මිල අනිවාර්යයෙන් ඇතුලත් කරන්න.")

                    if cancel_edit:
                        st.session_state.editing_index = None
                        st.rerun()
        
        # --- List of Existing Products ---
        for i, p in enumerate(st.session_state.products):
            with st.container(border=True): 
                col1, col2, col3 = st.columns([2, 1, 1])
                col1.write(f"**{p['name']}**")
                
                if col2.button("✏️ Edit", key=f"edit_{i}"):
                    st.session_state.editing_index = i
                    st.rerun()
                    
                if col3.button("🗑️ Delete", key=f"del_{i}"):
                    if st.session_state.editing_index == i:
                        st.session_state.editing_index = None
                    st.session_state.products.pop(i)
                    save_data(st.session_state.products)
                    st.rerun()
