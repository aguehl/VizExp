
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
        
    for Col in ['METREPLANCHERDECL', 'METREPLANCHERCORR','PRIXMLKM', 'PRIXKM', 'PRIXML', 'PRIXPDSDECL', 'PROV TPRS']:
        dfDom[Col]=dfDom[Col].apply(lambda x: round(x, 2))
        
    dfInter=pd.read_parquet('dfExp_V2.1_mix_Inter.parquet')
    for Col in ['METREPLANCHERDECL', 'METREPLANCHERCORR','PRIXMLKM', 'PRIXKM', 'PRIXML', 'PRIXPDSDECL', 'PROV TPRS']:
        dfInter[Col]=dfInter[Col].apply(lambda x: round(x, 2))
    dfTransInter=pd.read_parquet('dfExp_V2.1_mix_TransInter.parquet')
    for Col in ['METREPLANCHERDECL', 'METREPLANCHERCORR','PRIXMLKM', 'PRIXKM', 'PRIXML', 'PRIXPDSDECL', 'PROV TPRS']:
        dfTransInter[Col]=dfTransInter[Col].apply(lambda x: round(x, 2))
    return dfDom, dfInter, dfTransInter

dfDom, dfInter, dfTrans =LoadParam()
#['NUMEXPEDITION', 'METIER', 'DTCHGTPREVUDU', 'CODEMODEPORT', 'MONTANTHTMB', 'NUMAGENCE', 'NOMAGENCE', 'TYPEFOUR', '
# PROV TPRS', 'MD(QT)', 'PAYSEXP', 'DEPTEXP', 'PAYSDEST', 'DEPTDEST', 'NBETIQ', 'NBPALEURDECL', 'POIDSDECLARE', 'NBKM', 
# 'METREPLANCHERDECL', 'ANNEEEXP', 'MOISEXP', 'METREPLANCHERCORR', 'PRIXMLKM', 'PRIXKM', 'PRIXML', 'PRIXPDSDECL', 
# 'METREPLANCHERDECLSTD', 'METREPLANCHERCORRSTD', 'PalEUR', 'PalEUR_IO', 'ADR_IO', 'TransType', 'Trajet', 'DISTANCE', 'FTL'
ListCol=['','NBKM','POIDSDECLARE', 'METREPLANCHERDECL', 'METREPLANCHERCORR', 'NBETIQ','DENSITE', 'PRIXKM', 'PRIXML', 'PRIXMLKM', 'PROV TPRS' ]
ListHue=['','PROV TPRS', 'NBETIQ',  'POIDSDECLARE', 'NBKM', 'METREPLANCHERDECL', 'METREPLANCHERCORR','DENSITE','ANNEEEXP', 'MOISEXP', 'PRIXMLKM', 'PRIXKM', 'PRIXML', 'PRIXPDSDECL', 
        'METREPLANCHERDECLSTD', 'METREPLANCHERCORRSTD', 'PalEUR', 'PalEUR_IO', 'ADR_IO', 'TransType', 'Trajet', 'DISTANCE', 'FTL']
dfDict={'Domestic':dfDom,"Inter" :dfInter,'TransInter' :dfTrans }
Type=['Domestic', 'Inter', 'TransInter']


st.header('Sélection')
col21, col22, col23=st.columns([1,1,1])
with col21: 
    Typ=st.selectbox('Type de Trajet',Type )
    Selected=st.selectbox('Limites', ListCol, index=0)
    st.header('')
    if Selected!='':
        st.header('')
    Selected2=st.selectbox('seconde Limites', ListCol, index=0)
    

df=dfDict[Typ]
Distances=['', 'XXS', 'XS', 'S', 'M', 'L', 'XL', 'XXL']
i=len(Distances)

with col22:
    Dist=st.selectbox('Distance', Distances)
    
    if Selected!='':
        if Selected in ['NBKM','POIDSDECLARE', 'NBETIQ']:
            Selmin=int(df[Selected].min())
            Selmax=int(df[Selected].max())
        else:
            Selmin=float(df[Selected].min())
            Selmax=float(df[Selected].max())
        st.write(Selmin)
        st.write(Selmax)
        Limmin=st.number_input('min', min_value=Selmin,max_value=Selmax)
        Limmax=st.number_input('max(df[Selected].min())', min_value=Selmin, max_value=Selmax)

    if Selected2!='':
        if Selected2 in ['NBKM','POIDSDECLARE','NBETIQ', 'DENSITE']:
            Selmin2=int(df[Selected2].min())
            Selmax2=int(df[Selected2].max())
        else:
            Selmin2=float(df[Selected2].min())
            Selmax2=float(df[Selected2].max())
        st.write(Selmin2)
        st.write(Selmax2)
        Limmin2=st.number_input('min', min_value=Selmin2,max_value=Selmax2)
        Limmax2=st.number_input('max', min_value=Selmin2, max_value=Selmax2)   
    

with col23:
    ftl=st.checkbox('FTL', value=True)
    ltl=st.checkbox('LTL', value=False)

if Dist!='':    
    df=df[df.DISTANCE==Dist]
    
if Selected!='':
    df=df[(df[Selected]>=Limmin)&(df[Selected]<=Limmax)]
if Selected2!='':
    df=df[(df[Selected2]>=Limmin2)&(df[Selected2]<=Limmax2)]
    
if ftl==True:
    if ltl==False:
        df=df[df.FTL=='FTL']
if ltl==True:
    if ftl==False:
        df=df[df.FTL=='LTL']
      

    
col31, col32, col33 =st.columns([1,1,1])
with col31:
    ColX=st.selectbox('Axe des x', ListCol)
    LogX=st.checkbox('Ehelle Log sur x', value=False)
with col32:
    ColY=st.selectbox('Axe des y', ListCol)
    LogY=st.checkbox('Ehelle Log sur y', value=False)
    
with col33:
    ColHue=st.selectbox('Mise en évidence', ListHue)

Height=st.slider('HAuteur du graph', min_value=400, max_value=1500, value=1000)

if (ColX!='')&(ColY!=''):
    if ColHue!='':
        fig = px.scatter(df, y=ColY, x=ColX, color=ColHue, color_continuous_scale="turbo",
                        log_x=LogX, log_y=LogY,
                        labels={
                        ColY:ColY,
                        ColX:ColX},
                        title=f'Correlation entre {ColX} et {ColY}',
                        height=Height)
    else:
        fig = px.scatter(df, y=ColY, x=ColX, 
                        log_x=LogX, log_y=LogY,
                        labels={
                        ColY:ColY,
                        ColX:ColX},
                        title=f'Correlation entre {ColX} et {ColY}',
                        height=Height)

    fig.update_layout(title_font_size=26)
    st.plotly_chart(fig, use_container_width=True)
st.write(df[['NUMEXPEDITION',  'NOMAGENCE',  'PROV TPRS',  'NBETIQ',  'POIDSDECLARE', 'NBKM', 
            'METREPLANCHERDECL', 'ANNEEEXP', 'MOISEXP', 'METREPLANCHERCORR', 'PRIXMLKM', 'PRIXKM', 'PRIXML', 'PRIXPDSDECL', 
            'DENSITE', 'PalEUR', 'PalEUR_IO', 'ADR_IO', 'TransType', 'Trajet', 'DISTANCE', 'FTL']])
