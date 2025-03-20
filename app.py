import streamlit as st
import pandas as pd

# Set wide layout
st.set_page_config(layout="wide")

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("ccmt_data.psv", sep="|")
    return df

df = load_data()

# Helper: Extract institute type
def get_institute_type(name):
    name = name.lower()
    if "indian institute of technology" in name:
        return "IIT"
    elif "indian institute of information technology" in name:
        return "IIIT"
    elif "national institute of technology" in name:
        return "NIT"
    else:
        return "OTHER"

df["Institute Type"] = df["Institute"].apply(get_institute_type)

# --- Sidebar Filters ---
st.sidebar.header("🎯 Filter Options")

# 1. Institute Type
institute_choice = st.sidebar.radio(
    "Select Institute Type",
    options=["ALL", "IIT", "NIT", "IIIT"],
    index=0
)

if institute_choice != "ALL":
    df = df[df["Institute Type"] == institute_choice]

# 2. PG Program filter
pg_programs = df["PG Program"].unique().tolist()
pg_selected = st.sidebar.multiselect(
    "Select PG Programs (optional)",
    options=pg_programs,
    default=[]  # Initially empty
)

# --- Special Filters ---
st.sidebar.markdown("### 🔍 Special Program Filters")

special_filter = st.sidebar.radio(
    "Quick Filter by Program Type",
    options=["None", "CS-programs", "AIML-programs"],
    index=0
)

# Apply special program filters if selected
if special_filter == "CS-programs":
    df = df[df["PG Program"].str.contains("computer", case=False, na=False)]

elif special_filter == "AIML-programs":
    keywords = ["data", "machine", "intelligence", "ai", "ml", "learning"]
    df = df[df["PG Program"].str.contains('|'.join(keywords), case=False, na=False)]

# Apply user-selected PG Programs if any
if pg_selected:
    df = df[df["PG Program"].isin(pg_selected)]

# 3. Category filter
categories = df["Category"].unique().tolist()
categories.sort()
categories = ["All"] + categories  # Add "All" option

category_selected = st.sidebar.selectbox(
    "Select Category",
    options=categories
)

if category_selected != "All":
    df = df[df["Category"] == category_selected]


# 4. GATE Score input
user_gate_score = st.sidebar.number_input(
    "Enter your GATE score",
    min_value=0,
    value=1000,
    step=1
)

# Final filter by GATE score
df["Min GATE Score"] = pd.to_numeric(df["Min GATE Score"], errors="coerce")
df = df[df["Min GATE Score"] <= user_gate_score]

# --- Display Result ---
st.title("🎓 CCMT Program Finder")

# Data source note
st.markdown(
    """
    **ℹ️ Note:** This data is based on [CCMT Counselling 2024 official records](https://admissions.nic.in/CCMT/Applicant/Report/ORCRReport.aspx?enc=Nm7QwHILXclJQSv2YVS+7jwDCTS6FhNmjKGAxsSogZ/WSC5YMGOlm6wjUQsaRQ5B).
    """
)

st.markdown(f"### Showing {len(df)} matching programs")
st.dataframe(df.reset_index(drop=True), use_container_width=True)
