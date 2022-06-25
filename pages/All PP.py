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
st.title("All PP")
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


@st.experimental_memo
def get_data() -> pd.DataFrame:
    return pd.read_csv(dataset_url)


df = get_data()


# # Formatting Image URL
# image_url = []
# for i in df['image']:
#     image_url.append('<img src=' + i + ' width="100">')
# df['image'] = image_url

# Aggrid Defined
def aggrid_interactive_table(df: pd.DataFrame):
    """Creates an st-aggrid interactive table based on a dataframe.

    Args:
        df (pd.DataFrame]): Source dataframe

    Returns:
        dict: The selected row
    """
    options = GridOptionsBuilder.from_dataframe(df, enableRowGroup=True, enableValue=True, enablePivot=True)
    options.configure_side_bar(filters_panel=True)
    options.configure_selection("single")

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
    # st.write(df.to_html(escape=False), unsafe_allow_html=True)
    # st.dataframe(df)
    selection = aggrid_interactive_table(
        df[['number', 'Batch', 'Type', 'Total Score', 'Background', 'Base', 'Outfit',
            'Necklace', 'Eye', 'Beard', 'Hair', 'Hat', 'Hand_Accessories', 'Shoulder',
            'Mouth']])

    try:
        image_number = selection["selected_rows"][0]['number']
        image_url = (df[df['number'] == image_number]['image']).iloc[0]
    except Exception as e:
        image_number = ""
        image_url = "https://www.liquiddriver.finance/static/media/logoImg.32a133f7.svg"

    if selection:
        st.write("You selected:")

        st.image(image_url, caption=["# " + str(image_number)], width=100)  # Images

    time.sleep(1)
