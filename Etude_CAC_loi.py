# Import des packages 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import seaborn.objects as so
import pdtypes
from shapely.geometry import Point
import contextily as ctx
import re
import chardet
import streamlit as st
import os
os.environ['USE_PYGEOS'] = '0'
import geopandas as gpd
import warnings
warnings.filterwarnings("ignore")
sns.set_theme()
pd.options.display.max_columns = None
#pd.options.display.max_rows = None
sns.set(rc={'figure.figsize':(12,10)})


col1, col2 = st.columns(2, gap="large")
with col1:
    #st.header("A cat")
    st.image("logo_audc.png")
with col2:
    #st.header("A dog")
    st.image("Châlons_Agglo.png")
    

# Lecture du fichier CSV rpls2022_loi_epci200066876
df = pd.read_csv('rpls2022_loi_epci200066876.csv', sep= ";", decimal=',', 
                 dtype={"ANNEE_REMLOC" : "Int64", "MOIS_REMLOC" : "Int64", "MOIS_BAIL" : "Int64", "ANNEE_BAIL" : "Int64"}, encoding = "WINDOWS-1252")
df.duree_vacance = df.duree_vacance.round().astype("Int64")


#Traitement du fichier

df["LIBCOM"] = df["LIBCOM"].replace({
 'ChÃ¢lons-en-Champagne' : "Châlons-en-Champagne",
 'CondÃ©-sur-Marne' : "Condé-sur-Marne",
 'FagniÃ¨res' :  'Fagnières',
 'JÃ¢lons' : 'Jâlons',
 "L'Ã‰pine" : "L'Épine",
 'Saint-Martin-sur-le-PrÃ©' : "Saint-Martin-sur-le-Pré",
 'Saint-Ã‰tienne-au-Temple' : 'Saint-Étienne-au-Temple'})

df["LIBEPCI"] = df["LIBEPCI"].replace({'CA de ChÃ¢lons-en-Champagne' : "CA de Châlons-en-Champagne"})

df.NUMVOIE = df.NUMVOIE.str.strip(r"^0+")
df.NOMVOIE = df.NOMVOIE.str.upper()
df.TYPVOIE = df.TYPVOIE.str.upper()
df.INDREP = df.INDREP.str.upper()

df.NOMVOIE = df.NOMVOIE.str.replace("RUE U", "RUE DU")
df.NOMVOIE = df.NOMVOIE.str.replace("W. CHURCHILL", "WINSTON CHURCHILL")
df.NOMVOIE.replace(['AVENUE W. CHURCHLL','AVENUE W. CURCILL','AVENUE WINSTON CHURCHILL','AVNU WINSTON CHURCHILL'], 
                   "AVENUE WINSTON CHURCHILL", inplace = True)
df.NOMVOIE = df.NOMVOIE.str.replace("SAINTE MENÉHOULD","SAINTE MENEHOULD")
df.NOMVOIE = df.NOMVOIE.str.replace("MELINET","MÉLINET")
df.NOMVOIE = df.NOMVOIE.str.replace("PORTE MUREE", "PORTE MURÉE")
df.NOMVOIE = df.NOMVOIE.str.replace('SAINT- ANTOINE', 'SAINT-ANTOINE')
df.NOMVOIE = df.NOMVOIE.str.replace("SAINT ANTOINE", 'SAINT-ANTOINE')
df.NOMVOIE = df.NOMVOIE.str.replace("LECOMTE DE LISLE", 'LECONTE DE LISLE')
df.NOMVOIE.replace(["REVOLUTION DE 178",'REVOLUTION DE 179','REVOLUTION DE 189','REVOLUTION DE 789',
                    'REVOLUTION DE 89'], 'REVOLUTION DE 1789', inplace = True)

df.NOMVOIE.replace(["DE FAGNIERES"], "DE FAGNIÈRES", inplace = True)   
df.NOMVOIE.replace(['P MENDES FRANCE','P. MENDES FRANCE'],"PIERRE MENDES FRANCE", inplace = True)
df.NOMVOIE.replace(['JEAN J. ROUSSEAU','JEAN JACQUES ROUSSEAU', "J.J. ROUSSEAU"], "JEAN-JACQUES ROUSSEAU", inplace = True)
df.NOMVOIE.replace(['J. PREVERT','J. PRÉVERT', "JACQUES PREVERT"], "JACQUES PRÉVERT", inplace = True)
df.NOMVOIE.replace(['J.B. ARMONVILLE', "J.B. D'ARMONVILLE", "JB D'ARMONVILLE"],"JEAN-BAPTISTE ARMONVILLE", inplace = True)
df.NOMVOIE = df.NOMVOIE.str.replace("RU ", "RUE ")
df.NOMVOIE.replace("JEAN JAURES",'JEAN JAURÈS', inplace = True)
df.NOMVOIE.replace(["RUE JB 'ARMONVILLE"], "RUE JEAN-BAPTISTE ARMONVILLE", inplace = True)
df.NOMVOIE.replace(["EMILE SCHMITT"], "EMILE SCHMIT", inplace = True)
df.NOMVOIE.replace(["RUE MIL SCHMIT"], "RUE EMILE SCHMIT", inplace = True)
df.NOMVOIE.replace(["J.F. KENNEDY", "KENNEDY", "JONH F. KENNEDY", "JOHN F. KENNEDY"], "JOHN FITZGERALD KENNEDY", inplace = True)

