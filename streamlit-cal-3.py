# -*- coding: utf-8 -*-
"""
Created on Thu Jul 21 11:09:11 2022

@author: furkanyunus.cevahir
"""

import pandas as pd
import streamlit as st
from gwosc import datasets
from gwosc.api import fetch_event_json
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import numpy as np
import io
import xlsxwriter
import os
import glob



def is_authenticated(password):
    return password == "tans" or password == "fyec" or password == "cevo"


def generate_login_block():
    block1 = st.empty()
    block2 = st.empty()

    return block1, block2


def clean_blocks(blocks):
    for block in blocks:
        block.empty()


def login(blocks):
    blocks[0].markdown("""
            <style>
                input {
                    -webkit-text-security: disc;
                }
            </style>
        """, unsafe_allow_html=True)

    return blocks[1].text_input('Password')


# def main():
#     st.header('Hello')
#     st.balloons()





df = pd.read_csv('./data/Havza-Althavza-il-ilçe Listesi.csv',encoding='ISO-8859-9')
list_of_csv=df["Havza-Althavza-il-ilçe Listesi"].tolist()
list_of_csv.insert(0, "Yazın")
# dfall = pd.read_csv('./data/ALL-Prcp-Tavg-csv.csv')



# def get_eventlist():
#     allevents = datasets.find_datasets(type='events')
#     eventset = set()
#     for ev in allevents:
#         name = fetch_event_json(ev)['events'][ev]['commonName']
#         if name[0:2] == 'GW':
#             eventset.add(name)
#     eventlist = list(eventset)
#     eventlist.sort()
#     return eventlist

#-- Set GCM
select_GCM = st.selectbox('GCM Seçin',
                                    ["GCM Seçin",'HadGEM', 'CNRM', "MPI"])

if select_GCM=="GCM Seçin":
    select_RCP = st.selectbox('Senaryo Seçin',
                                        ["Senaryo Seçin",'RCP45', 'RCP85'], disabled=True)
else:
    select_RCP = st.selectbox('Senaryo Seçin',
                                        ["Senaryo Seçin",'RCP45', 'RCP85'], disabled=False)  
    
if select_RCP=='Senaryo Seçin' or select_GCM=="GCM Seçin":
    select_para = st.selectbox('Parametre Seçin',
                                    ["Parametre Seçin",'Prcp', 'Tavg'], disabled=True)
else:
    select_para = st.selectbox('Parametre Seçin',
                                    ["Parametre Seçin",'Prcp', 'Tavg'], disabled=False)

if select_RCP=='Senaryo Seçin' or select_GCM=="GCM Seçin" or select_para=="Parametre Seçin":
    # st.title('Havza, Alt Havza, İl veya İlçe İsmini Yazın')
    bol_secimim = st.selectbox('Havza, Alt Havza, İl veya İlçe İsmini Yazın', 
                                       list_of_csv, disabled=True)
else:
    bol_secimim = st.selectbox('Havza, Alt Havza, İl veya İlçe İsmini Yazın', 
                                       list_of_csv, disabled=False)

