import pandas as pd
from datetime import datetime, timedelta

def get_expenses_df(expenses):
    """Convert list of Expense objects to Pandas DataFrame"""
    if not expenses:
        return pd.DataFrame()
        
    data = [{
        'id': e.id,
        'amount': e.amount,
        'category': e.category,
        'date': e.date,
        'month': e.date.month,
        'year': e.date.year
    } for e in expenses]
    
    df = pd.DataFrame(data)
    df['date'] = pd.to_datetime(df['date'])
    return df

def generate_insights(df, budget):
    """Generate textual insights based on expense data"""
    insights = []
    
    if df.empty:
        return ["Not enough data to generate insights. Add some expenses!"]
        
    current_month = datetime.utcnow().month
    current_year = datetime.utcnow().year
    
    # Filter for current month
    curr_month_df = df[(df['month'] == current_month) & (df['year'] == current_year)]
    total_curr_month = curr_month_df['amount'].sum()
    
    if total_curr_month > budget * 0.9:
        insights.append(f"Warning: You have used {total_curr_month/budget*100:.1f}% of your monthly budget (₹{budget}).")
    elif total_curr_month > budget * 0.7:
        insights.append(f"Notice: You have used {total_curr_month/budget*100:.1f}% of your monthly budget.")
        
    # Pacing and predictive insights
    import calendar
    _, total_days_in_month = calendar.monthrange(current_year, current_month)
    days_passed = datetime.utcnow().day
    
    if days_passed > 0 and total_curr_month > 0:
        daily_average = total_curr_month / days_passed
        projected_spend = daily_average * total_days_in_month
        
        if projected_spend > budget:
            days_until_empty = budget / daily_average if daily_average > 0 else 0
            days_early = total_days_in_month - days_until_empty
            if days_early > 0:
                insights.append(f"At your current spending rate, your budget may finish {int(days_early)} days early.")
        else:
            savings = budget - projected_spend
            insights.append(f"Great pacing! You are on track to save ₹{savings:.2f} this month.")
            
    # Check highest category
    if not curr_month_df.empty:
        cat_grouped = curr_month_df.groupby('category')['amount'].sum()
        highest_cat = cat_grouped.idxmax()
        highest_amt = cat_grouped.max()
        
        insights.append(f"Your highest spending category this month is {highest_cat} (₹{highest_amt:.2f}).")
        
    # Compare with last month
    last_month = current_month - 1 if current_month > 1 else 12
    last_year = current_year if current_month > 1 else current_year - 1
    
    last_month_df = df[(df['month'] == last_month) & (df['year'] == last_year)]
    total_last_month = last_month_df['amount'].sum()
    
    if total_last_month > 0:
        pct_change = ((total_curr_month - total_last_month) / total_last_month) * 100
        if pct_change > 0:
            insights.append(f"Your spending increased by {pct_change:.1f}% compared to last month.")
        else:
            insights.append(f"Great job! Your spending decreased by {abs(pct_change):.1f}% compared to last month.")

    return insights

def get_category_distribution(df):
    """Return data for Pie Chart"""
    if df.empty:
        return {'labels': [], 'data': []}
        
    grouped = df.groupby('category')['amount'].sum().reset_index()
    return {
        'labels': grouped['category'].tolist(),
        'data': grouped['amount'].tolist()
    }

def get_monthly_trend(df):
    """Return data for Bar/Line Chart showing monthly totals"""
    if df.empty:
        return {'labels': [], 'data': []}
        
    # Format date as YYYY-MM
    df['month_year'] = df['date'].dt.to_period('M').astype(str)
    grouped = df.groupby('month_year')['amount'].sum().reset_index()
    
    # Sort chronologically
    grouped = grouped.sort_values('month_year')
    
    return {
        'labels': grouped['month_year'].tolist(),
        'data': grouped['amount'].tolist()
    }
