import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Uber App",
    page_icon="🚕",
    layout="wide"
)

# Load data
@st.cache_data
def load_data():
    return (
        pd.read_csv("https://s3-us-west-2.amazonaws.com/streamlit-demo-data/uber-raw-data-sep14.csv.gz")
        .rename(columns=lambda x: x.lower())
        .assign(
            datetime=lambda x: pd.to_datetime(x["date/time"]),
            date=lambda df: df["datetime"].dt.date,
            weekday=lambda df: df["datetime"].dt.day_name(),
            hour=lambda df: df["datetime"].dt.hour,
        )
    )

with st.sidebar:
    st.image("https://www.cidaen.es/assets/img/cidaen.png")
    nrows_selected = st.slider("Número de filas", 0, 100000, 10000)
    weekday_selected = st.selectbox("Día de la semana", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
    hour_selected = st.slider("Hora", 0, 23, 12)
    
df = load_data()

df = (
    df
    .iloc[:nrows_selected]
)

st.title("SUPER APP: Uber pickups en NYC")

show_table = st.checkbox("Mostrar datos crudos")
if show_table:
    st.write("## Datos crudos")
    st.dataframe(df.head())
    
col1, col2 = st.columns(2)

with col1:
    st.write("## Media de pickups por día de la semana")
    
    mean_pickups_by_weekday = (
        df
        .loc[lambda df: df["weekday"] == weekday_selected]
        .groupby("date")
        .size()
        .mean()
    )
    
    global_mean_pickups = (
        df
        .groupby(["date"])
        .size()
        .mean()
    )
    
    st.metric(
        f"Media pickups {weekday_selected}",
        mean_pickups_by_weekday,
        delta=f"{mean_pickups_by_weekday/global_mean_pickups-1:.2%}",
    )
    
with col2:
    st.write("## Media de pickups por hora")
    
    mean_pickups_by_hour = (
        df
        .loc[lambda df: df["hour"] == hour_selected]
        .assign(
            year=lambda df: df["datetime"].dt.year,
            month=lambda df: df["datetime"].dt.month,
            day=lambda df: df["datetime"].dt.day,
        )
        .groupby(["year", "month", "day", "hour"])    
        .size()
        .mean()
    )
    
    global_mean_pickups = (
        df
        .assign(
            year=lambda df: df["datetime"].dt.year,
            month=lambda df: df["datetime"].dt.month,
            day=lambda df: df["datetime"].dt.day,
        )
        .groupby(["year", "month", "day", "hour"])    
        .size()
        .mean()
    )
    
    st.metric(
        f"Media pickups {hour_selected}:00",
        f"{mean_pickups_by_hour:.0f}",  
        delta=f"{mean_pickups_by_hour/global_mean_pickups-1:.2%}",
    )
    
st.map((
    df
    .loc[lambda df: df["weekday"] == weekday_selected]
    .loc[lambda df: df["hour"] == hour_selected]
))