import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

import warnings
warnings.filterwarnings('ignore')

# Load data
data_file = "hhs_project_data.csv"
df = pd.read_csv(data_file)

# Define functions for screens
def overview():
    st.title("HHS Project Dashboard")
    st.write("This dashboard provides insights into the progress of the HHS Knowledge Management System project.")
    st.dataframe(df)

def phase_summary():
    st.title("Phase Summary")
    st.write("Summary of costs and tasks across different project phases.")
    
    phase_data = df.groupby("Phase").agg({"Cost": "sum", "Task": "count"}).reset_index()
    phase_data.columns = ["Phase", "Total Cost", "Number of Tasks"]
    
    st.bar_chart(phase_data.set_index("Phase")["Total Cost"], use_container_width=True)
    st.write("### Phase Details")
    st.dataframe(phase_data)

def task_status():
    st.title("Task Status Overview")
    st.write("Distribution of task statuses across the project.")
    
    status_data = df["Status"].value_counts().reset_index()
    status_data.columns = ["Status", "Count"]
    
    st.pie_chart(status_data.set_index("Status"), use_container_width=True)
    st.write("### Task Status Details")
    st.dataframe(status_data)

def filter_data():
    st.title("Filter Data and Visualizations")
    st.write("Use filters to view specific subsets of the project data and visualize key metrics.")
    
    # Filters
    phase = st.selectbox("Select Phase", ["All"] + df["Phase"].unique().tolist())
    status = st.selectbox("Select Status", ["All"] + df["Status"].unique().tolist())
    
    filtered_df = df.copy()
    if phase != "All":
        filtered_df = filtered_df[filtered_df["Phase"] == phase]
    if status != "All":
        filtered_df = filtered_df[filtered_df["Status"] == status]
    
    st.write("### Filtered Data")
    st.dataframe(filtered_df)

    # Filtered plots
    st.write("### Filtered Plots")
    if not filtered_df.empty:
        st.write("#### Cost Distribution")
        plt.figure(figsize=(10, 5))
        filtered_df.groupby("Phase")["Cost"].sum().plot(kind="bar")
        plt.ylabel("Total Cost")
        plt.xlabel("Phase")
        st.pyplot(plt)

        st.write("#### Task Count by Status")
        plt.figure(figsize=(10, 5))
        filtered_df["Status"].value_counts().plot(kind="bar", color="skyblue")
        plt.ylabel("Number of Tasks")
        plt.xlabel("Status")
        st.pyplot(plt)
    else:
        st.write("No data available for the selected filters.")

def cost_breakdown():
    st.title("Cost Breakdown")
    st.write("Breakdown of costs by task and phase.")
    
    cost_phase = df.groupby("Phase")["Cost"].sum().reset_index()
    cost_task = df.groupby("Task")["Cost"].sum().reset_index().sort_values(by="Cost", ascending=False)
    
    st.write("### Costs by Phase")
    st.bar_chart(cost_phase.set_index("Phase"), use_container_width=True)
    st.write("### Costs by Task")
    st.bar_chart(cost_task.set_index("Task"), use_container_width=True)

def progress_timeline():
    st.title("Progress Timeline")
    st.write("Visualize the project timeline and progress by start and end dates.")
    
    df["Start Date"] = pd.to_datetime(df["Start Date"])
    df["End Date"] = pd.to_datetime(df["End Date"])
    
    st.write("### Gantt Chart of Tasks")
    st.write("This feature requires integration with plotly or Altair for timeline charts.")
    # Placeholder for Gantt chart
    # You can use plotly.express.timeline here if required

# Streamlit sidebar navigation
st.sidebar.title("Navigation")
menu = st.sidebar.radio(
    "Navigate to", 
    ["Overview", "Phase Summary", "Task Status", "Filter Data and Visualizations", "Cost Breakdown", "Progress Timeline"]
)

# Conditional rendering based on selected menu
if menu == "Overview":
    overview()
elif menu == "Phase Summary":
    phase_summary()
elif menu == "Task Status":
    task_status()
elif menu == "Filter Data and Visualizations":
    filter_data()
elif menu == "Cost Breakdown":
    cost_breakdown()
elif menu == "Progress Timeline":
    progress_timeline()
