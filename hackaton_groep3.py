import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


st.set_page_config(page_title='Hackaton Minor Datascience 2024 (groep 3)', page_icon='💻')

# sidebar
with st.sidebar: 
  selected = option_menu(menu_title="Menu", options=["Intro", "Energievraag Sectoren", "Zonnepanelen"], icons=["play", "building-up", "sun"], menu_icon="list")

# --------------------------------------------------------------------------

# INTRO pagina
if selected == 'Intro':
    st.title("Hackaton - Groep 3")
    
    
    # Bronnen
    st.write("### Gebruikte Bronnen:")
    st.write("""
        - [Energieverbruik per sector](https://opendata.cbs.nl/statline/#/CBS/nl/dataset/83989NED/table?dl=21D0E)
        - [Aantal bedrijven per sector](https://opendata.cbs.nl/#/CBS/nl/dataset/81589NED/table?searchKeywords=voeding)
        - [Opbrengst zonnepanelen](https://waternet.omgevingswarmte.nl/waternet#c9eaed99-a69e-48eb-9642-61c0e0b77078)
    """)
    

# --------------------------------------------------------------------------

# ENERGIEVRAAG SECTOREN pagina
if selected == "Energievraag Sectoren": 
  st.title("Energievraag Sectoren")
  st.subheader("Sloterdijk Poort Noord")
  
  # PIECHART
  sectoren = ['Non-ferrobedrijven', 'Vervoer en opslag', 'Houtindustrie', 
            'Groothandel/hygiene', 'Voedings en genotsmiddelen', 'Auto-industrie', 
            'Farmaceutische industrie', 'Drankindustrie', 'Leidingen industrie']

  aantal_2023 = [15.29, 3.26, 0.76, 30.13, 2.78, 14.17, 12.11, 0.57, 20.93]

  # Piechart subplot
  fig = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]],
                      subplot_titles=["Bedrijven per Sector", "Energieverbruik 2023"])

  fig.add_trace(go.Pie(labels=sectoren, values=[1, 12, 1, 1, 1, 4, 2, 1, 1], 
                       name="Aantal bedrijven per sector"), row=1, col=1)
  fig.add_trace(go.Pie(labels=sectoren, values=aantal_2023, name="Energieverbruik 2023"), row=1, col=2)
  fig.update_layout(title_text="Vergelijking: Bedrijven per Sector en Energieverbruik 2023")

  st.plotly_chart(fig)


  # SUBPLOTS
  df = pd.read_excel('Energieverbruik_ddjh2_0.xlsx')

  # Checkbox 
  limit_checkbox = st.checkbox('Beperk de y-as tot een maximum van 0.3')

  fig, axes = plt.subplots(3, 3, figsize=(18, 12))

  # regplots
  sns.regplot(ax=axes[0, 0], data=df, x='years', y='Non-ferrobedrijven')
  axes[0, 0].set_title(sectoren[0])
  sns.regplot(ax=axes[0, 1], data=df[df['years'] >= 2010], x="years", y="Vervoer en opslag")
  axes[0, 1].set_title(sectoren[1])
  sns.regplot(ax=axes[0, 2], data=df, x='years', y='Houtindustrie')
  axes[0, 2].set_title(sectoren[2])
  sns.regplot(ax=axes[1, 0], data=df[df['years'] >= 2011], x='years', y='Groothandel/hygiene')
  axes[1, 0].set_title(sectoren[3])
  sns.regplot(ax=axes[1, 1], data=df, x='years', y='Voedings en genotsmiddelen')
  axes[1, 1].set_title(sectoren[4])
  sns.regplot(ax=axes[1, 2], data=df[df['years'] >= 1995], x='years', y='Auto-industrie')
  axes[1, 2].set_title(sectoren[5])
  sns.regplot(ax=axes[2, 0], data=df[df['years'] >= 2011], x='years', y='Farmaceutische industrie')
  axes[2, 0].set_title(sectoren[6])
  sns.regplot(ax=axes[2, 1], data=df[df['years'] >= 1995], x='years', y='Drankindustrie')
  axes[2, 1].set_title(sectoren[7])
  sns.regplot(ax=axes[2, 2], data=df[df['years'] >= 2011], x='years', y='Leidingen industrie')
  axes[2, 2].set_title(sectoren[8])

  for ax in axes.flat:
      ax.set_ylabel("Energieverbruik [PJ]")
      if limit_checkbox:
          ax.set_ylim(top=0.3)  

  plt.tight_layout()

  st.pyplot(fig)
  

# --------------------------------------------------------------------------

# ZONNEPANELEN pagina
if selected == 'Zonnepanelen':
  st.title("Zonnepanelen")
