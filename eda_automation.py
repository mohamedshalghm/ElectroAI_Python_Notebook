import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings
from pandas.api.types import is_numeric_dtype,is_string_dtype,is_object_dtype
import io


# Start Page Setting
warnings.filterwarnings('ignore')
st.set_page_config(page_title='Interactive Dashboard',page_icon=':bar_chart',layout='wide')
st.title(':bar_chart: Simple Interactive Generic Dashboard ')
st.markdown('<style>div.block-container{padding-top:1rem}</style>',unsafe_allow_html=True)
st.markdown('<style>.stToolbar{display:none} .css-fblp2m{display:none} .css-10pw50{display:none}</style>',unsafe_allow_html=True)
# End Page Setting

# Start Generic Function

df = pd.DataFrame()

def load_df(df):
    return df

def is_string_type(s: pd.Series):
    return is_string_dtype(s)

def is_numeric(col: pd.Series):
    try:
        return is_numeric_dtype(col)
    except:
        return False

def count_numerical_categorical_column(df,type_to_count):
    count_num = 0
    count_cat = 0
    for c in df.columns:
        if type_to_count == "numerical":
            if is_numeric(df[c]):
                count_num +=1
                return count_num
            else:
                count_cat +=1
            return count_cat


def clean_df(df):
    #fill null values
    for c in df:
        if is_numeric(df[c]):
            mean_value = df[c].mean()
            df[c].fillna(mean_value,inplace=True)
        elif is_string_type(df[c]):
            col_mode_value = df[c].mode()
            df[c].fillna(col_mode_value,inplace=True)
    return df

def get_df_mumerical_cols(df):
    mumerical_cols = []
    for c in df:
        if is_numeric(df[c]):
            mumerical_cols.append(c)
    return mumerical_cols

def get_df_other_cols(df):
    other_cols = []
    for c in df:
        if is_string_dtype(df[c]):
            other_cols.append(c)
    return other_cols

def get_df_info(df):
    buffer = io.StringIO()
    df.info(buf=buffer)
    s = buffer.getvalue()
    return s

def get_df_summary(df):
    return df.describe()

def get_df_columns(df):
    return df.columns

def get_df_col_types(df):
    return df.dtypes

# End Generic Function

# Start Page Logic
col_one,col_two = st.columns(2)

with col_one:
    f1 = st.file_uploader(':file_folder: upload a file',type=['csv','xlsx','xls'])
    
    if f1 is not None:
        # Check MIME type of the uploaded file
        if f1.type == "text/csv":
            df = pd.read_csv(f1,encoding="ISO-8859-1")
            file_name = f1.name
        elif f1.type:
            df = pd.read_excel(f1,encoding="ISO-8859-1")
            file_name = f1.name
        else:
            streamlit_js_eval(js_expressions="parent.window.location.reload()")

with col_two:
    if f1 is not None:
        btn_clean_data = st.button(':canoe: Clean Data',use_container_width=True)
        if btn_clean_data:
            df = clean_df(df)
col1,col2 = st.columns(2)

mselect_values = st.sidebar.multiselect('Select Filter Term',options=get_df_columns(df))



with col1:
    if f1 is not None:
        st.write(load_df(df))
        with st.expander('Data Justification Operations',expanded=True):     
            st.markdown(f'<span style="color: rgb(9, 171, 59);font-weight: bold;font-size: 18px;">Analyise Data</span>',unsafe_allow_html=True)
            c3,c4 = st.columns(2)
            with c3 :
                btn_get_data_info = st.button(':open_book: Get Data Info',use_container_width=True)
            with c4 : 
                btn_get_data_desc = st.button(':dark_sunglasses: Get Data Desciptions (Statistics)',use_container_width=True)
            if btn_get_data_info:
                st.text(get_df_info(df))
            if btn_get_data_desc:
                st.write(get_df_summary(df))

            rd_preview = st.radio('Select Option :writing_hand: ',options=('Data Columns','Data Types','Data Shape'),key='rd_preview_value')         
            if rd_preview:
                if st.session_state.rd_preview_value == 'Data Columns':
                    col_df = pd.DataFrame(get_df_columns(df).tolist())
                    st.write(col_df)                
                if st.session_state.rd_preview_value == 'Data Types':
                    st.text(get_df_col_types(df),)        
                if st.session_state.rd_preview_value == 'Data Shape':
                    row_num = df.shape[0]
                    col_num = df.shape[1]
                    st.markdown(
                        f'Data has <span style="color:rgb(14 135 163)"> {row_num} </span> Rows and <span style="color:rgb(14 135 163)"> {col_num} </span> Columns',unsafe_allow_html=True
                    )

            st.markdown(f'<span style="color: rgb(9, 171, 59);font-weight: bold;font-size: 18px;">Correlation & Heatmap</span>',unsafe_allow_html=True)
            c5,c6 = st.columns(2)
            with c5 :
                btn_data_correlation= st.button(':abacus: Data Correlation',use_container_width=True)
            with c6 : 
                btn_get_data_heatmap = st.button(':sunny: Data Heatmap ',use_container_width=True)
            if btn_data_correlation:
                st.write(df.corr(numeric_only=True))

            if btn_get_data_heatmap:
                fig, ax = plt.subplots()
                sns.heatmap(df.corr(numeric_only=True), ax=ax)
                st.write(fig)      