df.NOMVOIE.replace(["AVENUE DU GÉNÉRAL DE GAU"], "AVENUE DU GÉNÉRAL CHARLES DE GAULLE", inplace = True)
df.NOMVOIE.replace('GAL DE GAULLE', "GÉNÉRAL CHARLES DE GAULLE", inplace = True)
df.NOMVOIE.replace('DU GÉNÉRAL DE GAULLE', "DU GÉNÉRAL CHARLES DE GAULLE", inplace = True)

df.NOMVOIE.replace('D. SIMONNOT', 'DANIEL SIMONNOT', inplace = True)
df.NOMVOIE.replace("DU 2 AOUT 144", 'DU 29 AOUT 1944', inplace = True)
df.NOMVOIE.replace(['AMITIE /LES PEUPLES','AMITIE E/LES PEUPLES', "DE L'AMITIE ENTRE LES PEUPL", "AMITIE ENTRE LES PEUPLES"],"DE L'AMITIÉ ENTRE LES PEUPLES", inplace = True)
df.NOMVOIE.replace( ['DU GAL FERY','DU GENERAL FERY',], "DU GÉNÉRAL FERY" , inplace = True)
df.NOMVOIE.replace( ['RUE DU GAL FRY',"RUE DU GAL FERY",], "RUE DU GÉNÉRAL FERY" , inplace = True)
df.NOMVOIE.replace('67 AV DE METZ', '67 AVENUE DE METZ', inplace = True)
df.NOMVOIE.replace('D AMSTERDAM\t', "D'AMSTERDAM", inplace = True)
df.NOMVOIE = df.NOMVOIE.str.replace("D'ORLEANS","D'ORLÉANS")
df.NOMVOIE.replace("DE SAINT MALO", "DE SAINT-MALO", inplace = True)
df.NOMVOIE.replace(["J-BAPTISTE DROUET",'J.B. DROUET'], "JEAN-BAPTISTE DROUET", inplace = True)
df.NOMVOIE.replace("BENARD REMY", "BERNARD REMY", inplace = True)
df.NOMVOIE.replace("DE L ABBE LAMBERT", "DE L'ABBE LAMBERT", inplace = True)
df.NOMVOIE.replace("DE L HOPITAL MILITAIRE", "DE L'HOPITAL MILITAIRE", inplace = True)
df.NOMVOIE.replace("DELACROIX DE CONTAUT", "CHARLES DELACROIX DE CONTAUT", inplace = True)
df.NOMVOIE.replace(['DU FBG SAINT JEAN','DU FBG ST JEAN'], "DU FAUBOURG SAINT JEAN", inplace = True)
df.NOMVOIE.replace("DU GL CHARLES DE-GAULL", "DU GÉNÉRAL CHARLES DE GAULLE" , inplace = True)
              
df['TYPVOIE'] = df['TYPVOIE'].replace(["","ALLEE", "ALLÈE"], "ALLÉE")
df['TYPVOIE'] = df['TYPVOIE'].replace(["BD", "BD.", "BLD","BLD.", "BLV","BOUVELARD","BLS"], "BOULEVARD")
df['TYPVOIE'] = df['TYPVOIE'].replace(["AV", "AV.", 'AVE.'], "AVENUE")
df['TYPVOIE'] = df['TYPVOIE'].replace(["AVE.DU"], "AVENUE DU")
df['TYPVOIE'] = df['TYPVOIE'].replace(["PL."], "PLACE")
df['TYPVOIE'] = df['TYPVOIE'].replace(["CH"], "RUE")
df['TYPVOIE'] = df['TYPVOIE'].replace(["FBG"], "FAUBOURG")
df['TYPVOIE'] = df['TYPVOIE'].replace(["IMP."], "IMPASSE")
df['TYPVOIE'] = df['TYPVOIE'].replace(["BAT"], "BATIMENT")

df["RSEXPRO"] = df["RSEXPRO"].str.replace("privÈ", "privé")

# Création d'une nouvelle colonne pour les types de QPV
QPV_OUEST = ["ALBERT SCHWEITZER", "BENJAMIN FRANKLIN", "DAVID BLONDEL", 
             "DE BRETAGNE","DE CANCALE",  "DE COURSEULLES SUR MER", "DE NORMANDIE", 
             "DE PARIS", "DE SAINT-MALO","DES AVEUGLES","D'ORLEANS","D'ORLÉANS", 
             "DU 372 ÈME R.A.L.V.F.", "DU LEGS MOREL","HENRI DUNANT", "JEAN JAURÈS", 
             "JULES LOBET", "LAFAYETTE", "LIEUTENANT LOYER","MAURICE COLIN", 
             "PIERRE SEMARD", "PIERRE SONGY", "TER RUE D'ALSACE"]

