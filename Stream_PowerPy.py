####################
# Import packages 
####################
from typing import Literal
from bokeh.core.property.primitive import String
import streamlit as st
from bokeh.plotting import figure, show
import pandas as pd
import time
from math import pi
from bokeh.plotting import figure, output_notebook, show, ColumnDataSource, output_file, save
from bokeh.models import FactorRange, Legend, DatetimeTickFormatter, formatters, HoverTool, LinearAxis, Range1d, LabelSet, Label, Arrow, NormalHead, OpenHead
from bokeh.palettes import Bokeh, Category20c
from bokeh.transform import factor_cmap, dodge
from bokeh.models.widgets import Panel, Tabs
from bokeh.core.properties import value


####################
# Page Titre et Configuration 
####################
st.set_page_config(
     page_title="PowerPy",
     page_icon="🧊",
     layout="wide",
     initial_sidebar_state="expanded" 
)

st.image("ener3.png", use_column_width = True)
st.title("Prédiction de la Consommation d'Électricité" )

st.sidebar.title("Projet : PowerPy")
st.sidebar.header("Options")

st.write("""
Objectif : Prédire la Consommation Moyenne en MW en Ile de France
""")

st.text("")


####################
# Text Box 
####################

# Variables + description
st.write("### Variables du jeu de données")
st.text("")

# Charger les données description_donnees
description_donnees = pd.read_csv('./predictions_csv/Description_donnees.csv', sep=';')

st.dataframe(description_donnees)


# Afficher les valeurs des variables Code INSEE et Region
Detail_Region = description_donnees.Valeurs[1]
if st.checkbox('Afficher les valeurs de la variable Région'):
   Detail_Region
Detail_Insee = description_donnees.Valeurs[0]
if st.checkbox('Afficher les valeurs de la variable Code INSEE'):
   Detail_Insee

# Dimensions DF
st.write("Dimension DataFrame Séries Temporelles : (2891, **2**)")
st.write("Dimension DataFrame Modèles de Régression : (2891, 29)")
st.text("")

# Evolution de la consommation et de la production
st.write("### Évolution de la Consommation / Production d'Électricité")

####################
# Chargement des données
####################

# Charger les données df_evo_conso
df_evo_conso = pd.read_csv('./predictions_csv/df_evo_conso.csv', sep=';', index_col=0, parse_dates=['Date'])

# Charger les données df_evo_conso sans fluctuations 
df_evo_conso_sans = pd.read_csv('./predictions_csv/def_evo_conso_sans.csv', sep=';', index_col=0, parse_dates=['Date'])

# Charger les données de Production df_group_date_prod
df_group_date_prod = pd.read_csv('./predictions_csv/df_group_date_prod.csv', sep=',', index_col=0)
df_group_date_prod['Annee'] = df_group_date_prod['Annee'].astype(str)

# Charger les données df_group et df_group_somme
df_group = pd.read_csv('./predictions_csv/df_group.csv', sep=',', index_col=0)
df_group_somme = pd.read_csv('./predictions_csv/df_group_somme.csv', sep=',', index_col=0)

# Chargement des prédictions
ridge_model_1 = pd.read_csv('./predictions_csv/Ridge.csv', sep=',', index_col=0, parse_dates=[0])
lasso_model_1 = pd.read_csv('./predictions_csv/Lasso.csv', sep=',', index_col=0, parse_dates=[0])
EN_model = pd.read_csv('./predictions_csv/Elastic.csv', sep=',', index_col=0, parse_dates=[0])
sgd_model = pd.read_csv('./predictions_csv/SGD.csv', sep=',', index_col=0, parse_dates=[0])
model_arima_df = pd.read_csv('./predictions_csv/Arima.csv', sep=',', index_col=0, parse_dates=[0])
model_sarima_df = pd.read_csv('./predictions_csv/Sarima.csv', sep=',', index_col=0, parse_dates=[0])
model_sarimax_df = pd.read_csv('./predictions_csv/Sarimax.csv', sep=',', index_col=0, parse_dates=[0])
model_sarimaxlog_df = pd.read_csv('./predictions_csv/SarimaxLog.csv', sep=',', index_col=0, parse_dates=[0])

# Chargement de résultats scores
comparaison_scores = pd.read_csv('./predictions_csv/Scores.csv', sep=',', index_col=0)


####################
# Texte Box / Cases à cocher
####################

# Case à cocher 1
if st.checkbox("Voir l'évolution de la Consommation d'Électricité ?"): 

    # Source de données pour les graphiques
    source1 = ColumnDataSource(df_evo_conso[df_evo_conso['Code INSEE région']== 11])
    source2 = ColumnDataSource(df_evo_conso[df_evo_conso['Code INSEE région']== 24])
    source3 = ColumnDataSource(df_evo_conso[df_evo_conso['Code INSEE région']== 27])
    source4 = ColumnDataSource(df_evo_conso[df_evo_conso['Code INSEE région']== 28])
    source5 = ColumnDataSource(df_evo_conso[df_evo_conso['Code INSEE région']== 32])
    source6 = ColumnDataSource(df_evo_conso[df_evo_conso['Code INSEE région']== 44])
    source7 = ColumnDataSource(df_evo_conso[df_evo_conso['Code INSEE région']== 52])
    source8 = ColumnDataSource(df_evo_conso[df_evo_conso['Code INSEE région']== 53])
    source9 = ColumnDataSource(df_evo_conso[df_evo_conso['Code INSEE région']== 75])
    source10 = ColumnDataSource(df_evo_conso[df_evo_conso['Code INSEE région']== 76])
    source11= ColumnDataSource(df_evo_conso[df_evo_conso['Code INSEE région']== 84])
    source12 = ColumnDataSource(df_evo_conso[df_evo_conso['Code INSEE région']== 93])

    # List de tools
    TOOLS="crosshair,pan,wheel_zoom,box_zoom,reset"

    # Figure
    y_overlimit = 0.05 
    p = figure(plot_width = 700, plot_height = 400,     
            title = "Evolution de la Consommation d'Électricité par Région",                    
            x_axis_label = 'Date', x_axis_type="datetime",
            y_axis_label = 'Consommation Moyenne (MW)',
            toolbar_location="below",
            tools=TOOLS)  

    p.title.text_color = "darkblue"
    p.title.text_font = "times"
    p.title.text_font_size = "20px"
    p.title.align = 'center'

    # Courves
    p.line(x='Date', y = 'Consommation (MW)', color = '#3182bd', legend_label = 'Île-de-France', source = source1)   
    p.line(x='Date', y = 'Consommation (MW)', color = '#6baed6', legend_label = 'Centre-Val de Loire', source = source2)  
    p.line(x='Date', y = 'Consommation (MW)', color = '#9ecae1', legend_label = 'Bourgogne-Franche-Comté', source = source3)  
    p.line(x='Date', y = 'Consommation (MW)', color = '#c6dbef', legend_label = 'Normandie', source = source4)  
    p.line(x='Date', y = 'Consommation (MW)', color = '#e6550d', legend_label = 'Hauts-de-France', source = source5)  
    p.line(x='Date', y = 'Consommation (MW)', color = '#fd8d3c', legend_label = 'Grand Est', source = source6)  
    p.line(x='Date', y = 'Consommation (MW)', color = '#fdae6b', legend_label = 'Pays de la Loire', source = source7)  
    p.line(x='Date', y = 'Consommation (MW)', color = '#fdd0a2', legend_label = 'Bretagne', source = source8)  
    p.line(x='Date', y = 'Consommation (MW)', color = '#31a354', legend_label = 'Nouvelle-Aquitaine', source = source9)  
    p.line(x='Date', y = 'Consommation (MW)', color = '#74c476', legend_label = 'Occitanie', source = source10)  
    p.line(x='Date', y = 'Consommation (MW)', color = '#a1d99b', legend_label = 'Auvergne-Rhône-Alpes', source = source11)  
    p.line(x='Date', y = 'Consommation (MW)', color = '#c7e9c0', legend_label = "Provence-Alpes-Côte d'Azu", source = source12)  

    # Paramettres axis
    p.xaxis.major_label_orientation = pi/4
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    p.xaxis.ticker.desired_num_ticks = 10

    # Activation de l'interaction avec la légende
    p.legend.location = (0,-50)
    p.legend.click_policy = 'hide'

    # Style hover
    p.add_tools(HoverTool(
        tooltips=[('Date', '@Date{%Y-%m-%d}'),
            ('Consommation (MW)', '@{Consommation (MW)}{0.00}')
            ],
        formatters={'@Date': 'datetime'}
    ))

    st.bokeh_chart(p, use_container_width=True)