with col2:

    # Draw Selected Data As Radio Button List
    if f1 is not None:
        with st.expander('',expanded=True):
                st.markdown(f'<span style="color: rgb(9, 171, 59);font-weight: bold;font-size: 18px;">Show All Data Distribution</span>',unsafe_allow_html=True)
                c1,c2 =st.columns(2)
                with c1:
                    rd__numerical_graph_options = st.radio(':chart_with_downwards_trend: Select Graph Type',options=('Histogram','Box Plot','Density Plot'),horizontal=True)                                              
                    btn_numerical_data_click = st.button(':chart_with_downwards_trend: Plot All Numerical Data',use_container_width=True)
                with c2:
                    rd_categrical_graph_options = st.radio(':chart_with_downwards_trend: Select Graph Type',options=('Bar Plot','Box Plot','violin Plot'),horizontal=True)                                              
                    btn_categorical_data_click = st.button(':chart_with_downwards_trend: Plot All Categorical Data',use_container_width=True)

                if btn_numerical_data_click and rd__numerical_graph_options:
                       if rd__numerical_graph_options:
                            for c in df:
                                if is_numeric(df[c]):
                                    fig, axes = plt.subplots(sharey=True)
                                    if rd__numerical_graph_options == 'Histogram':
                                         st.markdown(f'<span style="color: rgb(9, 171, 59);font-weight: bold;font-size: 18px;">{c}</span> distributions',unsafe_allow_html=True)
                                         fig = px.histogram(df,x=c,y=c,template='seaborn')
                                         st.plotly_chart(fig,use_container_width=True,height=200)     
                                    elif rd__numerical_graph_options == 'Box Plot':
                                         st.markdown(f'<span style="color: rgb(9, 171, 59);font-weight: bold;font-size: 18px;">{c}</span> distributions',unsafe_allow_html=True)
                                         fig = px.box(y=df[c])
                                         st.plotly_chart(fig,use_container_width=True,height=200)                                             
                                    else:
                                        st.markdown(f'<span style="color: rgb(9, 171, 59);font-weight: bold;font-size: 18px;">{c}</span> distributions',unsafe_allow_html=True)                                        
                                        sns.kdeplot(df[c], bw=0.5)

                                    st.plotly_chart(fig,use_container_width=True,height=200) 

                if btn_categorical_data_click:                          
                       if rd_categrical_graph_options:        
                            for c in df:
                                if is_string_dtype(df[c]):
                                    fig, axes = plt.subplots(sharey=True)
                                    if rd_categrical_graph_options == 'Bar Plot':
                                         st.markdown(f'<span style="color: rgb(9, 171, 59);font-weight: bold;font-size: 18px;">{c}</span> distributions',unsafe_allow_html=True)
                                         fig = px.bar(df,x=c,y=c,template='seaborn')
                                         st.plotly_chart(fig,use_container_width=True,height=200)     
                                    elif rd_categrical_graph_options == 'Box Plot':
                                         st.markdown(f'<span style="color: rgb(9, 171, 59);font-weight: bold;font-size: 18px;">{c}</span> distributions',unsafe_allow_html=True)
                                         fig = px.box(y=df[c])
                                         st.plotly_chart(fig,use_container_width=True,height=200)                                             
                                    else:
                                        st.markdown(f'<span style="color: rgb(9, 171, 59);font-weight: bold;font-size: 18px;">{c}</span> distributions',unsafe_allow_html=True)                                        
                                        fig = px.violin(df[c], color=df[c])

                                    st.plotly_chart(fig,use_container_width=True,height=200) 


    # Draw Selected Data As Radio Button List
    with st.expander('',expanded=True):
        if f1 is not None:
            rdColSelectedOne = st.radio('Select Column To Plot Value',options=mselect_values,
                                        horizontal=True,key='rd_col_key')
            
            if rdColSelectedOne is not None:
                if is_numeric(df[rdColSelectedOne]):
                    with col2:
                        st.markdown(f'<span style="color: rgb(9, 171, 59);font-weight: bold;font-size: 18px;">{rdColSelectedOne}</span> distributions',unsafe_allow_html=True)
                        fig = px.histogram(df,x=rdColSelectedOne,y=rdColSelectedOne,template='seaborn')
                        st.plotly_chart(fig,use_container_width=True,height=200)
                        
                        # fig = px.pie(df,names=rdColSelectedOne,values=rdColSelectedOne,template='seaborn')
                        # st.plotly_chart(fig,use_container_width=True,height=200)     



                        fig = px.pie(df,values=rdColSelectedOne,names=rdColSelectedOne,hole=0.5)
                        fig.update_traces(text=df[rdColSelectedOne],textposition='outside')
                        st.plotly_chart(fig,use_container_width=True)                    

                elif is_string_type(df[rdColSelectedOne]):
                    with col2:
                        st.markdown(f'<span style="color: rgb(9, 171, 59);font-weight: bold;font-size: 18px;">{rdColSelectedOne}</span> distributions',unsafe_allow_html=True)
                        # fig = px.bar(df,x=rdColSelectedOne,y=df[rdColSelectedOne].mode(),text=['${:,.2f}'.format(x) for x in df[rdColSelectedOne]],template='seaborn')
                        fig = px.bar(df,x=rdColSelectedOne,y=rdColSelectedOne,text=[x for x in df[rdColSelectedOne]],template='seaborn')
                        st.plotly_chart(fig,use_container_width=True,height=200)       

                        # fig = px.pie(df,names=rdColSelectedOne,values=rdColSelectedOne,template='seaborn')
                        # st.plotly_chart(fig,use_container_width=True,height=200)                    



        #Plot Column Based On it's Data Type



# End Page Logic