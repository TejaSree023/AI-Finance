from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models.expense import Expense
from app import db
from datetime import datetime, timedelta
from sqlalchemy import func

main = Blueprint('main', __name__)

from app.services.analytics import get_expenses_df, get_category_distribution, get_monthly_trend
from app.services.ml_models import detect_anomalies
import calendar

@main.route('/')
def index():
    if not current_user.is_authenticated:
        return render_template('dashboard/landing.html', title='Welcome')

    # Calculate statistics for the dashboard
    now = datetime.utcnow()
    first_day_of_month = datetime(now.year, now.month, 1)
    
    # Days in current month
    _, total_days_in_month = calendar.monthrange(now.year, now.month)
    days_passed = now.day
    days_left = total_days_in_month - days_passed
    # If today is the last day, avoid division by zero
    days_left = max(1, days_left)

    # All-time total
    total_expenses = db.session.query(func.sum(Expense.amount)).filter_by(user_id=current_user.id).scalar() or 0
    
    # Monthly total
    monthly_expenses = db.session.query(func.sum(Expense.amount)).filter(
        Expense.user_id == current_user.id,
        Expense.date >= first_day_of_month
    ).scalar() or 0
    
    # Budget calculations
    budget = current_user.monthly_budget
    remaining_budget = budget - monthly_expenses
    budget_usage_pct = (monthly_expenses / budget * 100) if budget > 0 else 0
    
    # Health Status
    if budget_usage_pct < 70:
        health_status = 'green'
        health_color_class = 'bg-success'
        health_text = 'Healthy'
    elif budget_usage_pct <= 90:
        health_status = 'yellow'
        health_color_class = 'bg-warning'
        health_text = 'Warning'
    else:
        health_status = 'red'
        health_color_class = 'bg-danger'
        health_text = 'Danger'
        
    # Daily Safe Limit
    daily_safe_limit = remaining_budget / days_left if remaining_budget > 0 else 0
    
    # Daily average this month
    daily_average = monthly_expenses / days_passed if days_passed > 0 else 0
    
    # Predicted end of month spend (Simple linear projection)
    projected_spend = daily_average * total_days_in_month
    
    # Highest category this month
    highest_category = db.session.query(Expense.category, func.sum(Expense.amount).label('total'))\
        .filter(Expense.user_id == current_user.id, Expense.date >= first_day_of_month)\
        .group_by(Expense.category)\
        .order_by(db.desc('total')).first()
        
    highest_category_name = highest_category.category if highest_category else "N/A"
    
    # Recent transactions
    recent_transactions = Expense.query.filter_by(user_id=current_user.id)\
        .order_by(Expense.date.desc()).limit(5).all()

    # Data for charts and ML on dashboard
    user_expenses = Expense.query.filter_by(user_id=current_user.id).all()
    df = get_expenses_df(user_expenses)
    
    category_data = {'labels': [], 'data': []}
    trend_data = {'labels': [], 'data': []}
    anomalies = []
    
    if not df.empty:
        # Filter df for current month for category pie chart
        curr_month_df = df[(df['date'].dt.month == now.month) & (df['date'].dt.year == now.year)]
        category_data = get_category_distribution(curr_month_df)
        
        # Monthly trend
        trend_data = get_monthly_trend(df)
        
        # Anomalies
        anomalies = detect_anomalies(df)
        # Limit anomalies to top 3 on dashboard
        anomalies = anomalies[:3] if anomalies else []

    return render_template('dashboard/index.html', 
                           title='Dashboard',
                           total_expenses=total_expenses,
                           monthly_expenses=monthly_expenses,
                           remaining_budget=remaining_budget,
                           budget_usage_pct=min(100, budget_usage_pct), # Cap at 100 for progress bar
                           health_color_class=health_color_class,
                           health_text=health_text,
                           daily_safe_limit=daily_safe_limit,
                           days_left=days_left,
                           projected_spend=projected_spend,
                           highest_category=highest_category_name,
                           daily_average=daily_average,
                           recent_transactions=recent_transactions,
                           category_labels=category_data['labels'],
                           category_values=category_data['data'],
                           trend_labels=trend_data['labels'][-6:], # Last 6 months
                           trend_values=trend_data['data'][-6:],
                           anomalies=anomalies)

from flask import request, flash, redirect, url_for

@main.route('/update_budget', methods=['POST'])
@login_required
def update_budget():
    new_budget = request.form.get('budget')
    try:
        new_budget = float(new_budget)
        if new_budget < 0:
            raise ValueError
        current_user.monthly_budget = new_budget
        db.session.commit()
        flash('Monthly budget updated successfully!', 'success')
    except ValueError:
        flash('Invalid budget amount.', 'danger')
    return redirect(url_for('main.index'))
