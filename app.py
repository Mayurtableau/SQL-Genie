import streamlit as st
import pandas as pd
import altair as alt
import requests
from user_auth import register_user, validate_user, get_user_history, save_query_history
from query_runner import run_query
from test_db import get_table_schema

# --- Streamlit Page Config ---
st.set_page_config(page_title="Genie", layout="wide", page_icon="✨")

# --- Custom CSS ---
st.markdown("""
    <style>
        html, body, .stApp {
            background-color: #1E1E2F;
            color: #F5F5F5;
        }
        input, .stTextInput > div > div > input,
        .stSelectbox > div > div,
        .stMultiselect > div > div {
            color: #F5F5F5 !important;
            background-color: #2C2C3A !important;
        }
        ::placeholder {
            color: #F5F5F5 !important;
            opacity: 0.6 !important;
        }
        label, .stMarkdown {
            color: #FFFFFF !important;
            font-weight: 700 !important;
            font-size: 16px !important;
        }
    </style>
""", unsafe_allow_html=True)

# --- App Title ---
st.title("✨ Genie - Natural Language to SQL")
st.markdown("_Select tables, ask questions, and visualize instantly!_ 🧠")

# --- Session State ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

# --- Login/Register UI ---
def login_section():
    st.subheader("🔐 Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if validate_user(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success(f"✅ Welcome back, {username}!")
        else:
            st.error("❌ Invalid credentials. Please try again.")

def register_section():
    st.subheader("📝 Register")
    username = st.text_input("New Username")
    email = st.text_input("Email")
    password = st.text_input("New Password", type="password")
    if st.button("Register"):
        success = register_user(username, email, password)
        if success:
            st.success("✅ Registration successful! Please login.")
        else:
            st.error("❌ Registration failed. Username may already exist.")

# --- Show login/register if not logged in ---
if not st.session_state.logged_in:
    option = st.radio("Choose action:", ("Login", "Register"))
    if option == "Login":
        login_section()
    else:
        register_section()
    st.stop()

# --- Main App UI after Login ---
schema = get_table_schema()
if not schema:
    st.error("❌ Could not fetch table schema.")
    st.stop()

table_options = list(schema.keys())
selected_tables = st.multiselect("📊 Select tables to use:", table_options)

if not selected_tables:
    st.warning("Please select at least one table to proceed.")
    st.stop()

st.markdown("### 🔍 Ask your Question")
user_question = st.text_input("Plain English question:", placeholder="e.g., Show month-wise app_tag_cost...")

chart_type = st.selectbox("📈 Choose chart type (optional):", ["None", "Bar", "Line", "Area", "Donut"])

# --- Schema Prompt Context ---
table_context = "Use the following table schemas only:\n\n"
for table in selected_tables:
    table_context += f"Table: {table}\nColumns:\n"
    for col in schema[table]:
        table_context += f"- {col}\n"
    table_context += "\n"
table_context += "Always use the exact table and column names from the above schema.\n"

# --- Query Generation + Execution ---
if user_question:
    with st.spinner("✨ Generating SQL query..."):
        prompt = f"""{table_context}
Convert the following natural language question to SQL for a PostgreSQL database.
Return only the SQL without any explanation.

Question: {user_question}
SQL:
"""
        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={"model": "mistral", "prompt": prompt, "stream": False}
            )
            if response.status_code == 200:
                sql_query = response.json()['response'].strip()
                st.code(sql_query, language='sql')
            else:
                st.error(f"❌ Failed to generate SQL: {response.text}")
                st.stop()
        except Exception as e:
            st.error(f"❌ Ollama error: {str(e)}")
            st.stop()

        # --- Run Query ---
        try:
            columns, rows = run_query(sql_query)
            if columns:
                df = pd.DataFrame(rows, columns=columns)

                st.subheader("📄 Query Result")
                st.dataframe(df, use_container_width=True)

                # Save user query to DB
                save_query_history(st.session_state.username, user_question, sql_query)

                if chart_type != "None":
                    st.subheader(f"📊 {chart_type} Chart")
                    if len(df.columns) < 2:
                        st.warning("Need at least 2 columns to plot chart.")
                    else:
                        x_col, y_col = df.columns[0], df.columns[1]

                        chart = None
                        if chart_type == "Bar":
                            chart = alt.Chart(df).mark_bar().encode(x=x_col, y=y_col)
                        elif chart_type == "Line":
                            chart = alt.Chart(df).mark_line().encode(x=x_col, y=y_col)
                        elif chart_type == "Area":
                            chart = alt.Chart(df).mark_area().encode(x=x_col, y=y_col)
                        elif chart_type == "Donut":
                            chart = alt.Chart(df).mark_arc(innerRadius=60).encode(
                                theta=alt.Theta(field=y_col, type="quantitative"),
                                color=alt.Color(field=x_col, type="nominal"),
                                tooltip=[x_col, y_col]
                            ).properties(width=250, height=250)

                        if chart:
                            st.altair_chart(chart, use_container_width=True)
            else:
                st.error("❌ No data returned from query.")
        except Exception as e:
            st.error(f"❌ Query Execution Error: {str(e)}")

# --- Query History ---
st.markdown("### 📜 Your Query History")
history = get_user_history(st.session_state.username)
if history:
    for h in history:
        st.markdown(f"- 🧠 **Q:** {h['question']}  \n💾 **SQL:** `{h['query']}`")
else:
    st.info("No previous queries yet.")
