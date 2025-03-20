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

cs_program_list = ['Computer Science & Engineering',
 'Computer Science and Engineering with Specialization in Data Science and Artificial Intelligence',
 'Computer Science',
 'Dual Degree M.Tech. - Ph.D in IT  with specialization in Machine Learning, Robotics and Human Computer Interaction Group',
 'Computer Science and Engineering with Specialization in Artificial Intelligence and Data Science',
 'Computer Science & Information Security',
 'Computer Integrated Manufacturing',
 'Computer Science & Engineering (Artificial Intelligence)',
 'Computer Science and  Engineering (Cyber Security)',
 'Computer Science & Technology',
 'Computer Aided Design Manufacture and Engineering',
 'M.Tech. IT with specialization in Machine Learning, Robotics and Human Computer Interaction Group',
 'Computer Engineering (Cyber Security)',
 'Computer Science & Engineering (Information Security)',
 'Computer Aided Design & Manufacturing',
 'Computer Networking',
 'Computer Engineering',
 'Computer Science & Engineering in (Artificial Intelligence & Data Science)',
 'Computer Science & Engineering (Analytics)']

aiml_program_list = [ 'Computer Science and Engineering with Specialization in Data Science and Artificial Intelligence',
 'Data Science',
 'M.Tech. IT  with specialization in Software and Data Engineering Group',
 'Artificial Intelligence',
 'Data Science & Engineering',
 'Dual Degree M.Tech. - Ph.D in IT  with specialization in Machine Learning, Robotics and Human Computer Interaction Group',
 'Computer Science and Engineering with Specialization in Artificial Intelligence and Data Science',
 'M.Tech in Artificial Intelligence',
 'M.Tech in Data Science',
 'Machine Learning and Computing',
 'M.Tech in Artificial Intelligence and Machine Learning',
 'Signal Processing and Machine Learning',
 'Data Analytics',
 'Artificial Intelligence & Data Science',
 'Computer Science & Engineering (Artificial Intelligence)',
 'Dual Degree M.Tech. - Ph.D  in IT with specialization in Software and Data Engineering Group',
 'Artificial Intelligence and Machine Learning',
 'M.Tech. IT with specialization in Machine Learning, Robotics and Human Computer Interaction Group',
 'Data Science and Engineering',
 'Computational and Data Science',
 'Industrial Engineering and Data Analytics',
 'Computer Science & Engineering in (Artificial Intelligence & Data Science)',
 'Machine Intelligence and Automation']


if special_filter == "CS-programs":
    df = df[df["PG Program"].isin(cs_program_list)]

elif special_filter == "AIML-programs":
    df = df[df["PG Program"].isin(aiml_program_list)]

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
st.markdown(
    """
Developed by Shivraj Anand.
[Contact](https://shivrajanand.github.io)
"""
)
# Data source note
st.markdown(
    """
    **ℹ️ Note:** This data is based on [CCMT Counselling 2024 official records](https://admissions.nic.in/CCMT/Applicant/Report/ORCRReport.aspx?enc=Nm7QwHILXclJQSv2YVS+7jwDCTS6FhNmjKGAxsSogZ/WSC5YMGOlm6wjUQsaRQ5B).
    """
)

st.markdown(f"### Showing {len(df)} matching programs")
st.dataframe(df.reset_index(drop=True), use_container_width=True)
