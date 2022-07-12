# Importing Libraries
import time
import pandas as pd
import streamlit as st
import yaml
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import GridUpdateMode

# App
st.set_page_config(
    page_title="All PP Details",
    page_icon="icons/pp.png",
    layout="wide",
)

# Title
st.title("🍆 All PP")
# st.markdown("# All PP")

# Params
params_path = "params.yaml"


def read_params(config_path):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config


config = read_params(params_path)

# Read Data
dataset_url = config["main"]["data-source"]


def get_data() -> pd.DataFrame:
    return pd.read_csv(dataset_url)


df = get_data()

# Sidebar Data
batch = pd.unique(df["Batch"])
type = pd.unique(df["Type"])
background = pd.unique(df["Background"])
base = pd.unique(df["Base"])
outfit = pd.unique(df["Outfit"])
necklace = pd.unique(df["Necklace"])
eye = pd.unique(df["Eye"])
beard = pd.unique(df["Beard"])
hair = pd.unique(df["Hair"])
hat = pd.unique(df["Hat"])
hand = pd.unique(df["Hand_Accessories"])
shoulder = pd.unique(df["Shoulder"])
mouth = pd.unique(df["Mouth"])

# Sidebar - title & filters
st.sidebar.markdown('### Data Filters')
batch_choice = st.sidebar.multiselect(
    'Choose batch:', batch, default=batch)
type_choice = st.sidebar.multiselect(
    'Choose type:', type, default=type)
background_choice = st.sidebar.multiselect(
    'Choose background:', background, default=background)
base_choice = st.sidebar.multiselect(
    'Choose base:', base, default=base)
outfit_choice = st.sidebar.multiselect(
    'Choose outfit:', outfit, default=outfit)
necklace_choice = st.sidebar.multiselect(
    'Choose necklace:', necklace, default=necklace)
eye_choice = st.sidebar.multiselect(
    'Choose eye:', eye, default=eye)
beard_choice = st.sidebar.multiselect(
    'Choose beard:', beard, default=beard)
hair_choice = st.sidebar.multiselect(
    'Choose hair:', hair, default=hair)
hat_choice = st.sidebar.multiselect(
    'Choose hat:', hat, default=hat)
hand_choice = st.sidebar.multiselect(
    'Choose hand:', hand, default=hand)
shoulder_choice = st.sidebar.multiselect(
    'Choose shoulder:', shoulder, default=shoulder)
mouth_choice = st.sidebar.multiselect(
    'Choose mouth:', mouth, default=mouth)

# dataframe filter
df = df[df["Batch"].isin(batch_choice)]
df = df[df["Type"].isin(type_choice)]
df = df[df["Background"].isin(background_choice)]
df = df[df["Base"].isin(base_choice)]
df = df[df["Outfit"].isin(outfit_choice)]
df = df[df["Necklace"].isin(necklace_choice)]
df = df[df["Eye"].isin(eye_choice)]
df = df[df["Beard"].isin(beard_choice)]
df = df[df["Hair"].isin(hair_choice)]
df = df[df["Hat"].isin(hat_choice)]
df = df[df["Hand_Accessories"].isin(hand_choice)]
df = df[df["Shoulder"].isin(shoulder_choice)]
df = df[df["Mouth"].isin(mouth_choice)]


# Aggrid Defined
def aggrid_interactive_table(df: pd.DataFrame):
    """Creates an st-aggrid interactive table based on a dataframe.

    Args:
        df (pd.DataFrame]): Source dataframe

    Returns:
        dict: The selected row
    """
    options = GridOptionsBuilder.from_dataframe(df, enableRowGroup=True, enableValue=True, enablePivot=True,
                                                autoHeight=True)
    options.configure_side_bar(filters_panel=True)
    options.configure_selection(selection_mode="multiple", rowMultiSelectWithClick=True)

    selection = AgGrid(
        df,
        enable_enterprise_modules=True,
        gridOptions=options.build(),
        theme="light",
        update_mode=GridUpdateMode.MODEL_CHANGED,
        allow_unsafe_jscode=True,
    )

    return selection


# creating a single-element container
placeholder = st.empty()

# Empty Placeholder Filled
with placeholder.container():
    st.markdown("### All PP Details")
    selection = aggrid_interactive_table(
        df[['number', 'Batch', 'Type', 'Total Score', 'Background', 'Base', 'Outfit',
            'Necklace', 'Eye', 'Beard', 'Hair', 'Hat', 'Hand_Accessories', 'Shoulder',
            'Mouth']])

    # Image Data
    image_number = [i['number'] for i in selection["selected_rows"]]
    image_url = (df[df['number'].isin(image_number)]['image'])

    if selection:
        st.image(image_url.tolist(), caption=["# " + str(i) for i in image_number], width=200)  # Images

    time.sleep(1)
