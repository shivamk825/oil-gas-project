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
#---------------------- mboe graph-----------
    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=all_companies,
        y=employe
    ))

    fig.update_layout(
        autosize=False,
        width=500,
        height=500,
        yaxis=dict(
            title_text="Sum of Total Mboe/D",

            tickmode="array",
            titlefont=dict(size=20),
        )
    )

    fig.update_yaxes(automargin=True)
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

    df5 = df.sort_values(by=['Marketcap'], ascending=True)
    fig = go.Figure(go.Bar(x=df5.Company, y=df5["Marketcap"], name='Marketcap'))
    fig.add_trace(go.Bar(x=df5.Company, y=df5['Enterprisevalue'], name='Enterprisevalue'))
    fig.update_layout(barmode='stack',xaxis={'categoryorder':'total descending'})
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

    return render_template('index.html',listofcompanies=all_companies,graph=graphJSON,graphemp=graphJSONemp,marketenterpricegraph=graphJSONmarfenterprice,ebitdagraph=graphJSONebitda)
app.run()