# Case à cocher 2
if st.checkbox("Voir la tendance de la Consommation d'Électricité ?"): 

    # Source de données pour les graphiaques
    source1 = ColumnDataSource(df_evo_conso_sans[df_evo_conso_sans['Code INSEE région']== 11])
    source2 = ColumnDataSource(df_evo_conso_sans[df_evo_conso_sans['Code INSEE région']== 24])
    source3 = ColumnDataSource(df_evo_conso_sans[df_evo_conso_sans['Code INSEE région']== 27])
    source4 = ColumnDataSource(df_evo_conso_sans[df_evo_conso_sans['Code INSEE région']== 28])
    source5 = ColumnDataSource(df_evo_conso_sans[df_evo_conso_sans['Code INSEE région']== 32])
    source6 = ColumnDataSource(df_evo_conso_sans[df_evo_conso_sans['Code INSEE région']== 44])
    source7 = ColumnDataSource(df_evo_conso_sans[df_evo_conso_sans['Code INSEE région']== 52])
    source8 = ColumnDataSource(df_evo_conso_sans[df_evo_conso_sans['Code INSEE région']== 53])
    source9 = ColumnDataSource(df_evo_conso_sans[df_evo_conso_sans['Code INSEE région']== 75])
    source10 = ColumnDataSource(df_evo_conso_sans[df_evo_conso_sans['Code INSEE région']== 76])
    source11= ColumnDataSource(df_evo_conso_sans[df_evo_conso_sans['Code INSEE région']== 84])
    source12 = ColumnDataSource(df_evo_conso_sans[df_evo_conso_sans['Code INSEE région']== 93])

    # List de tools
    TOOLS="crosshair,pan,wheel_zoom,box_zoom,reset"

    # Figure
    y_overlimit = 0.05 
    p = figure(plot_width = 800, plot_height = 600,     
            title = "Tendance de la Consommation d'Électricité par Région",                    
            x_axis_label = 'Date', x_axis_type="datetime",
            y_axis_label = 'Consommation Moyenne (MW)',
            toolbar_location="below",
            tools=TOOLS)  

    p.title.text_color = "darkblue"
    p.title.text_font = "times"
    p.title.text_font_size = "20px"
    p.title.align = 'center'

    # Courves
    p.line(x='Date', y = 'Consommation (MW)', color = '#3182bd', legend_label = 'Île-de-France', source = source1)   
    p.line(x='Date', y = 'Consommation (MW)', color = '#6baed6', legend_label = 'Centre-Val de Loire', source = source2)  
    p.line(x='Date', y = 'Consommation (MW)', color = '#9ecae1', legend_label = 'Bourgogne-Franche-Comté', source = source3)  
    p.line(x='Date', y = 'Consommation (MW)', color = '#c6dbef', legend_label = 'Normandie', source = source4)  
    p.line(x='Date', y = 'Consommation (MW)', color = '#e6550d', legend_label = 'Hauts-de-France', source = source5)  
    p.line(x='Date', y = 'Consommation (MW)', color = '#fd8d3c', legend_label = 'Grand Est', source = source6)  
    p.line(x='Date', y = 'Consommation (MW)', color = '#fdae6b', legend_label = 'Pays de la Loire', source = source7)  
    p.line(x='Date', y = 'Consommation (MW)', color = '#fdd0a2', legend_label = 'Bretagne', source = source8)  
    p.line(x='Date', y = 'Consommation (MW)', color = '#31a354', legend_label = 'Nouvelle-Aquitaine', source = source9)  
    p.line(x='Date', y = 'Consommation (MW)', color = '#74c476', legend_label = 'Occitanie', source = source10)  
    p.line(x='Date', y = 'Consommation (MW)', color = '#a1d99b', legend_label = 'Auvergne-Rhône-Alpes', source = source11)  
    p.line(x='Date', y = 'Consommation (MW)', color = '#c7e9c0', legend_label = "Provence-Alpes-Côte d'Azu", source = source12)  

    # Axis
    p.xaxis.major_label_orientation = pi/4
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    p.xaxis.ticker.desired_num_ticks = 10

    # Citation
    citation = Label(x=400, y=110, x_units='screen', y_units='screen',
                    text="Sans fluctuations saisonniers", render_mode='css')

    # Activation de l'interaction avec la légende
    p.legend.location = "top_left"
    p.legend.click_policy = 'hide'
    p.add_layout(citation)

    # Style hover
    p.add_tools(HoverTool(
        tooltips=[('Date', '@Date{%Y-%m-%d}'),
            ('Consommation (MW)', '@{Consommation (MW)}{0.00}')
            ],
        formatters={'@Date': 'datetime'}
    ))

    st.bokeh_chart(p, use_container_width=True)

