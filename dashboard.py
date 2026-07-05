import streamlit as st
import pandas as pd
import plotly.express as px
from repository.velocity_dao import fetch_github_logs, fetch_figma_logs
from crew.pipeline import run_velocity_pipeline

st.set_page_config(page_title="E5 Velocity Tracking Dashboard", layout="wide")
st.title("E5 Velocity Engine Dashboard")
st.subheader("Real-time Tracking & Engineering Consistency Analytics")

st.sidebar.header("Target Infrastructure")
repo_owner = st.sidebar.text_input("Github Owner", value="your-github_username")
repo_name = st.sidebar.text_input("Repository Name", value="your-repo_name")
figma_key = st.sidebar.text_input("Figma File Key", value="s1sE1lI4ldL9Ms2SBv9YkO")

if st.sidebar.button("Run Agent Inspection Loop"):
    with st.spinner("Executing CrewAI Factory Worker Pipeline..."):
        try:
            report = run_velocity_pipeline(repo_owner, repo_name, figma_key)
            st.sidebar.success("Inspection Cycle Complete!")
            st.sidebar.write(report)
        except Exception as e:
            st.sidebar.error(f"Pipeline Interrupted: {e}")
    
tab_git, tab_figma = st.tabs(["GitHub Code Velocity", "Figma Design Velocity"])

with tab_git:
    git_data = fetch_github_logs()
    if not git_data:
        st.info("No git logs found. Execute a scan to populate.")
    else:
        df_git = pd.DataFrame(git_data)
        df_git['activity_time'] = pd.to_datetime(df_git['activity_time'], utc=True).dt.tz_convert('Asia/Manila')
        df_git['display_time'] = df_git['activity_time'].dt.strftime('%Y-%m-%d %I:%M %p')

        col1, col2 = st.columns([2, 1])

        with col1:
            st.markdown("### **How Often:** Commit Frequency Timeline")
            fig_timeline = px.scatter(
                df_git, x="activity_time", y="person", color="person",
                hover_data={"display_time": True, "detail": True, "activity_time": False},
                labels={"activity_time": "Time (Manila)", "person": "Developer"}
            )
            fig_timeline.update_traces(marker=dict(size=14, opacity=0.8))
            st.plotly_chart(fig_timeline, use_container_width=True)

        with col2:
            st.markdown("#### **How Much:** Aggregate Commits")
            commit_counts = df_git['person'].value_counts().reset_index()
            commit_counts.columns = ['Developer', 'Total Commits']

            fig_bar = px.bar(commit_counts, x='Total Commits', y='Developer', orientation='h', color='Developer')
            st.plotly_chart(fig_bar, use_container_width=True)

with tab_figma:
    figma_data = fetch_figma_logs()
    if not figma_data:
        st.info("No Figma design logs discovered in persistence layer yet.")
    else:
        df_figma = pd.DataFrame(figma_data)
        df_figma['activity_time'] = pd.to_datetime(df_figma['activity_time'], utc=True).dt.tz_convert('Asia/Manila')
        df_figma['display_time'] = df_figma['activity_time'].dt.strftime('%Y-%m-%d %I:%M %p')

        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("#### **How Often:** Design Modification Timeline")
            fig_figma_time = px.scatter(
                df_figma, x="activity_time", y="person", color="person",
                hover_data={"display_time": True, "detail": True, "activity_time": False},
                label={"activity_time": "Time (Manila)", "person": "Designer"}

            )
            fig_figma_time.update_traces(marker=dict(size=14, opacity=0.8).update(symbol="diamond"))
            st.plotly_chart(fig_figma_time, use_container_width=True)
        
        with col2:
            st.markdown("#### **How Much:** Total Canvas Mutations")
            figma_counts = df_figma['person'].value_counts().reset_index()
            figma_counts.columns = ['Designer', 'Total Modifications']

            fig_figma_bar = px.bar(figma_counts, x='Total Modifications', y='Designer', orientation='h', color='Designer')
            st.plotly_chart(fig_figma_bar, use_container_width=True)