def main():
    

    if st.button('10 yıllık ortalamaları göster'):
        # dfall = pd.read_csv('./data/ALL-Prcp-Tavg-csv.csv')
        
        folder="./data/chunked-allprcp/"
        # setting the path for joining multiple files
        files = os.path.join(folder, "*.csv")
        # list of merged files returned
        files = glob.glob(files)
        dfall=pd.concat(map(pd.read_csv, files), ignore_index=False)   
        
        if "(HAVZA)" in bol_secimim:
                text = bol_secimim
                # print(text.split(' (HAVZA)')[0])
                message = "GCM: " + str(select_GCM) + "\n" + "RCP Senaryosu: " + str(select_RCP)  + "\n" + 'Parametre: ' + str(select_para) + "\n" + "Havza: " + text.split(' (HAVZA)')[0]
                st.markdown(message, unsafe_allow_html=False)
                SEC_GCM=str(select_GCM)
                SEC_RCP=str(select_RCP)
                SEC_HAVZA=str(text.split(' (HAVZA)')[0])
                SEC_PARA= str(select_para)
                df_filtered = dfall[dfall['RCP'] == str(SEC_RCP)]
                df_filtered = df_filtered[df_filtered['HAVZA']== str(SEC_HAVZA)]
                df_filtered = df_filtered[df_filtered['GCM']== str(SEC_GCM)]
                df_filtered = df_filtered[df_filtered['Parameter']== str(SEC_PARA)]
                df_filtered.loc['mean'] = df_filtered.mean().round(1)
                df2=df_filtered.loc['mean']
                df2 = df2.filter(['HAVZA','RCP','GCM','Parameter','DATA_ref', 'DATA_2031_2040','DATA_2041_2050','DATA_2051_2060','DATA_2061_2070','DATA_2071_2080','DATA_2081_2090','DATA_2091_2100'])
                df2['HAVZA']=str(SEC_HAVZA); df2['RCP']=str(SEC_RCP); df2['GCM']=str(SEC_GCM); df2['Parameter']=str(SEC_PARA)
                df2 = pd.DataFrame(df2); df2=df2.T
                # print(df2)
                # print(str(SEC_GCM) + str(SEC_RCP)+ str(SEC_HAVZA) + str(SEC_PARA))
                
                  
                
                fig = Figure(figsize = (15, 6),dpi = 150)
                plt = fig.add_subplot(111)
                x_axis=['DATA_ref','DATA_2031_2040','DATA_2041_2050','DATA_2051_2060','DATA_2061_2070','DATA_2071_2080','DATA_2081_2090','DATA_2091_2100']
                x_axis_ref=['DATA_ref', 'DATA_2031_2040','DATA_2041_2050','DATA_2051_2060','DATA_2061_2070','DATA_2071_2080','DATA_2081_2090','DATA_2091_2100']
                y_axis=[df2['DATA_ref'],df2['DATA_2031_2040'],df2['DATA_2041_2050'],df2['DATA_2051_2060'],df2['DATA_2061_2070'],df2['DATA_2071_2080'],df2['DATA_2081_2090'],df2['DATA_2091_2100']]
                y_ref=[df2['DATA_ref'], df2['DATA_ref'],df2['DATA_ref'],df2['DATA_ref'],df2['DATA_ref'],df2['DATA_ref'],df2['DATA_ref']]
                plt.plot(x_axis,y_axis,'-bo', label='line with marker')     
                plt.hlines(xmin='DATA_ref', xmax='DATA_2091_2100',y=df2['DATA_ref'],linestyle='--' ,linewidth=1, color='r')
                # for i, v in enumerate(y_axis):
                #   plt.annotate(str(v), xy=(i,v), xytext=(-7,7), textcoords='offset points')
                if str(SEC_PARA)=='Tavg':
                  for i, v in enumerate(y_axis):
                    plt.text(i, v+0.1, "%.1f" %v, ha="center")
                if str(SEC_PARA)=='Prcp':
                  for i, v in enumerate(y_axis):
                    plt.text(i, v+2, "%.1f" %v,  ha="center")
                plt.set_xlabel('zaman periyodu')
                if str(SEC_PARA)=='Tavg':
                  plt.set_ylabel(str(SEC_PARA) + ' °C')
                if str(SEC_PARA)=='Prcp':
                  plt.set_ylabel(str(SEC_PARA) + ' mm/year')
                plt.set_title("GCM: " + str(select_GCM) + " " + "RCP Senaryosu: " + str(select_RCP)  + " " + 'Parametre: ' + str(select_para) + " " + "Havza: " + text.split(' (HAVZA)')[0])
                plt.grid(True)
                st.pyplot(fig)
                
                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                     # Write each dataframe to a different worksheet.
                     df2.to_excel(writer, sheet_name='Sheet1')
                 
                     # Close the Pandas Excel writer and output the Excel file to the buffer
                     writer.save()
                 
                     st.download_button(
                         label="Download Data as excel file",
                         data=buffer,
                         file_name="GCM: " + str(select_GCM) + " " + "RCP Senaryosu: " + str(select_RCP)  + " " + 'Parametre: ' + str(select_para) + " " + "Havza: " + text.split(' (HAVZA)')[0] + '.xlsx',
                         mime="application/vnd.ms-excel"
                     )
                
                
        if "(ALT HAVZA)" in bol_secimim:        
                text = bol_secimim
                # print(text.split(' (HAVZA)')[0])
                message = "GCM: " + str(select_GCM) + "\n" + "RCP Senaryosu: " + str(select_RCP)  + "\n" + 'Parametre: ' + str(select_para) + "\n" + "Alt Havza: " + text.split(' (ALT HAVZA)')[0]
                st.markdown(message, unsafe_allow_html=False)
                SEC_GCM=str(select_GCM)
                SEC_RCP=str(select_RCP)
                SEC_HAVZA=str(text.split(' (ALT HAVZA)')[0])
                SEC_PARA= str(select_para)
                df_filtered = dfall[dfall['RCP'] == str(SEC_RCP)]
                df_filtered = df_filtered[df_filtered['ALT HAVZA']== str(SEC_HAVZA)]
                df_filtered = df_filtered[df_filtered['GCM']== str(SEC_GCM)]
                df_filtered = df_filtered[df_filtered['Parameter']== str(SEC_PARA)]
                df_filtered.loc['mean'] = df_filtered.mean().round(1)
                df2=df_filtered.loc['mean']
                df2 = df2.filter(['ALT HAVZA','RCP','GCM','Parameter','DATA_ref', 'DATA_2031_2040','DATA_2041_2050','DATA_2051_2060','DATA_2061_2070','DATA_2071_2080','DATA_2081_2090','DATA_2091_2100'])
                df2['ALT HAVZA']=str(SEC_HAVZA); df2['RCP']=str(SEC_RCP); df2['GCM']=str(SEC_GCM); df2['Parameter']=str(SEC_PARA)
                df2 = pd.DataFrame(df2); df2=df2.T
                # print(df2)
                # print(str(SEC_GCM) + str(SEC_RCP)+ str(SEC_HAVZA) + str(SEC_PARA))
              
                
                fig = Figure(figsize = (15, 6),dpi = 150)
                plt = fig.add_subplot(111)
                x_axis=['DATA_ref','DATA_2031_2040','DATA_2041_2050','DATA_2051_2060','DATA_2061_2070','DATA_2071_2080','DATA_2081_2090','DATA_2091_2100']
                x_axis_ref=['DATA_ref', 'DATA_2031_2040','DATA_2041_2050','DATA_2051_2060','DATA_2061_2070','DATA_2071_2080','DATA_2081_2090','DATA_2091_2100']
                y_axis=[df2['DATA_ref'],df2['DATA_2031_2040'],df2['DATA_2041_2050'],df2['DATA_2051_2060'],df2['DATA_2061_2070'],df2['DATA_2071_2080'],df2['DATA_2081_2090'],df2['DATA_2091_2100']]
                y_ref=[df2['DATA_ref'], df2['DATA_ref'],df2['DATA_ref'],df2['DATA_ref'],df2['DATA_ref'],df2['DATA_ref'],df2['DATA_ref']]
                plt.plot(x_axis,y_axis,'-bo', label='line with marker')     
                plt.hlines(xmin='DATA_ref', xmax='DATA_2091_2100',y=df2['DATA_ref'],linestyle='--' ,linewidth=1, color='r')
                # for i, v in enumerate(y_axis):
                #   plt.annotate(str(v), xy=(i,v), xytext=(-7,7), textcoords='offset points')
                if str(SEC_PARA)=='Tavg':
                  for i, v in enumerate(y_axis):
                    plt.text(i, v+0.1, "%.1f" %v, ha="center")
                if str(SEC_PARA)=='Prcp':
                  for i, v in enumerate(y_axis):
                    plt.text(i, v+2, "%.1f" %v, ha="center")
                plt.set_xlabel('zaman periyodu')
                if str(SEC_PARA)=='Tavg':
                  plt.set_ylabel(str(SEC_PARA) + ' °C')
                if str(SEC_PARA)=='Prcp':
                  plt.set_ylabel(str(SEC_PARA) + ' mm/year')
                plt.set_title("GCM: " + str(select_GCM) + " " + "RCP Senaryosu: " + str(select_RCP)  + " " + 'Parametre: ' + str(select_para) + " " + "Alt Havza: " + text.split(' (ALT HAVZA)')[0])
                plt.grid(True)
                st.pyplot(fig)
                
                buffer = io.BytesIO()
                with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                     # Write each dataframe to a different worksheet.
                     df2.to_excel(writer, sheet_name='Sheet1')
                 
                     # Close the Pandas Excel writer and output the Excel file to the buffer
                     writer.save()
                 
                     st.download_button(
                         label="Download Data as excel file",
                         data=buffer,
                         file_name="GCM: " + str(select_GCM) + " " + "RCP Senaryosu: " + str(select_RCP)  + " " + 'Parametre: ' + str(select_para) + " " + "Alt Havza: " + text.split(' (ALT HAVZA)')[0] + '.xlsx',
                         mime="application/vnd.ms-excel"
                     )
        
        if "İLÇE" in bol_secimim:
               text = bol_secimim
               # print(text.split(' (HAVZA)')[0])
               message = "GCM: " + str(select_GCM) + "\n" + "RCP Senaryosu: " + str(select_RCP)  + "\n" + 'Parametre: ' + str(select_para) + "\n" + "İlçe: " + text.split(' (İLÇE)')[0]
               st.markdown(message, unsafe_allow_html=False)
               SEC_GCM=str(select_GCM)
               SEC_RCP=str(select_RCP)
               SEC_HAVZA=str(text.split(' (İLÇE)')[0])
               SEC_PARA= str(select_para)
               df_filtered = dfall[dfall['RCP'] == str(SEC_RCP)]
               df_filtered = df_filtered[df_filtered['İlçe']== str(SEC_HAVZA)]
               df_filtered = df_filtered[df_filtered['GCM']== str(SEC_GCM)]
               df_filtered = df_filtered[df_filtered['Parameter']== str(SEC_PARA)]
               df_filtered.loc['mean'] = df_filtered.mean().round(1)
               df2=df_filtered.loc['mean']
               df2 = df2.filter(['İlçe','RCP','GCM','Parameter','DATA_ref', 'DATA_2031_2040','DATA_2041_2050','DATA_2051_2060','DATA_2061_2070','DATA_2071_2080','DATA_2081_2090','DATA_2091_2100'])
               df2['İlçe']=str(SEC_HAVZA); df2['RCP']=str(SEC_RCP); df2['GCM']=str(SEC_GCM); df2['Parameter']=str(SEC_PARA)
               df2 = pd.DataFrame(df2); df2=df2.T
               # print(df2)
               # print(str(SEC_GCM) + str(SEC_RCP)+ str(SEC_HAVZA) + str(SEC_PARA))
             
               
               fig = Figure(figsize = (15, 6),dpi = 150)
               plt = fig.add_subplot(111)
               x_axis=['DATA_ref','DATA_2031_2040','DATA_2041_2050','DATA_2051_2060','DATA_2061_2070','DATA_2071_2080','DATA_2081_2090','DATA_2091_2100']
               x_axis_ref=['DATA_ref', 'DATA_2031_2040','DATA_2041_2050','DATA_2051_2060','DATA_2061_2070','DATA_2071_2080','DATA_2081_2090','DATA_2091_2100']
               y_axis=[df2['DATA_ref'],df2['DATA_2031_2040'],df2['DATA_2041_2050'],df2['DATA_2051_2060'],df2['DATA_2061_2070'],df2['DATA_2071_2080'],df2['DATA_2081_2090'],df2['DATA_2091_2100']]
               y_ref=[df2['DATA_ref'], df2['DATA_ref'],df2['DATA_ref'],df2['DATA_ref'],df2['DATA_ref'],df2['DATA_ref'],df2['DATA_ref']]
               plt.plot(x_axis,y_axis,'-bo', label='line with marker')     
               plt.hlines(xmin='DATA_ref', xmax='DATA_2091_2100',y=df2['DATA_ref'],linestyle='--' ,linewidth=1, color='r')
               # for i, v in enumerate(y_axis):
               #   plt.annotate(str(v), xy=(i,v), xytext=(-7,7), textcoords='offset points')
               if str(SEC_PARA)=='Tavg':
                 for i, v in enumerate(y_axis):
                   plt.text(i, v+0.1, "%.1f" %v, ha="center")
               if str(SEC_PARA)=='Prcp':
                 for i, v in enumerate(y_axis):
                   plt.text(i, v+2, "%.1f" %v, ha="center")
               plt.set_xlabel('zaman periyodu')
               if str(SEC_PARA)=='Tavg':
                 plt.set_ylabel(str(SEC_PARA) + ' °C')
               if str(SEC_PARA)=='Prcp':
                 plt.set_ylabel(str(SEC_PARA) + ' mm/year')
               plt.set_title("GCM: " + str(select_GCM) + " " + "RCP Senaryosu: " + str(select_RCP)  + " " + 'Parametre: ' + str(select_para) + " " + "İlçe: " + text.split(' (İLÇE)')[0])
               plt.grid(True)
               st.pyplot(fig)
    
               buffer = io.BytesIO()
               with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                    # Write each dataframe to a different worksheet.
                    df2.to_excel(writer, sheet_name='Sheet1')
                
                    # Close the Pandas Excel writer and output the Excel file to the buffer
                    writer.save()
                
                    st.download_button(
                        label="Download Data as excel file",
                        data=buffer,
                        file_name="GCM: " + str(select_GCM) + " " + "RCP Senaryosu: " + str(select_RCP)  + " " + 'Parametre: ' + str(select_para) + " " + "İlçe: " + text.split(' (İLÇE)')[0] + '.xlsx',
                        mime="application/vnd.ms-excel"
                    )
        
        
        
        
        if "ŞEHİR" in bol_secimim:
               text = bol_secimim
               # print(text.split(' (HAVZA)')[0])
               message = "GCM: " + str(select_GCM) + "\n" + "RCP Senaryosu: " + str(select_RCP)  + "\n" + 'Parametre: ' + str(select_para) + "\n" + "Şehir: " + text.split(' (ŞEHİR)')[0]
               st.markdown(message, unsafe_allow_html=False)
               SEC_GCM=str(select_GCM)
               SEC_RCP=str(select_RCP)
               SEC_HAVZA=str(text.split(' (ŞEHİR)')[0])
               SEC_PARA= str(select_para)
               df_filtered = dfall[dfall['RCP'] == str(SEC_RCP)]
               df_filtered = df_filtered[df_filtered['Şehir']== str(SEC_HAVZA)]
               df_filtered = df_filtered[df_filtered['GCM']== str(SEC_GCM)]
               df_filtered = df_filtered[df_filtered['Parameter']== str(SEC_PARA)]
               df_filtered.loc['mean'] = df_filtered.mean().round(1)
               df2=df_filtered.loc['mean']
               df2 = df2.filter(['Şehir','RCP','GCM','Parameter','DATA_ref', 'DATA_2031_2040','DATA_2041_2050','DATA_2051_2060','DATA_2061_2070','DATA_2071_2080','DATA_2081_2090','DATA_2091_2100'])
               df2['Şehir']=str(SEC_HAVZA); df2['RCP']=str(SEC_RCP); df2['GCM']=str(SEC_GCM); df2['Parameter']=str(SEC_PARA)
               df2 = pd.DataFrame(df2); df2=df2.T
               # print(df2)
               # print(str(SEC_GCM) + str(SEC_RCP)+ str(SEC_HAVZA) + str(SEC_PARA))
             
               
               fig = Figure(figsize = (15, 6),dpi = 150)
               plt = fig.add_subplot(111)
               x_axis=['DATA_ref','DATA_2031_2040','DATA_2041_2050','DATA_2051_2060','DATA_2061_2070','DATA_2071_2080','DATA_2081_2090','DATA_2091_2100']
               x_axis_ref=['DATA_ref', 'DATA_2031_2040','DATA_2041_2050','DATA_2051_2060','DATA_2061_2070','DATA_2071_2080','DATA_2081_2090','DATA_2091_2100']
               y_axis=[df2['DATA_ref'],df2['DATA_2031_2040'],df2['DATA_2041_2050'],df2['DATA_2051_2060'],df2['DATA_2061_2070'],df2['DATA_2071_2080'],df2['DATA_2081_2090'],df2['DATA_2091_2100']]
               y_ref=[df2['DATA_ref'], df2['DATA_ref'],df2['DATA_ref'],df2['DATA_ref'],df2['DATA_ref'],df2['DATA_ref'],df2['DATA_ref']]
               plt.plot(x_axis,y_axis,'-bo', label='line with marker')     
               plt.hlines(xmin='DATA_ref', xmax='DATA_2091_2100',y=df2['DATA_ref'],linestyle='--' ,linewidth=1, color='r')
               # for i, v in enumerate(y_axis):
               #   plt.annotate(str(v), xy=(i,v), xytext=(-7,7), textcoords='offset points')
               if str(SEC_PARA)=='Tavg':
                 for i, v in enumerate(y_axis):
                   plt.text(i, v+0.1, "%.1f" %v, ha="center")
               if str(SEC_PARA)=='Prcp':
                 for i, v in enumerate(y_axis):
                   plt.text(i, v+2, "%.1f" %v, ha="center")
               plt.set_xlabel('zaman periyodu')
               if str(SEC_PARA)=='Tavg':
                 plt.set_ylabel(str(SEC_PARA) + ' °C')
               if str(SEC_PARA)=='Prcp':
                 plt.set_ylabel(str(SEC_PARA) + ' mm/year')
               plt.set_title("GCM: " + str(select_GCM) + " " + "RCP Senaryosu: " + str(select_RCP)  + " " + 'Parametre: ' + str(select_para) + " " + "Şehir: " + text.split(' (ŞEHİR)')[0])
               plt.grid(True)
               st.pyplot(fig)
    
               buffer = io.BytesIO()
               with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
                    # Write each dataframe to a different worksheet.
                    df2.to_excel(writer, sheet_name='Sheet1')
                   
    
                    # Close the Pandas Excel writer and output the Excel file to the buffer
                    writer.save()
                    
    
                    st.download_button(
                        label="Download Data as excel file",
                        data=buffer,
                        file_name="GCM: " + str(select_GCM) + " " + "RCP Senaryosu: " + str(select_RCP)  + " " + 'Parametre: ' + str(select_para) + " " + "Şehir: " + text.split(' (ŞEHİR)')[0] + ".xlsx",
                        mime="application/vnd.ms-excel"
                    )
    
login_blocks = generate_login_block()
password = login(login_blocks)

if is_authenticated(password):
    clean_blocks(login_blocks)
    main()
elif password:
    st.info("Yanlış parola")

    