# Case à cocher 3
if st.checkbox("Voir la Consommation / Production d'Électricité par Region ?"): 

    # Source de données
    source_data = ColumnDataSource(df_group)
    source_data2 = ColumnDataSource(df_group_somme)
    Type_cmap = factor_cmap('Région', palette=df_group['color'].unique(), factors=df_group['Région'].unique())

    # List de tools
    TOOLS="crosshair,pan,wheel_zoom,box_zoom,reset"

    # Figure 1
    y_overlimit = 0.05 
    p1 = figure(plot_width = 800, plot_height = 750,     
            title = "Consommation Moyenne d'Électricité par Région / Mois",                    
            x_axis_label = 'Région',
            y_axis_label = 'Consommation Moyenne (MW)',
            toolbar_location="below",
            x_range=df_group['Région'],
            tools=TOOLS)  
    p1.vbar(x='Région', top='Consommation (MW)', width=0.8, source=source_data,line_color=Type_cmap, fill_color=Type_cmap,
    legend_group='Région', hover_line_color="black")

    p1.title.text_color = "darkblue"
    p1.title.text_font = "times"
    p1.title.text_font_size = "20px"
    p1.title.align = 'center'

    p1.xaxis.major_label_orientation = pi/4
    p1.xgrid.grid_line_color = None
    p1.ygrid.grid_line_color = None
    p1.legend.location = "top_left"
    p1.x_range = FactorRange(factors=df_group['Région'])

    p1.add_tools(HoverTool(tooltips=[('Consommation (MW)', '@{Consommation (MW)}{0.00}')]))
    p1.legend.click_policy = 'hide'

    # Figure 2
    p2 = figure(plot_width = 800, plot_height = 750,     
            title = "Production Moyenne d'Électricité par Région / Mois",                    
            x_axis_label = 'Région',
            y_axis_label = 'Production Moyenne (MW)',
            toolbar_location="below",
            x_range=df_group['Région'],
            tools=TOOLS)  
    p2.vbar(x='Région', top='Total', width=0.8, source=source_data2,line_color=Type_cmap, fill_color=Type_cmap,
    legend_group='Région', hover_line_color="black")

    p2.title.text_color = "darkblue"
    p2.title.text_font = "times"
    p2.title.text_font_size = "20px"
    p2.title.align = 'center'

    p2.xaxis.major_label_orientation = pi/4
    p2.xgrid.grid_line_color = None
    p2.ygrid.grid_line_color = None
    p2.legend.location = "top_left"
    p2.x_range = FactorRange(factors=df_group_somme['Région'])

    p2.add_tools(HoverTool(tooltips=[('Production moyenne', '@Total{0.00}')]))
    p2.legend.click_policy = 'hide'

    # Tabs
    tab1 = Panel(child=p1, title="Consommation (MW)")
    tab2 = Panel(child=p2, title="Production")

    tabs = Tabs(tabs=[ tab1, tab2 ])

    st.bokeh_chart(tabs, use_container_width=True)


# Case à cocher 4
if st.checkbox("Voir l'évolution de la Production d'Électricité par nature ?"): 

    # Source Graphique 1
    data = df_group_date_prod.to_dict(orient='list')
    idx = df_group_date_prod['Annee'].tolist()
    source = ColumnDataSource(data=data)

    TOOLS="crosshair,pan,wheel_zoom,box_zoom,reset"

    # Figure 1
    p1 = figure(x_range=idx, y_range=(0, df_group_date_prod[['Consommation (MW)',
    'Thermique (MW)','Nucléaire (MW)','Eolien (MW)','Solaire (MW)','Hydraulique (MW)','Bioénergies (MW)']].values.max()), 
            plot_width = 900, plot_height = 600, title="Production d'Électricité Moyenne par Nature / Année",
            toolbar_location="below",
            tools=TOOLS,
            x_axis_label = 'Année',
            y_axis_label = 'Production Moyenne (MW)')

    # Graphique à Barres
    p1.vbar(x=dodge('Annee', -0.4, range=p1.x_range), top='Thermique (MW)', width=0.2, source=source,
        color="#F05223", legend_label='Thermique (MW)')
    p1.vbar(x=dodge('Annee', -0.2, range=p1.x_range), top='Nucléaire (MW)', width=0.2, source=source,
        color="#F6A91B", legend_label='Nucléaire (MW)')
    p1.vbar(x=dodge('Annee', 0, range=p1.x_range), top='Eolien (MW)', width=0.2, source=source,
        color="#A5CD39", legend_label='Eolien (MW)')
    p1.vbar(x=dodge('Annee', 0.2, range=p1.x_range), top='Solaire (MW)', width=0.2, source=source,
        color="#20B254", legend_label='Solaire (MW)')
    p1.vbar(x=dodge('Annee', 0.4, range=p1.x_range), top='Hydraulique (MW)', width=0.2, source=source,
        color="#00AAAE", legend_label='Hydraulique (MW)')
    p1.vbar(x=dodge('Annee', 0.6, range=p1.x_range), top='Bioénergies (MW)', width=0.2, source=source,
        color="#892889", legend_label='Bioénergies (MW)')

    # Axis Graphique 1
    p1.title.text_color = "darkblue"
    p1.title.text_font = "times"
    p1.title.text_font_size = "20px"
    p1.title.align = 'center'

    p1.x_range.range_padding = 0.2
    p1.xgrid.grid_line_color = None
    p1.axis.minor_tick_line_color = None
    p1.outline_line_color = None
    p1.legend.location = "top_left"
    p1.legend.orientation = "horizontal"

    p1.legend.click_policy = 'hide'

    # Style hover
    p1.add_tools(HoverTool(
        tooltips=[#('Date', '@Date{%Y-%m-%d}'),
            #('Consommation (MW)', '@{Consommation (MW)}{0.00}'),
            ('Thermique (MW)', '@{Thermique (MW)}{0.00}'),
            ('Nucléaire (MW)', '@{Nucléaire (MW)}{0.00}'),
            ('Eolien (MW)', '@{Eolien (MW)}{0.00}'),
            ('Solaire (MW)', '@{Solaire (MW)}{0.00}'),
            ('Hydraulique (MW)', '@{Hydraulique (MW)}{0.00}'),
            ('Bioénergies (MW)', '@{Bioénergies (MW)}{0.00}')
            ]
    ))
    
    # -----------------------
  
    # Figure 2
    p2 = figure(x_range=idx, y_range=(0, df_group_date_prod[['Consommation (MW)',
    'Thermique (MW)','Nucléaire (MW)','Eolien (MW)','Solaire (MW)','Hydraulique (MW)','Bioénergies (MW)']].values.max()), 
            plot_width = 900, plot_height = 600, title="Evolution de la Production d'Électricité par Nature / Année",
            toolbar_location="below",
            tools=TOOLS,
            x_axis_label = 'Année',
            y_axis_label = 'Production Moyenne (MW)')


    # Source Graphique 2
    data1 = df_group_date_prod[['Consommation (MW)','Annee']]
    data2 = df_group_date_prod[['Thermique (MW)','Annee']]
    data3 = df_group_date_prod[['Nucléaire (MW)','Annee']]
    data4 = df_group_date_prod[['Eolien (MW)','Annee']]
    data5 = df_group_date_prod[['Solaire (MW)','Annee']]
    data6 = df_group_date_prod[['Hydraulique (MW)','Annee']]
    data7 = df_group_date_prod[['Bioénergies (MW)','Annee']]

    source1 = ColumnDataSource(data=data1)
    source2 = ColumnDataSource(data=data2)
    source3 = ColumnDataSource(data=data3)
    source4 = ColumnDataSource(data=data4)
    source5 = ColumnDataSource(data=data5)
    source6 = ColumnDataSource(data=data6)
    source7 = ColumnDataSource(data=data7)

    # Graphique à lignes
    p2.line(x='Annee', y = 'Thermique (MW)', color = '#F05223', legend_label = 'Thermique (MW)', source = source2, line_width=2)   
    p2.line(x='Annee', y = 'Nucléaire (MW)', color = '#F6A91B', legend_label = 'Nucléaire (MW)', source = source3, line_width=2)   
    p2.line(x='Annee', y = 'Eolien (MW)', color = '#A5CD39', legend_label = 'Eolien (MW)', source = source4, line_width=2)   
    p2.line(x='Annee', y = 'Solaire (MW)', color = '#20B254', legend_label = 'Solaire (MW)', source = source5, line_width=2)   
    p2.line(x='Annee', y = 'Hydraulique (MW)', color = '#00AAAE', legend_label = 'Hydraulique (MW)', source = source6, line_width=2)   
    p2.line(x='Annee', y = 'Bioénergies (MW)', color = '#892889', legend_label = 'Bioénergies (MW)', source = source7, line_width=2)   

    # Axis Graphique 2
    p2.title.text_color = "darkblue"
    p2.title.text_font = "times"
    p2.title.text_font_size = "20px"
    p2.title.align = 'center'

    p2.x_range.range_padding = 0.2
    p2.xgrid.grid_line_color = None
    p2.axis.minor_tick_line_color = None
    p2.outline_line_color = None
    p2.legend.location = "top_left"
    p2.legend.orientation = "horizontal"
    p2.legend.click_policy = 'hide'

    # Tabs
    tab1 = Panel(child=p1, title="Production par Nature")
    tab2 = Panel(child=p2, title="Évolution production")
    tabs = Tabs(tabs=[ tab1, tab2 ])

    st.bokeh_chart(tabs, use_container_width=True)


