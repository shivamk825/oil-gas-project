from flask import Flask
from flask import render_template,request
import pandas as pd
import json
import plotly.graph_objects as go
import plotly.express as px
from plotly.utils import PlotlyJSONEncoder
import plotly
import requests
from flask import Flask, jsonify
import numpy as np

app=Flask(__name__)  
@app.route('/')
def dahsboard():
    df=pd.read_csv('C:/Users/91855/Desktop/oilgas1.csv',index_col=0)
    print(df.head())
    companies=df['Company'].dropna()
    employe=df['Employees'].dropna()
    enterprice=df['Enterprisevalue'].dropna()
    market_cap=df['Marketcap'].dropna()    
    ebitda=df['Ebitda'].dropna()    

    employe.tolist()
    enterprice.tolist()    
    market_cap.tolist()
    ebitda.tolist()
    all_companies = companies.tolist()
    print(all_companies)
    dropdown_selection=['BigCompanies','SmallCompanies','AllCompanies']
#---------------------- mboe graph-----------
    
    df_mboe=pd.read_csv('C:/Users/91855/Desktop/all_company_one_csv_complete_conversion (1).csv',index_col=0)
    fig = go.Figure(go.Bar(x=df_mboe.Company, y=df_mboe["Natural Gas"], name='Natural Gas',marker_color='red'))
    fig.add_trace(go.Bar(x=df_mboe.Company, y=df_mboe['Oil'], name='Oil',marker_color='green'))
    fig.add_trace(go.Bar(x=df_mboe.Company, y=df_mboe['NGL'], name='NGL',marker_color='yellow'))
    fig.update_layout(barmode='stack',xaxis={'categoryorder':'total descending'})
    fig.update_layout(template="simple_white")
    graphJSON =json.dumps(fig,cls=plotly.utils.PlotlyJSONEncoder)

#---------------------- mboe graph end -----------

#---------------------employee==============

    df2 = df.sort_values(by=['Employees'], ascending=True)
    fig= px.bar(df2, y='Company', x='Employees', text='Employees',color='Employees')
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    fig.update_layout(template="simple_white")
    graphJSONemp =json.dumps(fig,cls=plotly.utils.PlotlyJSONEncoder)

#---------------------employee end ==============

