import pandas as pd
import plotly.graph_objects as go
import streamlit as st 
from plotly.subplots import make_subplots

# TERESÓPOLIS
df = pd.read_csv("teresopolisdados.CSV", sep=";", encoding="latin1", skiprows=8)
df["Data"] = pd.to_datetime(df["Data"], format="%d/%m/%Y")
df["PRECIPITAÇÃO TOTAL, HORÁRIO (mm)"] = df["PRECIPITAÇÃO TOTAL, HORÁRIO (mm)"].astype(str).str.replace(",", ".").astype(float)
df["TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)"] = df["TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)"].astype(str).str.replace(",", ".").astype(float)
df_monthly = df.groupby(df["Data"].dt.to_period("M")).agg(
    media_temperatura=("TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)", "mean"),
    precipitacao_total=("PRECIPITAÇÃO TOTAL, HORÁRIO (mm)", "sum")
).reset_index()


df_monthly["Data"] = df_monthly["Data"].dt.strftime("%B").str.capitalize()

fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.add_trace(
    go.Bar(x=df_monthly["Data"], y=df_monthly["media_temperatura"], 
           name="Temperatura (°C)", marker_color="#32CD32"),
    secondary_y=False
)
fig.add_trace(
    go.Scatter(x=df_monthly["Data"], y=df_monthly["precipitacao_total"], 
               mode="lines+markers", name="Precipitação (mm)", 
               line=dict(color="firebrick")),
    secondary_y=True
)
fig.update_layout(
    title_text="Clima de Teresópolis",
    xaxis_title="Mês",
    yaxis_title="Precipitação (mm)",
    yaxis2=dict(title="Temperatura (°C)"),  
    legend_title="Dados",
    xaxis=dict(tickmode="array", tickvals=list(range(len(df_monthly["Data"]))), 
               ticktext=df_monthly["Data"], tickangle=-45) 
)

# PARATY
df2 = pd.read_csv("paratydados.CSV", sep=";", encoding="latin1", skiprows=8)
df2["Data"] = pd.to_datetime(df2["Data"], format="%Y/%m/%d")
df2["PRECIPITAÇÃO TOTAL, HORÁRIO (mm)"] = df2["PRECIPITAÇÃO TOTAL, HORÁRIO (mm)"].astype(str).str.replace(",", ".").astype(float)
df2["TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)"] = df2["TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)"].astype(str).str.replace(",", ".").astype(float)
df_monthly2 = df2.groupby(df2["Data"].dt.to_period("M")).agg(
    media_temperatura=("TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)", "mean"),
    precipitacao_total=("PRECIPITAÇÃO TOTAL, HORÁRIO (mm)", "sum")
).reset_index()

# Converter a coluna "Data" para o nome do mês em português
df_monthly2["Data"] = df_monthly2["Data"].dt.strftime("%B").str.capitalize()

fig2 = make_subplots(specs=[[{"secondary_y": True}]])
fig2.add_trace(
    go.Bar(x=df_monthly2["Data"], y=df_monthly2["media_temperatura"], 
           name="Temperatura (°C)", marker_color="#32CD32"),
    secondary_y=False
)
fig2.add_trace(
    go.Scatter(x=df_monthly2["Data"], y=df_monthly2["precipitacao_total"], 
               mode="lines+markers", name="Precipitação (mm)", 
               line=dict(color="firebrick")),
    secondary_y=True
)
fig2.update_layout(
    title_text="Clima de Paraty",
    xaxis_title="Mês",
    yaxis_title="Precipitação (mm)",
    yaxis2=dict(title="Temperatura (°C)"),  
    legend_title="Dados",
    xaxis=dict(tickmode="array", tickvals=list(range(len(df_monthly2["Data"]))), 
               ticktext=df_monthly2["Data"], tickangle=-45) 
)

st.plotly_chart(fig)
st.plotly_chart(fig2)

