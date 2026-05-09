import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import IsolationForest
import warnings
warnings.filterwarnings('ignore')

def predict_next_month_expenses(df):
    """Predict next month's total expenses using simple Linear Regression"""
    if df.empty or len(df['month_year'].unique()) < 3:
        return None, "Need at least 3 months of data for prediction."
        
    # Group by month
    monthly_data = df.groupby('month_year')['amount'].sum().reset_index()
    monthly_data = monthly_data.sort_values('month_year')
    
    # Simple time index
    X = np.arange(len(monthly_data)).reshape(-1, 1)
    y = monthly_data['amount'].values
    
    model = LinearRegression()
    model.fit(X, y)
    
    # Predict next month (index = len(monthly_data))
    next_index = np.array([[len(monthly_data)]])
    prediction = model.predict(next_index)[0]
    
    return max(0, prediction), None # Ensure no negative predictions

def detect_anomalies(df):
    """Detect unusual spending behavior using Isolation Forest"""
    if df.empty or len(df) < 10:
        return []
        
    # We will look for anomalies in amounts
    X = df[['amount']].values
    
    # Contamination is the expected proportion of outliers (e.g., 5%)
    model = IsolationForest(contamination=0.05, random_state=42)
    model.fit(X)
    
    # Predict anomalies (-1 for outlier, 1 for inlier)
    predictions = model.predict(X)
    
    # Get outlier rows
    df['is_anomaly'] = predictions
    anomalies_df = df[df['is_anomaly'] == -1]
    
    anomalies = []
    for _, row in anomalies_df.iterrows():
        anomalies.append({
            'date': row['date'].strftime('%Y-%m-%d'),
            'category': row['category'],
            'amount': row['amount']
        })
        
    return sorted(anomalies, key=lambda x: x['amount'], reverse=True)
