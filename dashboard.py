import streamlit as st
from db_utils import get_user_queries, toggle_favorite, delete_query, export_user_queries
import pandas as pd

def show_user_dashboard():
    st.subheader("📁 My Query Dashboard")
    
    queries_df = get_user_queries(st.session_state["user_id"])

    if queries_df.empty:
        st.info("No queries found.")
        return

    # Search/filter options
    search = st.text_input("Search your queries")
    if search:
        queries_df = queries_df[queries_df["query_text"].str.contains(search, case=False)]

    if st.checkbox("Show only favorites"):
        queries_df = queries_df[queries_df["is_favorite"] == True]

    st.dataframe(queries_df)

    # Timeline
    st.line_chart(queries_df["created_at"].dt.date.value_counts().sort_index())

    # Export
    if st.button("📥 Export CSV"):
        csv = export_user_queries(queries_df, "query_history.csv")
        st.download_button("Download CSV", csv, "query_history.csv")

    # Favorite/Delete actions
    selected_query_id = st.number_input("Query ID to modify", step=1)
    col1, col2 = st.columns(2)
    if col1.button("⭐ Toggle Favorite"):
        toggle_favorite(int(selected_query_id))
        st.experimental_rerun()
    if col2.button("🗑️ Delete"):
        delete_query(int(selected_query_id))
        st.experimental_rerun()
