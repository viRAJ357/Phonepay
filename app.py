import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
import joblib
import os

# Page configuration
st.set_page_config(page_title="PhonePe Pulse Analysis", page_icon="🏦", layout="wide")

# Custom CSS for Premium Look
st.markdown("""
    <style>
    .main {
        background-color: #f5f7f9;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        color: #0b0e14;
    }
    [data-testid="stMetricValue"] {
        color: #0b0e14 !important;
    }
    [data-testid="stMetricLabel"] {
        color: #555555 !important;
    }
    .stSidebar {
        background-color: #0b0e14;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# Database connection
def get_connection():
    return sqlite3.connect('phonepe_pulse.db')

def query_data(query):
    conn = get_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Load Model and Metadata
@st.cache_resource
def load_ml_assets():
    if os.path.exists('models/rf_model.joblib'):
        model = joblib.load('models/rf_model.joblib')
        le_state = joblib.load('models/le_state.joblib')
        le_type = joblib.load('models/le_type.joblib')
        metadata = joblib.load('models/metadata.joblib')
        return model, le_state, le_type, metadata
    return None, None, None, None

# Sidebar Navigation
st.sidebar.image("https://www.phonepe.com/pulse/static/7644265576bc97676759902660d0051e/logo.png", width=200)
st.sidebar.title("Pulse Explorer")
menu = ["🏠 Home", "🌍 Geo Analysis", "📊 Transaction Insights", "🤝 Insurance Analysis", "📱 User Comparison", "🏆 Top Performing", "🔮 Growth Predictions"]
choice = st.sidebar.radio("Navigate", menu)

if choice == "🏠 Home":
    st.title("PhonePe Pulse Data Visualization (2018 - 2024)")
    st.markdown("""
    Explore the digital payment revolution in India. This dashboard provides deep insights into how 
    transactions, users, and insurance patterns have evolved over the years.
    """)
    
    # Summary Metrics
    col1, col2, col3 = st.columns(3)
    
    total_tx_amount = query_data("SELECT SUM(Transaction_Amount) as total FROM aggregated_transaction")['total'][0]
    total_tx_count = query_data("SELECT SUM(Transaction_Count) as total FROM aggregated_transaction")['total'][0]
    total_users = query_data("SELECT SUM(RegisteredUsers) as total FROM map_user")['total'][0]
    
    col1.metric("Total Transaction Amount", f"₹ {total_tx_amount/1e12:.2f} T", "+15% YoY")
    col2.metric("Total Transactions", f"{total_tx_count/1e9:.2f} B", "+12% YoY")
    col3.metric("Registered Users", f"{total_users/1e6:.2f} M", "+18% YoY")
    
    st.image("https://www.phonepe.com/pulse/static/9d8ed2a1d3319808a38aeec37e5841e2/pulse-video-poster.png", use_container_width=True)

elif choice == "🌍 Geo Analysis":
    st.title("Geographical Analysis")
    
    col1, col2, col3 = st.columns(3)
    year = col1.selectbox("Year", [2018, 2019, 2020, 2021, 2022, 2023, 2024], index=6)
    quarter = col2.selectbox("Quarter", [1, 2, 3, 4], index=3)
    metric = col3.selectbox("Metric", ["Transaction Amount", "Transaction Count"])
    
    db_metric = "Transaction_Amount" if metric == "Transaction Amount" else "Transaction_Count"
    
    query = f"SELECT State, SUM({db_metric}) as Value FROM aggregated_transaction WHERE Year={year} AND Quarter={quarter} GROUP BY State"
    df = query_data(query)
    
    # State mapping for GeoJSON
    india_states_geojson = "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d1341404f8bbef7a347/raw/01c5a91d1ea44c207bb971032023ff2adeb3aa27/india_states.geojson"
    
    fig = px.choropleth(
        df,
        geojson=india_states_geojson,
        featureidkey='properties.ST_NM',
        locations='State',
        color='Value',
        color_continuous_scale='Viridis',
        title=f"Heatmap of {metric} in Q{quarter} {year}",
        template='plotly_white'
    )
    fig.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(fig, use_container_width=True)

elif choice == "📊 Transaction Insights":
    st.title("Transaction Trends & Highlights")
    
    # Yearly Trend
    query = "SELECT Year, SUM(Transaction_Amount) as Amount FROM aggregated_transaction GROUP BY Year"
    df_trend = query_data(query)
    fig_trend = px.line(df_trend, x='Year', y='Amount', title='Year-on-Year Transaction Amount Growth', markers=True)
    st.plotly_chart(fig_trend, use_container_width=True)
    
    # Type Breakdown
    col1, col2 = st.columns(2)
    
    query_type = "SELECT Transaction_Type, SUM(Transaction_Count) as Count FROM aggregated_transaction GROUP BY Transaction_Type"
    df_type = query_data(query_type)
    fig_type = px.pie(df_type, values='Count', names='Transaction_Type', title='Transaction Breakdown by Category', hole=0.4)
    col1.plotly_chart(fig_type, use_container_width=True)
    
    # State-wise Bar Chart
    query_state = "SELECT State, SUM(Transaction_Amount) as Amount FROM aggregated_transaction GROUP BY State ORDER BY Amount DESC"
    df_state = query_data(query_state)
    fig_state = px.bar(df_state.head(10), x='State', y='Amount', title='Top 10 States by Transaction Amount', color='Amount')
    col2.plotly_chart(fig_state, use_container_width=True)

elif choice == "🤝 Insurance Analysis":
    st.title("Insurance Penetration & Trends")
    st.info("Visualizing the growth of digital insurance purchases on PhonePe.")
    
    query = "SELECT Year, Insurance_Type, SUM(Transaction_Amount) as Amount FROM aggregated_insurance GROUP BY Year, Insurance_Type"
    df_ins = query_data(query)
    
    fig_ins = px.bar(df_ins, x='Year', y='Amount', color='Insurance_Type', barmode='group', title='Insurance Transaction Amount by Type')
    st.plotly_chart(fig_ins, use_container_width=True)

elif choice == "📱 User Comparison":
    st.title("Mobile Device Brand & User Demographics")
    
    state_list = query_data("SELECT DISTINCT State FROM aggregated_user")['State'].tolist()
    state = st.selectbox("Select State", state_list)
    
    query = f"SELECT Brand, SUM(Count) as Total_Users FROM aggregated_user WHERE State='{state}' GROUP BY Brand"
    df_user = query_data(query)
    
    fig_user = px.treemap(df_user, path=['Brand'], values='Total_Users', title=f"Device Brand Market Share in {state}")
    st.plotly_chart(fig_user, use_container_width=True)

elif choice == "🏆 Top Performing":
    st.title("Top Rankings (Quarterly Leaderboard)")
    
    col1, col2 = st.columns(2)
    view_type = col1.radio("View For", ["Districts", "States"])
    metric_type = col2.radio("Rank By", ["Transaction Amount", "Registered Users"])
    
    if view_type == "Districts":
        if metric_type == "Transaction Amount":
            query = "SELECT District, SUM(Transaction_Amount) as Value FROM top_transaction GROUP BY District ORDER BY Value DESC LIMIT 10"
        else:
            query = "SELECT District, SUM(RegisteredUsers) as Value FROM top_user GROUP BY District ORDER BY Value DESC LIMIT 10"
        label = "District"
    else:
        if metric_type == "Transaction Amount":
            query = "SELECT State, SUM(Transaction_Amount) as Value FROM aggregated_transaction GROUP BY State ORDER BY Value DESC LIMIT 10"
        else:
            query = "SELECT State, SUM(RegisteredUsers) as Value FROM map_user GROUP BY State ORDER BY Value DESC LIMIT 10"
        label = "State"
            
    df_top = query_data(query)
    fig_top = px.bar(df_top, x=label, y='Value', color='Value', title=f"Top 10 {view_type} by {metric_type}")
    st.plotly_chart(fig_top, use_container_width=True)

elif choice == "🔮 Growth Predictions":
    st.title("ML-Powered growth Forecasting")
    st.markdown("Predict future quarterly transaction amounts based on historical trends.")
    
    model, le_state, le_type, metadata = load_ml_assets()
    
    if model:
        with st.form("prediction_form"):
            col1, col2 = st.columns(2)
            p_state = col1.selectbox("Select State", metadata['states'])
            p_year = col2.number_input("Year", min_value=2024, max_value=2030, value=2025)
            p_quarter = col1.selectbox("Quarter", [1, 2, 3, 4])
            p_type = col2.selectbox("Transaction Type", metadata['types'])
            
            submit = st.form_submit_button("Forecast")
            
            if submit:
                # Encode inputs
                st_enc = le_state.transform([p_state])[0]
                ty_enc = le_type.transform([p_type])[0]
                
                input_data = pd.DataFrame({
                    'State_Encoded': [st_enc],
                    'Year': [p_year],
                    'Quarter': [p_quarter],
                    'Type_Encoded': [ty_enc]
                })
                
                prediction = model.predict(input_data)[0]
                
                st.subheader(f"Predicted Transaction Amount for {p_state} in Q{p_quarter} {p_year}")
                st.success(f"₹ {prediction:,.2f}")
                
                st.info("Note: Predictions are based on historical data using a Random Forest algorithm and should be used for informational purposes only.")
    else:
        st.warning("ML Model not found. Please run `scripts/train_model.py` to generate the predictive engine.")

st.sidebar.markdown("---")
st.sidebar.write("Developed by Nikhil Kumar")
st.sidebar.info("LabMentix Data Science Internship Project")
