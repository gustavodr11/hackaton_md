import streamlit as st
from streamlit_option_menu import option_menu


st.set_page_config(page_title='Hackaton Minor Datascience 2024 (groep 3)', page_icon='💻')

# sidebar
with st.sidebar: 
  selected = option_menu(menu_title="Menu", options=["Intro", "Energievraag Sectoren", "Zonnepanelen"], icons=["play", "building-up", "sun"], menu_icon="list")

# --------------------------------------------------------------------------

# INTRO pagina
if selected == 'Intro':
    st.title("Hackaton - Groep 3 ")
    
    
    # Bronnen
    st.write("### Gebruikte Bronnen:")
    st.write("""
        - [Youtube filmpje](https://www.youtube.com/watch?v=hEPoto5xp3k)
        - [Streamlit documentatie](https://docs.streamlit.io/)
    """)
    

# --------------------------------------------------------------------------

# ENERGIEVRAAG SECTOREN pagina
if selected == "Energievraag Sectoren": 
  st.title("Energievraag Sectoren") 
  

# --------------------------------------------------------------------------

if selected == 'Zonnepanelen':
  st.title("Zonnepanelen")