st.text("")

##################
# Check Box Barre Lateral Option 1
##################

if st.sidebar.checkbox('Prédictions par Modèle'):
   option = st.sidebar.selectbox("Modèle à utiliser :", 
   ("Lasso","Ridge","ElasticCV","SGDRegressor","ARIMA","SARIMA","SARIMAX","SARIMAXLog"))
   st.header(f"Prédictions quotidiennes Ile de France, Modèle {option}")
   with st.spinner('Attends moi...'):
     time.sleep(2)
     st.success("C'est fait !!")
   # Graphieques individuelles
   if option == "Ridge":

        #Source
        source1 = ColumnDataSource(ridge_model_1)

        # List de tools
        TOOLS="crosshair,pan,wheel_zoom,box_zoom,reset"

        # Figure
        y_overlimit = 0.05 
        p = figure(plot_width = 900, plot_height = 550,     
                title = "Régression du Modèle Ridge",                    
                x_axis_label = 'Date', x_axis_type="datetime",
                y_axis_label = 'Consommation Moyenne',
                toolbar_location="below",
                tools=TOOLS)  

        p.title.text_color = "darkblue"
        p.title.text_font = "times"
        p.title.text_font_size = "20px"
        p.title.align = 'center'

        # Axis
        p.xaxis.major_label_orientation = pi/4
        p.xgrid.grid_line_color = None
        p.ygrid.grid_line_color = None
        p.xaxis.ticker.desired_num_ticks = 29

        #Ridge
        p.line(x='Date', y ='predits', color = "#EC1557", legend_label = "Ridge", source = source1) 
        p.line(x='Date', y = 'Reel', color = "navy", legend_label = "Valeurs réellees", source = source1)
    
        # Axis y, gauche
        p.y_range = Range1d(ridge_model_1.Reel.min() * (1 - y_overlimit), ridge_model_1.predits.max() * (1 + y_overlimit))

        # Axis y, droite
        y_column2_range = "T" + "_range"
        p.extra_y_ranges = {
            y_column2_range: Range1d(
                start=ridge_model_1['T'].min() * (1 - y_overlimit),
                end=ridge_model_1['T'].max() * (1 + y_overlimit),
            )
        }
        p.add_layout(LinearAxis(y_range_name=y_column2_range), "right")

        p.line( x='Date', y = 'T', color="grey", legend_label="T (C°)", y_range_name=y_column2_range, source = source1)
        
        # Activation de l'interaction avec la légende
        p.legend.location = "top_left"
        p.legend.click_policy = 'hide'

        # Style hover
        p.add_tools(HoverTool(
            tooltips=[('Date', '@Date{%Y-%m-%d}'),
                ('Prédiction', '@predits{0.00}'),
                ('Valeur réelle', '@Reel{0.00}'),
                ('C°', "@T{0.00}")],
            formatters={'@Date': 'datetime'}
        ))

        st.bokeh_chart(p, use_container_width=True);

   if option == "Lasso":
        #Source
        source2 = ColumnDataSource(lasso_model_1)

        # List de tools
        TOOLS="crosshair,pan,wheel_zoom,box_zoom,reset"

        # Figure
        y_overlimit = 0.05 
        p = figure(plot_width = 900, plot_height = 550,     
                title = "Régression du Modèle Lasso",                    
                x_axis_label = 'Date', x_axis_type="datetime",
                y_axis_label = 'Consommation Moyenne',
                toolbar_location="below",
                tools=TOOLS)  

        p.title.text_color = "darkblue"
        p.title.text_font = "times"
        p.title.text_font_size = "20px"
        p.title.align = 'center'

        # Axis
        p.xaxis.major_label_orientation = pi/4
        p.xgrid.grid_line_color = None
        p.ygrid.grid_line_color = None
        p.xaxis.ticker.desired_num_ticks = 29

        #Lasso 
        p.line(x='Date', y ='predits', color = "#892889",legend_label = "Lasso", source = source2) 
        p.line(x='Date', y = 'Reel', color = "navy", legend_label = "Valeurs réellees", source = source2)

        # Axis y, gauche
        p.y_range = Range1d(ridge_model_1.Reel.min() * (1 - y_overlimit), ridge_model_1.predits.max() * (1 + y_overlimit))

        # Axis y, droite
        y_column2_range = "T" + "_range"
        p.extra_y_ranges = {
            y_column2_range: Range1d(
                start=ridge_model_1['T'].min() * (1 - y_overlimit),
                end=ridge_model_1['T'].max() * (1 + y_overlimit),
            )
        }
        p.add_layout(LinearAxis(y_range_name=y_column2_range), "right")

        p.line( x='Date', y = 'T', color="grey", legend_label="T (C°)", y_range_name=y_column2_range, source = source2)
    
        # Activation de l'interaction avec la légende
        p.legend.location = "top_left"
        p.legend.click_policy = 'hide'

        # Style hover
        p.add_tools(HoverTool(
            tooltips=[('Date', '@Date{%Y-%m-%d}'),
                ('Prédiction', '@predits{0.00}'),
                ('Valeur réelle', '@Reel{0.00}'),
                ('C°', "@T{0.00}")],
            formatters={'@Date': 'datetime'}
        ))

        st.bokeh_chart(p, use_container_width=True);

   if option == "ElasticCV":

        #Source
        source3 = ColumnDataSource(EN_model)

        # List de tools
        TOOLS="crosshair,pan,wheel_zoom,box_zoom,reset"

        # Figure
        y_overlimit = 0.05 
        p = figure(plot_width = 900, plot_height = 550,     
                title = "Régression du modèle Elastic-Net",                    
                x_axis_label = 'Date', x_axis_type="datetime",
                y_axis_label = 'Consommation Moyenne',
                toolbar_location="below",
                tools=TOOLS)  

        p.title.text_color = "darkblue"
        p.title.text_font = "times"
        p.title.text_font_size = "20px"
        p.title.align = 'center'

        # Axis
        p.xaxis.major_label_orientation = pi/4
        p.xgrid.grid_line_color = None
        p.ygrid.grid_line_color = None
        p.xaxis.ticker.desired_num_ticks = 29

        
        #Elastic Net
        p.line(x='Date', y ='predits', color = "#F6A91B",legend_label = "Elastic", source = source3) 
        p.line(x='Date', y = 'Reel', color = "navy", legend_label = "Valeurs réellees", source = source3) 
    
        # Axis y, gauche
        p.y_range = Range1d(ridge_model_1.Reel.min() * (1 - y_overlimit), ridge_model_1.predits.max() * (1 + y_overlimit))

        # Axis y, droite
        y_column2_range = "T" + "_range"
        p.extra_y_ranges = {
            y_column2_range: Range1d(
                start=ridge_model_1['T'].min() * (1 - y_overlimit),
                end=ridge_model_1['T'].max() * (1 + y_overlimit),
            )
        }
        p.add_layout(LinearAxis(y_range_name=y_column2_range), "right")

        p.line( x='Date', y = 'T', color="grey", legend_label="T (C°)", y_range_name=y_column2_range, source = source3)

        # Activation de l'interaction avec la légende
        p.legend.location = "top_left"
        p.legend.click_policy = 'hide'

        # Style hover
        p.add_tools(HoverTool(
            tooltips=[('Date', '@Date{%Y-%m-%d}'),
                ('Prédiction', '@predits{0.00}'),
                ('Valeur réelle', '@Reel{0.00}'),
                ('C°', "@T{0.00}")],
            formatters={'@Date': 'datetime'}
        ))

        st.bokeh_chart(p, use_container_width=True);

   if option == "SGDRegressor":
        #Source
        source7 = ColumnDataSource(sgd_model)

        # List de tools
        TOOLS="crosshair,pan,wheel_zoom,box_zoom,reset"

        # Figure
        y_overlimit = 0.05 
        p = figure(plot_width = 900, plot_height = 550,     
                title = "Régression du modèle SGDR",                    
                x_axis_label = 'Date', x_axis_type="datetime",
                y_axis_label = 'Consommation Moyenne',
                toolbar_location="below",
                tools=TOOLS)  

        p.title.text_color = "darkblue"
        p.title.text_font = "times"
        p.title.text_font_size = "20px"
        p.title.align = 'center'

        # Axis
        p.xaxis.major_label_orientation = pi/4
        p.xgrid.grid_line_color = None
        p.ygrid.grid_line_color = None
        p.xaxis.ticker.desired_num_ticks = 29

        #SGD
        p.line(x='Date', y ='predits', color = "#892889",legend_label = "SGD", source = source7)
        p.line(x='Date', y = 'Reel', color = "navy", legend_label = "Valeurs réellees", source = source7) 
        
        # Axis y, gauche
        p.y_range = Range1d(ridge_model_1.Reel.min() * (1 - y_overlimit), ridge_model_1.predits.max() * (1 + y_overlimit))

        # Axis y, droite
        y_column2_range = "T" + "_range"
        p.extra_y_ranges = {
            y_column2_range: Range1d(
                start=ridge_model_1['T'].min() * (1 - y_overlimit),
                end=ridge_model_1['T'].max() * (1 + y_overlimit),
            )
        }
        p.add_layout(LinearAxis(y_range_name=y_column2_range), "right")

        p.line( x='Date', y = 'T', color="grey", legend_label="T (C°)", y_range_name=y_column2_range, source = source7)
    
        # Activation de l'interaction avec la légende
        p.legend.location = "top_left"
        p.legend.click_policy = 'hide'

        # Style hover
        p.add_tools(HoverTool(
            tooltips=[('Date', '@Date{%Y-%m-%d}'),
                ('Prédiction', '@predits{0.00}'),
                ('Valeur réelle', '@Reel{0.00}'),
                ('C°', "@T{0.00}")],
            formatters={'@Date': 'datetime'}
        ))

        st.bokeh_chart(p, use_container_width=True);

   if option == "ARIMA":
        #Source
        source4 = ColumnDataSource(model_arima_df)

        # List de tools
        TOOLS="crosshair,pan,wheel_zoom,box_zoom,reset"

        # Figure
        y_overlimit = 0.05 
        p = figure(plot_width = 900, plot_height = 550,     
                title = "Modèle de séries Temporelles ARIMA[2,1,3]",                    
                x_axis_label = 'Date', x_axis_type="datetime",
                y_axis_label = 'Consommation Moyenne',
                toolbar_location="below",
                tools=TOOLS)  

        p.title.text_color = "darkblue"
        p.title.text_font = "times"
        p.title.text_font_size = "20px"
        p.title.align = 'center'

        # Axis
        p.xaxis.major_label_orientation = pi/4
        p.xgrid.grid_line_color = None
        p.ygrid.grid_line_color = None
        p.xaxis.ticker.desired_num_ticks = 29

        #Arima
        p.line(x='Date', y ='predits', color = "#A5CD39", legend_label = "ARIMA", source = source4)
        p.line(x='Date', y = 'Reel', color = "navy", legend_label = "Valeurs réellees", source = source4)  
        
        # Axis y, gauche
        p.y_range = Range1d(ridge_model_1.Reel.min() * (1 - y_overlimit), ridge_model_1.predits.max() * (1 + y_overlimit))

        # Axis y, droite
        #y_column2_range = "T" + "_range"
        #p.extra_y_ranges = {
        #    y_column2_range: Range1d(
        #        start=ridge_model_1['T'].min() * (1 - y_overlimit),
        #        end=ridge_model_1['T'].max() * (1 + y_overlimit),
        #    )
        #}
        #p.add_layout(LinearAxis(y_range_name=y_column2_range), "right")

        #p.line( x='Date', y = 'T', color="grey", legend_label="T (C°)", y_range_name=y_column2_range, source = source4)
    
        # Activation de l'interaction avec la légende
        p.legend.location = "top_left"
        p.legend.click_policy = 'hide'

        # Style hover
        p.add_tools(HoverTool(
            tooltips=[('Date', '@Date{%Y-%m-%d}'),
                ('Prédiction', '@predits{0.00}'),
                ('Valeur réelle', '@Reel{0.00}'),
                ('C°', "@T{0.00}")],
            formatters={'@Date': 'datetime'}
        ))

        st.bokeh_chart(p, use_container_width=True);

   if option == "SARIMA":
        #Source
        source5 = ColumnDataSource(model_sarima_df)

        # List de tools
        TOOLS="crosshair,pan,wheel_zoom,box_zoom,reset"

        # Figure
        y_overlimit = 0.05 
        p = figure(plot_width = 900, plot_height = 550,     
                title = "Modèle de Séries Temporelles SARIMA(3,1,0)(3,1,0)[7]",                    
                x_axis_label = 'Date', x_axis_type="datetime",
                y_axis_label = 'Consommation Moyenne',
                toolbar_location="below",
                tools=TOOLS)  

        p.title.text_color = "darkblue"
        p.title.text_font = "times"
        p.title.text_font_size = "20px"
        p.title.align = 'center'

        # Axis
        p.xaxis.major_label_orientation = pi/4
        p.xgrid.grid_line_color = None
        p.ygrid.grid_line_color = None
        p.xaxis.ticker.desired_num_ticks = 29

        #Sarima
        p.line(x='Date', y ='predits', color = "#20B254", legend_label = "SARIMA", source = source5)
        p.line(x='Date', y = 'Reel', color = "navy", legend_label = "Valeurs réellees", source = source5) 
    
        # Axis y, gauche
        p.y_range = Range1d(ridge_model_1.Reel.min() * (1 - y_overlimit), ridge_model_1.predits.max() * (1 + y_overlimit))

        # Axis y, droite
        #y_column2_range = "T" + "_range"
        #p.extra_y_ranges = {
        #    y_column2_range: Range1d(
        #        start=ridge_model_1['T'].min() * (1 - y_overlimit),
        #        end=ridge_model_1['T'].max() * (1 + y_overlimit),
        #    )
        #}
        #p.add_layout(LinearAxis(y_range_name=y_column2_range), "right")

        #p.line( x='Date', y = 'T', color="grey", legend_label="T (C°)", y_range_name=y_column2_range, source = source5)

        # Activation de l'interaction avec la légende
        p.legend.location = "top_left"
        p.legend.click_policy = 'hide'

        # Style hover
        p.add_tools(HoverTool(
            tooltips=[('Date', '@Date{%Y-%m-%d}'),
                ('Prédiction', '@predits{0.00}'),
                ('Valeur réelle', '@Reel{0.00}'),
                ('C°', "@T{0.00}")],
            formatters={'@Date': 'datetime'}
        ))

        st.bokeh_chart(p, use_container_width=True);

   if option == "SARIMAXLog":
        #Source
        source8 = ColumnDataSource(model_sarimaxlog_df)

        # List de tools
        TOOLS="crosshair,pan,wheel_zoom,box_zoom,reset"

        # Figure
        y_overlimit = 0.05 
        p = figure(plot_width = 900, plot_height = 550,     
                title = "Modèle de séries temporelles SARIMAX(3,1,0)(5,1,1)[7]",                    
                x_axis_label = 'Date', x_axis_type="datetime",
                y_axis_label = 'Consommation Moyenne',
                toolbar_location="below",
                tools=TOOLS)  

        p.title.text_color = "darkblue"
        p.title.text_font = "times"
        p.title.text_font_size = "20px"
        p.title.align = 'center'

        # Axis
        p.xaxis.major_label_orientation = pi/4
        p.xgrid.grid_line_color = None
        p.ygrid.grid_line_color = None
        p.xaxis.ticker.desired_num_ticks = 29

        #Sarimax
        p.line(x='Date', y ='predits', color = "orange", legend_label = "SARIMAXLog", source = source8)
        p.line(x='Date', y = 'Reel', color = "navy", legend_label = "Valeurs réellees", source = source8)  

        # Axis y, gauche
        p.y_range = Range1d(ridge_model_1.Reel.min() * (1 - y_overlimit), ridge_model_1.predits.max() * (1 + y_overlimit))

        # Axis y, droite
        y_column2_range = "T" + "_range"
        p.extra_y_ranges = {
            y_column2_range: Range1d(
                start=ridge_model_1['T'].min() * (1 - y_overlimit),
                end=ridge_model_1['T'].max() * (1 + y_overlimit),
            )
        }
        p.add_layout(LinearAxis(y_range_name=y_column2_range), "right")

        p.line( x='Date', y = 'T', color="grey", legend_label="T (C°)", y_range_name=y_column2_range, source = source8)

        # Activation de l'interaction avec la légende
        p.legend.location = "top_left"
        p.legend.click_policy = 'hide'

        # Style hover
        p.add_tools(HoverTool(
            tooltips=[('Date', '@Date{%Y-%m-%d}'),
                ('Prédiction', '@predits{0.00}'),
                ('Valeur réelle', '@Reel{0.00}'),
                ('C°', "@T{0.00}")],
            formatters={'@Date': 'datetime'}
        ))

        st.bokeh_chart(p, use_container_width=True);

   if option == "SARIMAX":
        #Source
        source6 = ColumnDataSource(model_sarimax_df)

        # List de tools
        TOOLS="crosshair,pan,wheel_zoom,box_zoom,reset"

        # Figure
        y_overlimit = 0.05 
        p = figure(plot_width = 900, plot_height = 550,     
                title = "Modèle de séries temporelles SARIMAX(3,1,2)(3,1,0)[7]",                    
                x_axis_label = 'Date', x_axis_type="datetime",
                y_axis_label = 'Consommation Moyenne',
                toolbar_location="below",
                tools=TOOLS)  

        p.title.text_color = "darkblue"
        p.title.text_font = "times"
        p.title.text_font_size = "20px"
        p.title.align = 'center'

        # Axis
        p.xaxis.major_label_orientation = pi/4
        p.xgrid.grid_line_color = None
        p.ygrid.grid_line_color = None
        p.xaxis.ticker.desired_num_ticks = 29

        #Sarimax
        p.line(x='Date', y ='predits', color = "#00AAAE", legend_label = "SARIMAX", source = source6)
        p.line(x='Date', y = 'Reel', color = "navy", legend_label = "Valeurs réellees", source = source6)  

        # Axis y, gauche
        p.y_range = Range1d(ridge_model_1.Reel.min() * (1 - y_overlimit), ridge_model_1.predits.max() * (1 + y_overlimit))

        # Axis y, droite
        y_column2_range = "T" + "_range"
        p.extra_y_ranges = {
            y_column2_range: Range1d(
                start=ridge_model_1['T'].min() * (1 - y_overlimit),
                end=ridge_model_1['T'].max() * (1 + y_overlimit),
            )
        }
        p.add_layout(LinearAxis(y_range_name=y_column2_range), "right")

        p.line( x='Date', y = 'T', color="grey", legend_label="T (C°)", y_range_name=y_column2_range, source = source6)

        # Activation de l'interaction avec la légende
        p.legend.location = "top_left"
        p.legend.click_policy = 'hide'

        # Style hover
        p.add_tools(HoverTool(
            tooltips=[('Date', '@Date{%Y-%m-%d}'),
                ('Prédiction', '@predits{0.00}'),
                ('Valeur réelle', '@Reel{0.00}'),
                ('C°', "@T{0.00}")],
            formatters={'@Date': 'datetime'}
        ))

        st.bokeh_chart(p, use_container_width=True);