QPV_SUD = ['AVENUE DU GÉNÉRAL CHARLES DE GAULLE',"CHARLES DE GAULLE",'GÉNÉRAL CHARLES DE GAULLE',
           'BIR HAKEIM',"D'ALSACE", 'DU 29 AOUT 1944','DU GENERAL GIRAUD', 'DU GROUPE MELPOMENE',
           'DU LEGS MOREL', 'JOHN FITZGERALD KENNEDY', 'LOUIS LAFOREST','POINT BAGATELLE']

conditions = [
    (df["LIBCOM"] == "Châlons-en-Champagne") & (df["QPV"] == 1) & (df["NOMVOIE"].isin(QPV_OUEST)),
    (df["LIBCOM"] == "Châlons-en-Champagne") & (df["QPV"] == 1) & (df["NOMVOIE"].isin(QPV_SUD)),
    (df["LIBCOM"] == "Châlons-en-Champagne") & (df["QPV"] == 2)]

choix = ["QPV OUEST", "QPV SUD", "HORS QPV"]

df.loc[ : , "LIBQPV"]  = pd.Series(np.select(conditions, choix, default = np.nan)).replace({"nan" : np.nan})


# Fonction pour déplacer les colonnes
@st.cache 
def movecol(df, cols_to_move=[], ref_col='', place='After'):
    cols = df.columns.tolist()
    if place == 'After':
        seg1 = cols[:list(cols).index(ref_col) + 1]
        seg2 = cols_to_move
    if place == 'Before':
        seg1 = cols[:list(cols).index(ref_col)]
        seg2 = cols_to_move + [ref_col]
    seg1 = [i for i in seg1 if i not in seg2]
    seg3 = [i for i in cols if i not in seg1 + seg2]
    
    return(df[seg1 + seg2 + seg3])

df = movecol(df, 
             cols_to_move=['QPV','LIBQPV'], 
             ref_col='NOMVOIE',
             place='After')



#st.write(df)
#st.dataframe(df.head())


# Filtre des qpv
filtre_qpv = df[["LIBCOM","NOMVOIE", "LIBQPV"]].groupby(["NOMVOIE", "LIBQPV"], 
                                           dropna=True)[["NOMVOIE", "LIBQPV"]].value_counts().reset_index(name ="Nombre").sort_values(by ="LIBQPV")
filtre_qpv[filtre_qpv["LIBQPV"].isin(["QPV OUEST", "QPV SUD"])].sort_values(by = [ "LIBQPV", "NOMVOIE"])

#st.write(filtre_qpv)

with st.sidebar:
    st_ms = st.multiselect("Lignes", filtre_qpv.LIBQPV.unique().tolist())
    
#st.bar_chart(filtre_qpv[["LIBQPV"]])
#st.bar_chart(filtre_qpv[["LIBQPV", "Nombre"]])
#fig = pd.DataFrame(df.groupby("LIBQPV", dropna = True)[["LIBQPV"]].value_counts().reset_index(name= "Total").set_index("LIBQPV")).plot(kind='bar', rot= 0)
#st.bar_chart(data=filtre_qpv, x="LIBQPV", y="Nombre", width=0, height=0, use_container_width=True)

import plotly.express as px
fig = px.bar(filtre_qpv, x="LIBQPV", y="Nombre", labels=dict(LIBQPV="Lieu QPV"))

col1, col2 = st.columns(2, gap="large")
with col1:
    #st.header("A cat")
    st.write(filtre_qpv)
with col2:
    #st.header("A dog")
    st.plotly_chart(fig, theme=None, use_container_width=True)




# Calcul du nombre de HLM par commune du CAC
table= pd.crosstab(df['LIBCOM'], df['QPV'], margins=True, margins_name='total HLM')

table.drop("total HLM", axis = 0, inplace = True)
table.index.names = ['Commune']
table = table.rename_axis(None, axis=1)
table.rename(columns = {1: "QPV", 	2 :"Hors_QPV"}, inplace=True)
table.sort_values(by=['QPV'], ascending=False, inplace=True)
#table.loc["total_ligne"] = table.sum(axis = 0) 
#table['Pourcentage'] = table["total HLM"].transform(lambda x: "{:.2f}%".format(x/table['total HLM'].sum()*100))
table['Pourcentage'] = table["total HLM"].transform(lambda x: round(x/table['total HLM'].sum()*100,2))
table.sort_values(by = "Pourcentage", ascending=False, inplace =True)


fig2 = px.bar(table, x = "Pourcentage", y = table.index)
st.plotly_chart(fig2, theme=None, use_container_width=True)