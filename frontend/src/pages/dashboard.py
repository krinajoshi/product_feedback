import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import numpy as np

# Reuse the styling from main.py
st.set_page_config(
    page_title="Product Feedback Dashboard",
    page_icon="📊",
    layout="centered"
)

# Import the same CSS styling from main.py
st.markdown("""
    <style>
    /* Add all your CSS from main.py here */
    :root {
        --uottawa-garnet: #8f001a;
        --uottawa-grey: #2d2d2d;
        --uottawa-light-grey: #f8f9fa;
        --uottawa-white: #ffffff;
    }
    
    .feedback-header {
        color: var(--uottawa-garnet);
        font-size: 2.5rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 1.5em;
        line-height: 1.2;
    }
    
    /* Add other CSS styles from main.py */
    </style>
""", unsafe_allow_html=True)

def load_feedback_data():
    try:
        # In production, replace this with your actual data loading logic
        with open('feedback_data.json', 'r') as f:
            data = json.load(f)
        return pd.DataFrame(data)
    except FileNotFoundError:
        # Return sample data if no file exists
        return create_sample_data()

def create_sample_data():
    # Create sample data for testing
    dates = pd.date_range(start='2024-01-01', end='2024-01-14', freq='D')
    sample_data = []
    
    for date in dates:
        for _ in range(3):  # 3 entries per day
            sample_data.append({
                'timestamp': date.strftime('%Y-%m-%d'),
               'feedback_type': np.random.choice(['Satisfaction', 'Feature', 'Bug', 'Process Feedback', 'General']),
                'sentiment': np.random.choice(['Positive', 'Neutral', 'Negative']),
                'sentiment_score': np.random.uniform(0, 1),
                'urgency': np.random.choice(['High', 'Medium', 'Low']),
                'product_name': np.random.choice(['Product A', 'Product B', 'Product C']),
                'user_role': np.random.choice(['End User', 'Developer', 'Product Manager', 'Stakeholder'])

            })
    
    return pd.DataFrame(sample_data)

def create_feedback_trends(df):
    st.subheader("Feedback Trends")
    
    # Group feedback by date and type
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    feedback_by_date = df.groupby([df['timestamp'].dt.date, 'feedback_type']).size().unstack(fill_value=0)
    
    fig = px.line(feedback_by_date, 
                  title='Feedback Volume Over Time',
                  labels={'value': 'Number of Feedback', 'date': 'Date'},
                  height=400)
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font={'color': '#2d2d2d'}
    )
    st.plotly_chart(fig, use_container_width=True)

def create_sentiment_analysis(df):
    st.subheader("Sentiment Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        sentiment_dist = df['sentiment'].value_counts()
        fig = px.pie(values=sentiment_dist.values,
                    names=sentiment_dist.index,
                    title='Sentiment Distribution',
                    height=300)
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font={'color': '#2d2d2d'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        sentiment_by_type = pd.crosstab(df['feedback_type'], df['sentiment'])
        fig = px.bar(sentiment_by_type,
                    title='Sentiment by Feedback Type',
                    height=300)
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font={'color': '#2d2d2d'}
        )
        st.plotly_chart(fig, use_container_width=True)

def create_product_metrics(df):
    st.subheader("Product Metrics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_feedback = len(df)
        st.metric("Total Feedback", total_feedback)
    
    with col2:
        avg_sentiment = (df['sentiment'] == 'Positive').mean() * 100
        st.metric("Positive Sentiment", f"{avg_sentiment:.1f}%")
    
    with col3:
        feature_requests = len(df[df['feedback_type'] == 'Feature'])
        st.metric("Feature Requests", feature_requests)

def create_feedback_table(df):
    st.subheader("Recent Feedback")
    
    # Create a more detailed view of recent feedback
    recent_feedback = df.sort_values('timestamp', ascending=False).head(10)
    
    # Format the DataFrame for display
    display_df = recent_feedback[[
        'timestamp', 'feedback_type', 'sentiment', 
        'product_name', 'user_role'
    ]].copy()
    
    st.dataframe(
        display_df,
        column_config={
            "timestamp": "Date",
            "feedback_type": "Type",
            "sentiment": "Sentiment",
            "product_name": "Product",
            "user_role": "User Role"
        },
        hide_index=True,
        use_container_width=True
    )

def main():
    # Header
    st.markdown('<h1 class="feedback-header">Product Feedback Dashboard</h1>', unsafe_allow_html=True)
    
    # Load data
    df = load_feedback_data()
    
    # Add filters in sidebar
    st.sidebar.header("Filters")
    
    # Date filter
    date_range = st.sidebar.date_input(
        "Select Date Range",
        value=(
            datetime.now() - timedelta(days=30),
            datetime.now()
        )
    )
    
    # Product filter
    selected_products = st.sidebar.multiselect(
        "Select Products",
        options=df['product_name'].unique(),
        default=df['product_name'].unique()
    )
    
    # Filter data
    mask = (
        (pd.to_datetime(df['timestamp']).dt.date >= date_range[0]) &
        (pd.to_datetime(df['timestamp']).dt.date <= date_range[1]) &
        (df['product_name'].isin(selected_products))
    )
    filtered_df = df[mask]
    
    # Display metrics and charts
    create_product_metrics(filtered_df)
    
    # Create two columns for charts
    create_feedback_trends(filtered_df)
    create_sentiment_analysis(filtered_df)
    create_feedback_table(filtered_df)

if __name__ == "__main__":
    main()