st.write("")


##################
# Check Box Barre Lateral Option 2
##################

if st.sidebar.checkbox('Comparaison par groups de modèles'):
    option2 = st.sidebar.selectbox("Comparaison Modèles :", ("Modèles de Régression","Séries Temporelles"))
    st.header(option2)
    my_bar = st.progress(0)
    for percent_complete in range(100):
        time.sleep(0.02)
        my_bar.progress(percent_complete + 1)

    if option2 == "Modèles de Régression":
        #Source
        source1 = ColumnDataSource(ridge_model_1)
        source2 = ColumnDataSource(lasso_model_1)
        source3 = ColumnDataSource(EN_model)
        source7 = ColumnDataSource(sgd_model)
        source4 = ColumnDataSource(model_arima_df)
        source5 = ColumnDataSource(model_sarima_df)
        source6 = ColumnDataSource(model_sarimax_df)

        # List de tools
        TOOLS="crosshair,pan,wheel_zoom,box_zoom,reset"

        y_overlimit = 0.05 
        p = figure(plot_width = 900, plot_height = 550,     
                title = "Comparaison Ridge, Lasso, Elastic-Net, SGDR",                    
                x_axis_label = 'Date', x_axis_type="datetime",
                y_axis_label = 'Consommation Moyenne',
                toolbar_location="below",
                tools=TOOLS)  

        p.title.text_color = "darkblue"
        p.title.text_font = "times"
        p.title.text_font_size = "20px"
        p.title.align = 'center'

        p.xaxis.major_label_orientation = pi/4
        p.xgrid.grid_line_color = None
        p.ygrid.grid_line_color = None
        p.xaxis.ticker.desired_num_ticks = 29

        #Valeurs Réelles
        p.line(x='Date', y = 'Reel', color = "navy", legend_label = "Valeurs réellees", source = source6)   

        #Ridge
        p.line(x='Date', y ='predits', color = "#EC1557", legend_label = "Ridge", source = source1) 
    
        #Lasso 
        p.line(x='Date', y ='predits', color = "#892889",legend_label = "Lasso", source = source2) 

        #Elastic Net
        p.line(x='Date', y ='predits', color = "#F6A91B",legend_label = "Elastic", source = source3) 

        #SGD
        p.line(x='Date', y ='predits', color = "#892889",legend_label = "SGD", source = source7) 

        # axis y, gauche
        p.y_range = Range1d(ridge_model_1.Reel.min() * (1 - y_overlimit), ridge_model_1.predits.max() * (1 + y_overlimit))

        # Axis y, droite
        y_column2_range = "T" + "_range"
        p.extra_y_ranges = {
            y_column2_range: Range1d(
                start=ridge_model_1['T'].min() * (1 - y_overlimit),
                end=ridge_model_1['T'].max() * (1 + y_overlimit),
            )
        }
        p.add_layout(LinearAxis(y_range_name=y_column2_range), "right")

        p.line( x='Date', y = 'T', color="grey", legend_label="T (C°)", y_range_name=y_column2_range, source = source1)
        
        # Activation de l'interaction avec la légende
        p.legend.location = "top_left"
        p.legend.click_policy = 'hide'

        # Style hover
        p.add_tools(HoverTool(
            tooltips=[('Date', '@Date{%Y-%m-%d}'),
                ('Prédiction', '@predits{0.00}'),
                ('Valeur réelle', '@Reel{0.00}'),
                ('C°', "@T{0.00}")],
            formatters={'@Date': 'datetime'}
        ))

        st.bokeh_chart(p, use_container_width=True);

    if option2 == "Séries Temporelles":
        #Source
        source1 = ColumnDataSource(ridge_model_1)
        source2 = ColumnDataSource(lasso_model_1)
        source3 = ColumnDataSource(EN_model)
        source7 = ColumnDataSource(sgd_model)
        source4 = ColumnDataSource(model_arima_df)
        source5 = ColumnDataSource(model_sarima_df)
        source6 = ColumnDataSource(model_sarimax_df)

        # List de tools
        TOOLS="crosshair,pan,wheel_zoom,box_zoom,reset"

        y_overlimit = 0.05 
        p = figure(plot_width = 900, plot_height = 550,     
                title = "Comparaison ARIMA, SARIMA, SARIMAX",                    
                x_axis_label = 'Date', x_axis_type="datetime",
                y_axis_label = 'Consommation Moyenne',
                toolbar_location="below",
                tools=TOOLS)  

        p.title.text_color = "darkblue"
        p.title.text_font = "times"
        p.title.text_font_size = "20px"
        p.title.align = 'center'

        p.xaxis.major_label_orientation = pi/4
        p.xgrid.grid_line_color = None
        p.ygrid.grid_line_color = None
        p.xaxis.ticker.desired_num_ticks = 29

        #Valeurs Réelles
        p.line(x='Date', y = 'Reel', color = "navy", legend_label = "Valeurs réellees", source = source6)   

        #Arima
        p.line(x='Date', y ='predits', color = "#A5CD39", legend_label = "ARIMA", source = source4) 

        #Sarima
        p.line(x='Date', y ='predits', color = "#20B254", legend_label = "SARIMA", source = source5) 

        #Sarimax
        p.line(x='Date', y ='predits', color = "#00AAAE", legend_label = "SARIMAX", source = source6) 

        # axis y, gauche
        p.y_range = Range1d(ridge_model_1.Reel.min() * (1 - y_overlimit), ridge_model_1.predits.max() * (1 + y_overlimit))

        # Axis y, droite
        y_column2_range = "T" + "_range"
        p.extra_y_ranges = {
            y_column2_range: Range1d(
                start=ridge_model_1['T'].min() * (1 - y_overlimit),
                end=ridge_model_1['T'].max() * (1 + y_overlimit),
            )
        }
        p.add_layout(LinearAxis(y_range_name=y_column2_range), "right")

        p.line( x='Date', y = 'T', color="grey", legend_label="T (C°)", y_range_name=y_column2_range, source = source1)
        
        # Activation de l'interaction avec la légende
        p.legend.location = "top_left"
        p.legend.click_policy = 'hide'

        # Style hover
        p.add_tools(HoverTool(
            tooltips=[('Date', '@Date{%Y-%m-%d}'),
                ('Prédiction', '@predits{0.00}'),
                ('Valeur réelle', '@Reel{0.00}'),
                ('C°', "@T{0.00}")],
            formatters={'@Date': 'datetime'}
        ))

        st.bokeh_chart(p, use_container_width=True)
        
        st.markdown("""
        Nous avons utilisé l'outil d'evaluation "Critére d'Information Akaike - AIC", 
        afin d'évaluer la bonne adéquation du modèle pour les predictions et comparer aussi plusieurs modèles 
        (plusieurs paramètres (p)(q)(P)(Q)).

        Rappel :
        * Un modèle qui fait des meilleurs prévisions reçoit un score AIC inférieur
        * AIC privilege les modèles simples, donc moins de parametres

        #### Diagnostic du modèle
        - Prob(Q) est la valeur de p associée à l'hypothèse nulle selon laquelle les résidus n'ont pas de structure de corrélation
        - Prob(JB) est la valeur de p associée à l'hypothèse nulle selon laquelle les résidus suivent une distribution normale

        Si une des ces valeurs est inférieur à 0.05 nous rejetons l'hypothèse
        * p valeu > 0.05 : H0 n'est pas rejetée. 
        * p valeu ≤ 0.05 : H0 est rejetée

        Sur l'ensemble, nous ne rejetons pas H0, cela signifie que nos résidus n'ont pas de structure de corrélation 
        Par contre, nous rejetons H0 pour Prob(JB), donc les résidus ne suivent pas une distribution normale
        """);

