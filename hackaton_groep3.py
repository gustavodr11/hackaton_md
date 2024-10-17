import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium


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
  st.header("Sloterdijk Poort Noord")
  
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
  fig.update_layout(title_text="Piechart Bedrijven per Sector en Energieverbruik 2023")

  st.plotly_chart(fig)


  # HEATMAP
  with st.container():
    st.subheader("Heatmap van Energieverbruik per Pand in Sloterdijk Poort Noord Amsterdam")

    df1 = pd.read_excel("Data_verbruik_v8.xlsx")
    df1 = df1.dropna(subset=['Latitude', 'Longitude'])

    df1["Totaal verbruik per week (kWh)"] = df1[["Verbruik maandag", "Verbruik dinsdag", "Verbruik woensdag", 
                                               "Verbruik donderdag", "Verbruik vrijdag"]].sum(axis=1)

    df1_grouped = df1.groupby(["pand", "Latitude", "Longitude"], as_index=False)["Totaal verbruik per week (kWh)"].sum()

    map_center = [52.395762704268726, 4.789355012543267]
    m = folium.Map(location=map_center, zoom_start=15)

    heat_data = [[row['Latitude'], row['Longitude'], row['Totaal verbruik per week (kWh)']] for index, row in df1_grouped.iterrows()]
    HeatMap(heat_data, radius=24, max_zoom=13).add_to(m)

    st_folium(m, width=700, height=500)


  # DAGELIJKS, WEEKELIJKS, MAANDELIJKS PLOTS
  # Lees het Excel-bestand in
  df2 = pd.read_excel('verbruik_persector_dwm.xlsx')

  # Kolomnamen specificeren die je wilt gebruiken
  sector_col = 'Sector'
  daily_columns = ['Verbruik maandag', 'Verbruik dinsdag', 'Verbruik woensdag', 'Verbruik donderdag', 'Verbruik vrijdag', 'Verbruik zaterdag', 'Verbruik zondag']
  weekly_col = 'Week verbruik'
  monthly_col = 'Maand verbruik'  # Correctie: Haakje verwijderd

  # Dagelijkse gegevens omzetten naar lange vorm voor gebruik in plot
  df_dagelijks = df2.melt(id_vars=sector_col, value_vars=daily_columns, 
                          var_name='Dag', value_name='Dagelijks Verbruik')

  # Dropdownmenu voor selectie (dagelijks, wekelijks of maandelijks verbruik)
  keuze = st.selectbox('Selecteer het type verbruik:', ['Dagelijks Verbruik', weekly_col, monthly_col])

  # Maak de visualisatie op basis van de kolomkeuze
  if keuze == 'Dagelijks Verbruik':
      # Lijnplot voor dagelijks verbruik
      fig2 = px.line(df_dagelijks, x='Dag', y='Dagelijks Verbruik', color=sector_col, 
                      title=f'{keuze} per dag per sector', 
                      labels={'Dagelijks Verbruik': 'Verbruik (kWh)', 'Dag': 'Dag van de week'},
                      markers=True)
  else:
      # Staafdiagram voor wekelijkse of maandelijkse verbruik
      fig2 = px.bar(df2, x=sector_col, y=keuze, color=sector_col, 
                      title=f'Energieverbruik per sector ({keuze})', 
                      labels={keuze: 'Verbruik (kWh)'})

  # Grafiek weergeven in Streamlit
  st.plotly_chart(fig2)


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
  
  st.subheader("Bestaande infrastructuur op het terrein")
  st.image("middenspanningskabels_ams.png", caption="Middenspanningskabels in Sloterdijk Poort Noord", use_column_width=True)
  
  st.subheader("Pandnummers Sloterijk Poort Noord")
  st.image("panden_ams.png", caption="Panden in Sloterdijk Poort Noord")


  # Streamlit layout
  st.subheader("Histogram van Zonnepanelen per Pand")

  # Zorg ervoor dat er geen null waarden zijn in de kolommen die je nodig hebt
  df1 = df1.dropna(subset=['pand', 'Aantal_zonnepanellen', 'Potentieel_zonnepanelen'])

  # Maak een histogram met Plotly
  fig3 = px.histogram(df1, x='pand', y=['Aantal_zonnepanellen', 'Potentieel_zonnepanelen'], 
                   barmode='group', 
                   title='Aantal Zonnepanelen en Potentieel per Pand')

  # Toon de grafiek in Streamlit
  st.plotly_chart(fig3)
