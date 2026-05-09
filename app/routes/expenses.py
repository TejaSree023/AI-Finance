from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models.expense import Expense
from datetime import datetime
import pandas as pd

expenses = Blueprint('expenses', __name__)

CATEGORIES = [
    'Food', 'Travel', 'Shopping', 'Education', 'Entertainment',
    'Bills', 'Health', 'Investments', 'Others'
]

@expenses.route('/list')
@login_required
def list_expenses():
    page = request.args.get('page', 1, type=int)
    category_filter = request.args.get('category')
    
    query = Expense.query.filter_by(user_id=current_user.id)
    
    if category_filter and category_filter in CATEGORIES:
        query = query.filter_by(category=category_filter)
        
    expenses_pagination = query.order_by(Expense.date.desc()).paginate(page=page, per_page=10)
    
    return render_template('expenses/list.html', 
                           expenses=expenses_pagination, 
                           categories=CATEGORIES,
                           current_category=category_filter,
                           title='Expense History')

@expenses.route('/add', methods=['GET', 'POST'])
@login_required
def add_expense():
    if request.method == 'POST':
        amount = request.form.get('amount')
        category = request.form.get('category')
        description = request.form.get('description')
        date_str = request.form.get('date')
        
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError("Amount must be positive")
            
            date_obj = datetime.strptime(date_str, '%Y-%m-%d') if date_str else datetime.utcnow()
            
            expense = Expense(
                amount=amount, 
                category=category, 
                description=description, 
                date=date_obj,
                user_id=current_user.id
            )
            db.session.add(expense)
            db.session.commit()
            flash('Expense added successfully!', 'success')
            return redirect(url_for('expenses.list_expenses'))
        except Exception as e:
            flash(f'Error adding expense: {str(e)}', 'danger')
            
    return render_template('expenses/add.html', categories=CATEGORIES, title='Add Expense', legend='Add Expense')

@expenses.route('/edit/<int:expense_id>', methods=['GET', 'POST'])
@login_required
def edit_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    if expense.user_id != current_user.id:
        flash('Unauthorized action.', 'danger')
        return redirect(url_for('expenses.list_expenses'))
        
    if request.method == 'POST':
        try:
            expense.amount = float(request.form.get('amount'))
            expense.category = request.form.get('category')
            expense.description = request.form.get('description')
            date_str = request.form.get('date')
            if date_str:
                expense.date = datetime.strptime(date_str, '%Y-%m-%d')
            db.session.commit()
            flash('Expense updated!', 'success')
            return redirect(url_for('expenses.list_expenses'))
        except Exception as e:
            flash(f'Error updating expense: {str(e)}', 'danger')
            
    return render_template('expenses/add.html', 
                           expense=expense, 
                           categories=CATEGORIES, 
                           title='Edit Expense',
                           legend='Edit Expense')

@expenses.route('/delete/<int:expense_id>', methods=['POST'])
@login_required
def delete_expense(expense_id):
    expense = Expense.query.get_or_404(expense_id)
    if expense.user_id != current_user.id:
        flash('Unauthorized action.', 'danger')
        return redirect(url_for('expenses.list_expenses'))
        
    db.session.delete(expense)
    db.session.commit()
    flash('Expense deleted.', 'success')
    return redirect(url_for('expenses.list_expenses'))

from app.services.analytics import get_expenses_df, generate_insights, get_category_distribution, get_monthly_trend
from app.services.ml_models import predict_next_month_expenses, detect_anomalies

@expenses.route('/analytics')
@login_required
def analytics():
    user_expenses = Expense.query.filter_by(user_id=current_user.id).all()
    df = get_expenses_df(user_expenses)
    
    if df.empty:
        flash('Not enough data for analytics. Add some expenses first.', 'info')
        return redirect(url_for('expenses.list_expenses'))
        
    # Get basic insights
    insights = generate_insights(df, current_user.monthly_budget)
    
    # Get chart data
    category_data = get_category_distribution(df)
    monthly_data = get_monthly_trend(df)
    
    # ML Features
    df['month_year'] = df['date'].dt.to_period('M').astype(str) # ensure month_year exists for prediction
    predicted_expense, ml_msg = predict_next_month_expenses(df)
    anomalies = detect_anomalies(df)
    
    return render_template('expenses/analytics.html', 
                           title='Smart Analytics',
                           insights=insights,
                           category_labels=category_data['labels'],
                           category_values=category_data['data'],
                           trend_labels=monthly_data['labels'],
                           trend_values=monthly_data['data'],
                           predicted_expense=predicted_expense,
                           ml_msg=ml_msg,
                           anomalies=anomalies)

import io
import csv
from flask import make_response

@expenses.route('/export/csv')
@login_required
def export_csv():
    user_expenses = Expense.query.filter_by(user_id=current_user.id).order_by(Expense.date.desc()).all()
    
    si = io.StringIO()
    cw = csv.writer(si)
    cw.writerow(['Date', 'Category', 'Description', 'Amount'])
    
    for e in user_expenses:
        cw.writerow([e.date.strftime('%Y-%m-%d'), e.category, e.description or '', f"{e.amount:.2f}"])
        
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=expenses_export.csv"
    output.headers["Content-type"] = "text/csv"
    return output

@expenses.route('/export/pdf')
@login_required
def export_pdf():
    from weasyprint import HTML
    
    user_expenses = Expense.query.filter_by(user_id=current_user.id).order_by(Expense.date.desc()).all()
    
    html_out = render_template('expenses/report_pdf.html', expenses=user_expenses, title="Expense Report")
    
    pdf = HTML(string=html_out).write_pdf()
    
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=expense_report.pdf'
    return response