###---------------market enter -----------------###############

    data3= df.sort_values(by=['Marketcap'], ascending=True)
    fig = go.Figure()
    fig.add_trace(go.Bar(x=data3.Company,
                    y=data3["Marketcap"],
                    name='Marketcap',
                    marker_color='green'
                    ))
    fig.add_trace(go.Bar(x=data3.Company,
                    y=data3["Enterprisevalue"],
                    name='Enterprisevalue',
                    marker_color='red'
                    ))
 
    fig.update_layout(
        title='Market Cap & Enterprise Value',
        xaxis=dict(tickfont_size=10,title='Company'),
        yaxis=dict(titlefont_size=20,
            tickfont_size=14,
        ),
        legend=dict(
            x=0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        barmode='group',
        bargap=0.15,
        bargroupgap=0.1 
    )
    fig.update_layout(template="simple_white")
    graphJSONmarfenterprice =json.dumps(fig,cls=plotly.utils.PlotlyJSONEncoder)
###---------------market enter end -----------------###############  


    ###---------------ebitda enter -----------------###############

    df3 = df.sort_values(by=['Ebitda'], ascending=True)
    fig= px.bar(df3, y='Ebitda', x='Company', text='Company',color='Company')
    fig.update_traces(texttemplate='%{​​​​​​​text:.2s}​​​​​​​', textposition='outside',)
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    fig.update_layout(template="simple_white")
    graphJSONebitda =json.dumps(fig,cls=plotly.utils.PlotlyJSONEncoder)

    ###---------------ebitda end -----------------###############  

    return render_template('index.html',listofselection=dropdown_selection,graph=graphJSON,graphemp=graphJSONemp,marketenterpricegraph=graphJSONmarfenterprice,ebitdagraph=graphJSONebitda)


@app.route("/selection_get" , methods=['GET', 'POST'])
def selected_dropdown_value():

    # ------------ for big and small companies------------------------------
    df=pd.read_csv('C:/Users/91855/Desktop/oilgas1.csv',index_col=0)
    small=['TALO','SBOW','SM','OAS','CXO']
    biggercomp=[]
    for i in df['compsymbol']:
        if i in small:
            pass
        else:
            biggercomp.append(i)
    print('biggercomp',biggercomp)
    #------------------------all csv-----------
    small_comp_df = pd.DataFrame()
    for i in small:
        small_comp_df=small_comp_df.append(df.loc[df['compsymbol']==i] ,ignore_index=True)
    # del small_comp_df['Unnamed: 0']
    small_comp_df=small_comp_df.fillna(0)
    print('small_comp_df',small_comp_df)

    biggercomp_df = pd.DataFrame()
    for i in biggercomp:
        biggercomp_df=biggercomp_df.append(df.loc[df['compsymbol']==i] ,ignore_index=True)
    # del biggercomp_df['Unnamed: 0']
    print('biggercomp_df',biggercomp_df)
    selected_value_from_dropdown=request.args.get('value')
    print('selected_value_from_dropdown',selected_value_from_dropdown)
    if selected_value_from_dropdown=='BigCompanies':
        dftouse=biggercomp_df
    elif selected_value_from_dropdown=='SmallCompanies':
        dftouse=small_comp_df      
    else:
        dftouse=df

    companies_selected=dftouse['Company'].dropna().tolist()
    employe_selected=dftouse['Employees'].dropna().tolist()
    enterprice_selected=dftouse['Enterprisevalue'].dropna().tolist()
    market_cap_selected=dftouse['Marketcap'].dropna().tolist()    
    ebitda_selected=dftouse['Ebitda'].dropna().tolist()   
    #------------------------all csv------end -------

    #------------------------mboe csv------
    df_mboe=pd.read_csv('C:/Users/91855/Desktop/all_company_one_csv_complete_conversion (1).csv',index_col=0)

    small_comp_df_mboe = pd.DataFrame()
    for i in small:
        small_comp_df_mboe=small_comp_df_mboe.append(df_mboe.loc[df_mboe['compsymbol']==i] ,ignore_index=True)
    small_comp_df_mboe=small_comp_df_mboe.fillna(0)
    print('small_comp_df',small_comp_df_mboe)

    biggercomp_df_mboe = pd.DataFrame()
    for i in biggercomp:
        biggercomp_df_mboe=biggercomp_df_mboe.append(df_mboe.loc[df_mboe['compsymbol']==i] ,ignore_index=True)
    print('biggercomp_df',biggercomp_df_mboe)

    #------------------------mboe csv-----------end -------


    # ------------ for big and small companies end------------------------------

#---------------------- mboe graph-----------

    if selected_value_from_dropdown=='BigCompanies':
        dftouse_mboe=biggercomp_df_mboe
    elif selected_value_from_dropdown=='SmallCompanies':
        dftouse_mboe=small_comp_df_mboe      
    else:
        dftouse_mboe=df_mboe
    fig = go.Figure(go.Bar(x=dftouse_mboe.Company, y=dftouse_mboe["Natural Gas"], name='Natural Gas',marker_color='red'))
    fig.add_trace(go.Bar(x=dftouse_mboe.Company, y=dftouse_mboe['Oil'], name='Oil',marker_color='green'))
    fig.add_trace(go.Bar(x=dftouse_mboe.Company, y=dftouse_mboe['NGL'], name='NGL',marker_color='yellow'))
    fig.update_layout(barmode='stack',xaxis={'categoryorder':'total descending'})
    fig.update_layout(template="simple_white")
    graphJSONMboerply =json.dumps(fig,cls=plotly.utils.PlotlyJSONEncoder)

#---------------------- mboe graph end -----------

#---------------------employee==============

    df_to_use_emp = dftouse.sort_values(by=['Employees'], ascending=True)
    fig= px.bar(df_to_use_emp, y='Company', x='Employees', text='Employees',color='Employees')
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    fig.update_layout(template="simple_white")
    graphJSONempgraphy =json.dumps(fig,cls=plotly.utils.PlotlyJSONEncoder)

#---------------------employee end ==============

###---------------market enter -----------------###############

    data3= dftouse.sort_values(by=['Marketcap'], ascending=True)
    fig = go.Figure()
    fig.add_trace(go.Bar(x=data3.Company,
                    y=data3["Marketcap"],
                    name='Marketcap',
                    marker_color='green'
                    ))
    fig.add_trace(go.Bar(x=data3.Company,
                    y=data3["Enterprisevalue"],
                    name='Enterprisevalue',
                    marker_color='red'
                    ))
 
    fig.update_layout(
        title='Market Cap & Enterprise Value',
        xaxis=dict(tickfont_size=10,title='Company'),
        yaxis=dict(titlefont_size=20,
            tickfont_size=14,
        ),
        legend=dict(
            x=0,
            y=1.0,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        ),
        barmode='group',
        bargap=0.15,
        bargroupgap=0.1 
    )
    fig.update_layout(template="simple_white")
    graphJSONmarketerprice =json.dumps(fig,cls=plotly.utils.PlotlyJSONEncoder)

###---------------market enter end -----------------###############  


    ###---------------ebitda enter -----------------###############

    df_to_use_ebitda = dftouse.sort_values(by=['Ebitda'], ascending=True)
    fig= px.bar(df_to_use_ebitda, y='Ebitda', x='Company', text='Company',color='Company')
    fig.update_traces(texttemplate='', textposition='outside',)
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')
    fig.update_layout(template="simple_white")
    graphJSONebitdaresponse =json.dumps(fig,cls=plotly.utils.PlotlyJSONEncoder)

    ###---------------ebitda end -----------------###############  

    return jsonify({'reply':graphJSONMboerply,'empgraphy':graphJSONempgraphy,'markentervalgraph':graphJSONmarketerprice,'ebitdagraph1':graphJSONebitdaresponse})


app.run()
