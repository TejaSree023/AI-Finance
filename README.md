# AI-Powered Personal Finance Analyzer

A production-ready full-stack web application for intelligent personal finance management, predictive budgeting, and automated spending analytics using Machine Learning.

## Features

- **Robust Authentication**: Secure user registration, login, and session management using Flask-Login and Bcrypt.
- **Expense Tracking**: Complete CRUD operations for daily expenses with categorization.
- **Smart Analytics Dashboard**: Beautiful UI built with Bootstrap 5 and interactive charts via Chart.js.
- **Machine Learning Integrations (Scikit-Learn & Pandas)**:
  - **Expense Prediction**: Predicts your next month's spending based on historical data using Linear Regression.
  - **Anomaly Detection**: Flags unusual spending behavior or abnormally high transactions using Isolation Forest.
  - **Automated Insights**: Generates smart text-based insights comparing month-over-month expenditure.
- **Export Capabilities**: Download expense history as CSV or PDF.

## Tech Stack

- **Backend**: Python, Flask, Flask-SQLAlchemy, SQLite (Expandable to MySQL)
- **Data Science & ML**: Pandas, Scikit-learn, Numpy
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5, Chart.js
- **Other Utilities**: WeasyPrint (PDF Export), Flask-WTF

## Installation & Setup

1. **Clone the repository** (if applicable) and navigate to the project directory:
   ```bash
   cd Expense
   ```

2. **Create a virtual environment** and activate it:
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Seed the database** (Creates test user and 6 months of sample ML data):
   ```bash
   python seed_db.py
   ```
   *Login credentials after seeding: Username: `testuser`, Password: `password123` (or use the email `test@example.com`)*

5. **Run the application**:
   ```bash
   python run.py
   ```
   The app will run on `http://127.0.0.1:5000/`.

---
