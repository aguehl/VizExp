
import pandas as pd
import numpy as np
import streamlit as st
from PIL import Image
import plotly.express as px


st.set_page_config(layout="wide")

col1,col2,col3 = st.columns([3,1,1])
with col1:
    im = Image.open("KN+EMP.jpg")
    st.image(im)
st.header('')
st.header('')


#uploaded_file = st.file_uploader("Choose a file")
#Chargeement des données
@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def LoadParam():
    dfDom=pd.DataFrame()
    for i in range (0,5):
        df=pd.read_parquet(f'dfExp_V2.1_mix_Domestic_{i}.parquet')
        dfDom=pd.concat([dfDom, df]).reset_index(drop=True)
    dfInter=pd.read_parquet('dfExp_V2.1_mix_Inter.parquet')
    dfTransInter=pd.read_parquet('dfExp_V2.1_mix_TransInter.parquet')
    return dfDom, dfInter, dfTransInter

dfDom, dfInter, dfTrans =LoadParam()
#['NUMEXPEDITION', 'METIER', 'DTCHGTPREVUDU', 'CODEMODEPORT', 'MONTANTHTMB', 'NUMAGENCE', 'NOMAGENCE', 'TYPEFOUR', '
# PROV TPRS', 'MD(QT)', 'PAYSEXP', 'DEPTEXP', 'PAYSDEST', 'DEPTDEST', 'NBETIQ', 'NBPALEURDECL', 'POIDSDECLARE', 'NBKM', 
# 'METREPLANCHERDECL', 'ANNEEEXP', 'MOISEXP', 'METREPLANCHERCORR', 'PRIXMLKM', 'PRIXKM', 'PRIXML', 'PRIXPDSDECL', 
# 'METREPLANCHERDECLSTD', 'METREPLANCHERCORRSTD', 'PalEUR', 'PalEUR_IO', 'ADR_IO', 'TransType', 'Trajet', 'DISTANCE
ListCol=['','NBKM','POIDSDECLARE', 'METREPLANCHERDECL', 'METREPLANCHERCORR', 'PRIXKKM', 'PRIXML', 'PRIXMLKM', 'PROV TPRS' ]

dfDict={'Domestic':dfDom,"Inter" :dfInter,'TransInter' :dfTrans }
Type=['Domestic', 'Inter', 'TransInter']
st.header('Sélection')
col21, col22, col23=st.columns([1,1,1])
with col21: 
    Typ=st.selectbox('Type de Trajet',Type )
    Selected=st.selectbox('Limites', ListCol, index=0)
    

df=dfDict[Typ]
Distances=list(df.DISTANCE.unique())
Distances.append('')
i=len(Distances)

with col22:
    Dist=st.selectbox('Distance', Distances, index=i-1)
    
    if Selected!='':
        if Selected in ['NBKM','POIDSDECLARE']:
            Selmin=int(df[Selected].min())
            Selmax=int(df[Selected].max())
        else:
            Selmin=float(df[Selected].min())
            Selmax=float(df[Selected].max())
        st.write(Selmin)
        st.write(Selmax)
        Limmax=0
        Limmin=st.slider('min', min_value=Selmin,max_value=Selmax)
        Limmax=st.slider('max(df[Selected].min())', min_value=Selmin, max_value=Selmax)

with col23:
    ftl=st.checkbox('FTL', value=True)
    ltl=st.checkbox('LTL', value=False)

if Dist!='':    
    df=df[df.DISTANCE==Dist]
if Selected!='':
    df=df[(df[Selected]>Limmin)&(df[Selected]<Limmax)]
if ftl==True:
    if ltl==False:
        df=df[df.FTL=='FTL']
if ltl==True:
    if ftl==False:
        df=df[df.FTL=='LTL']
      

    
col31, col32, col33 =st.columns([1,1,1])
with col31:
    ColX=st.selectbox('Axe des x', ListCol)
with col32:
    ColY=st.selectbox('Axe des y', ListCol)
with col33:
    ColHue=st.selectbox('Mise en évidence', ListCol)

if (ColX!='')&(ColY!=''):
    if ColHue!='':
        fig = px.scatter(df, y=ColY, x=ColX, color=ColHue, color_continuous_scale="turbo",
                        labels={
                        ColY:ColY,
                        ColX:ColX},
                        title=f'Correlation entre {ColX} et {ColY}')
    else:
        fig = px.scatter(df, y=ColY, x=ColX, 
                        labels={
                        ColY:ColY,
                        ColX:ColX},
                        title=f'Correlation entre {ColX} et {ColY}')

    fig.update_layout(title_font_size=26)
    st.plotly_chart(fig, use_container_width=True)