st.write("")

##################
# Check Box Barre Lateral Option 3
##################

if st.sidebar.checkbox('Scores'):
    option3 = st.sidebar.selectbox("Analyses des Scores :", ("MAPE","MSE", "RMSE"))
    if option3 == "MAPE":
        st.subheader("Analyse Score MAPE")
        source_scores = ColumnDataSource(comparaison_scores)
        #ouput_file('source_scores.html')
        # List de tools
        TOOLS="pan,wheel_zoom,box_zoom,reset"

        # Instanciation de la figure
        p = figure(y_range = comparaison_scores.Modele,           
                plot_width = 900, plot_height = 400,
                title = 'Mean Absolute Prediction Error - MAPE',
                x_axis_label = "Probabilité Moyenne d'erreur %",
                y_axis_label = 'Modèle',
                toolbar_location="below",
                tools=TOOLS) 
    
        p.title.text_color = "darkblue"
        p.title.text_font = "times"
        p.title.text_font_size = "20px"
        p.title.align = 'center'

        p.xgrid.grid_line_color = None
        p.ygrid.grid_line_color = None

        # Instanciation d'un diagramme à barres horizontales
        p.hbar(y = 'Modele',  right = 'MAPE', height = 0.5, color='Colors', source=source_scores)                  

        labels = LabelSet(x='MAPE', y='Modele', text='MAPE',source=source_scores)

        # Iteraction legend
        p.add_layout(labels)

        st.bokeh_chart(p, use_container_width=False);

        st.write("MAPE, moyenne des écarts en valeur absolue par rapport aux valeurs observées");


    if option3 == "MSE":
        st.subheader("Analyse Score MSE")
        #Source
        source_scores = ColumnDataSource(comparaison_scores)
        # List de tools
        TOOLS="pan,wheel_zoom,box_zoom,reset"

        # Instanciation de la figure
        p = figure(y_range = comparaison_scores.Modele,           
                plot_width = 900, plot_height = 400,
                title = 'Mean Square Error - MSE',
                x_axis_label = "Carré moyen des erreurs",
                y_axis_label = 'Modèle',
                toolbar_location="below",
                tools=TOOLS) 
        
        p.title.text_color = "darkblue"
        p.title.text_font = "times"
        p.title.text_font_size = "20px"
        p.title.align = 'center'

        p.xgrid.grid_line_color = None
        p.ygrid.grid_line_color = None

        # Instanciation d'un diagramme à barres horizontales
        p.hbar(y = 'Modele',  right = 'MSE', height = 0.5, color='Colors', source=source_scores)

        p.add_layout(Arrow(end=OpenHead(line_color="darkblue", line_width=4),
                        x_start=400000, y_start=3.5, x_end=250000, y_end=3.5))
        citation = Label(x=190, y=135, x_units='screen', y_units='screen',
                        text="valeur MSE la plus bas", render_mode='css')
        p.add_layout(citation)
        st.bokeh_chart(p, use_container_width=False)
        
        st.write("""
        MSE, c’est la moyenne arithmétique des carrés des écarts entre prévisions du modèle et observations.
        Cette moyenne n'est autre que la VARIANCE RÉSIDUELLE que l'on cherche à minimiser.
        Si on compare les MSE, le meilleur est bien sûr celui qui présente la valeur MSE la plus faible, ici SGDRegressor
        """);

    if option3 == "RMSE":
        st.subheader("Analyse Score RMSE")
        source_scores = ColumnDataSource(comparaison_scores)

        # List de tools
        TOOLS="pan,wheel_zoom,box_zoom,reset"

        # Instanciation de la figure
        p = figure(y_range = comparaison_scores.Modele,           
                plot_width = 900, plot_height = 400,
                title = 'Root Mean Square Error - RMSE',
                x_axis_label = "Racine carrée de la moyenne des erreurs quadratiques",
                y_axis_label = 'Modèle',
                toolbar_location="below",
                tools=TOOLS) 

        p.title.text_color = "darkblue"
        p.title.text_font = "times"
        p.title.text_font_size = "20px"
        p.title.align = 'center'

        p.xgrid.grid_line_color = None
        p.ygrid.grid_line_color = None

        # Instanciation d'un diagramme à barres horizontales
        p.hbar(y = 'Modele',  right = 'RMSE', height = 0.5, color='Colors', source=source_scores)                  

        labels = LabelSet(x='RMSE', y='Modele', text='RMSE',source=source_scores)

        p.add_layout(Arrow(end=OpenHead(line_color="darkblue", line_width=4),
                        x_start=700, y_start=3.5, x_end=600, y_end=3.5))
        citation = Label(x=390, y=135, x_units='screen', y_units='screen',
                        text="valeur RMSE la plus bas", render_mode='css')

        # Iteraction legend
        p.add_layout(labels)
        p.add_layout(citation)

        st.bokeh_chart(p, use_container_width=False)
        st.write("""
        RMSE, c'est la racine carrée des différences entre les valeurs prédites et les valeurs observées. Ces écarts sont appelés résidus.
        Il s'agit d'une mesure de précision qui sert à comparer les erreurs de différents modèles prédictifs pour un ensemble de données particulier.
        Une valeur de RMSE plus petite indique une meilleur précision qu'une valeur de RMSE plus élevée.
        """);
