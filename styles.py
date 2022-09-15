# remove padding from body
remove_padding = """
        <style>
         .block-container {
           padding-top: 0rem;
           }
        </style>"""
st.markdown(remove_padding, unsafe_allow_html = True)

# hide main menu
hide_streamlit_style = """
        <style>
         #MainMenu, header, footer {
              visibility: hidden;
              }
        section[data-testid="stSidebar"] div:first-child {
             top: 0;
             }
        </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html = True) 

# button style
button_style = """
        <style>
        .stButton > button {
            color: white;
            background: #242124;
        }
        </style>
        """
st.sidebar.markdown(button_style, unsafe_allow_html = True)

# download button style
dwnl_button_style = """
        <style>
        .stDownloadButton > button {
            color: white;
            background: #00a1de; 
        } 
        .stDownloadButton > button:hover {
            color:white;
    }
        </style>
        """
st.sidebar.markdown(dwnl_button_style, unsafe_allow_html = True)

# bold expander label
expander_label = """
<style>
.streamlit-expanderHeader {
    font-weight: bold;
    border-bottom-style: solid;
}
</style>
"""
st.markdown(expander_label, 
            unsafe_allow_html = True)

# background picture
def set_bg(main_bg):
    main_bg_ext = "png"      
    st.markdown(
         f"""
         <style>
         .stApp {{
             background: url(data:image/{main_bg_ext};base64,{base64.b64encode(open(main_bg, "rb").read()).decode()});
             background-size: 20% 100%;
             background-repeat: no-repeat;
             background-position: right top;
         }}
         </style>
         """,
         unsafe_allow_html = True)