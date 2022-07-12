# Importing Libraries
import streamlit as st
import requests
import pandas as pd
import yaml
import plotly.express as px

# App
st.set_page_config(
    page_title="PP Stats",
    page_icon="icons/pp.png",
    layout="wide",
)

# Title
st.title("🔢 Pixel Pirate Statistics")

# Params
params_path = "params.yaml"


def read_params(config_path):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config


config = read_params(params_path)

# Read Data
dataset_url = config["main"]["data-source"]
stats_url = config["stats"]["api"]


def get_data(dataset) -> pd.DataFrame:
    return pd.read_csv(dataset)


nft_df = get_data(dataset_url)

# Scraping Data
r = requests.get(stats_url)
stats = r.json()
stats_df = pd.json_normalize(stats)
columns_with_nos = ['collection.stats.averagePrice', 'collection.stats.floor', 'collection.stats.lastSellPrice',
                    'collection.stats.totalVolumeTraded', 'collection.stats.volumeLast24Hours',
                    'collection.stats.volumeLast7Days',
                    'collection.stats.sale.floorSaleTVL', 'collection.stats.sale.volumeLast24Hours',
                    'collection.stats.sale.volumeLast7Days',
                    'collection.stats.sale.totalVolumeTraded', 'collection.stats.sale.totalVolumeTradedFTM',
                    'collection.stats.floorCap',
                    'collection.stats.floorFTM', 'collection.stats.lastSellPriceFTM',
                    'collection.stats.totalVolumeTradedFTM']
for i in columns_with_nos:
    stats_df[i] = stats_df[i].apply(lambda x: int(x) / 1000000000000000000)  # Format Conversion

# Getting data ready
unique_holders = len(nft_df.address.unique())  # Unique PP Holders
pp_floor = stats_df['collection.stats.floor'][0] # PP Floor
number_of_pps = len(nft_df) # Number of PPs
number_of_active_sales = stats_df['collection.stats.sale.numActiveSales'][0] # Number of Active Sales
number_of_trades_24hr = stats_df['collection.stats.sale.numTradesLast24Hours'][0] # Number of Trades Last 24 Hours
volume_24hr = stats_df['collection.stats.volumeLast24Hours'][0] # Volume Last 24 Hours
number_of_trades_7d = stats_df['collection.stats.sale.numTradesLast7Days'][0] # Number of Trades Last 7 Days
volume_7d = stats_df['collection.stats.volumeLast7Days'][0] # Volume Last 7 Days
number_of_trades_alltime = stats_df['collection.stats.sale.totalTrades'][0] # Total Number of Sales
volume_alltime = stats_df['collection.stats.totalVolumeTraded'][0] # Total Volume Traded


# creating a single-element container
placeholder = st.empty()

# Empty Placeholder Filled
with placeholder.container():
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Unique PP Holders", unique_holders)
    col2.metric("Number of PPs", number_of_pps)
    col3.metric("PP Floor in FTM", pp_floor)
    col4.metric("Number of Active Sales", number_of_active_sales)

    dfg = nft_df['address'].value_counts().reset_index().sort_values('address', ascending = False).head(10)
    dfg['index'] = [i[:6] for i in dfg['index']]
    fig = px.bar(dfg, x='address', y ='index', labels={"address": "Number of PPs", "index": "Holders"}, text='address')
    fig.update_layout(title="Top 10 PP Whales", xaxis_title="Number of PPs", yaxis_title="Holders", yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig, use_container_width=True)


    col1, col2, col3 = st.columns(3)

    col1.markdown("#### Last 24 Hours")
    col2.markdown("#### Last 7 Days")
    col3.markdown("#### All Time")


    col1, col2, col3, col4, col5, col6 = st.columns(6)

    col1.metric("Number of Trades", number_of_trades_24hr)
    col2.metric("Volume Traded in FTM", volume_24hr)
    col3.metric("Number of Trades", number_of_trades_7d)
    col4.metric("Volume Traded in FTM", volume_7d)
    col5.metric("Number of Trades", number_of_trades_alltime)
    col6.metric("Volume Traded in FTM", volume_alltime)