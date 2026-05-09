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

## Resume & Placement Materials

### ATS-Friendly Resume Description

**Project Title:** AI-Powered Personal Finance Analyzer
**Technologies:** Python, Flask, Pandas, Scikit-learn, SQLite, Bootstrap 5, Chart.js
*   Architected and developed a full-stack SaaS-style personal finance application with a modular MVC architecture using Flask Blueprints and SQLAlchemy.
*   Implemented predictive analytics using Scikit-learn (`LinearRegression`) to forecast future monthly expenses, optimizing user budget planning by analyzing historical expenditure data.
*   Integrated anomaly detection (`IsolationForest`) to automatically flag unusual spending behaviors and prevent financial leakages.
*   Engineered a dynamic analytics engine using Pandas to generate automated, natural language insights comparing month-over-month financial trends.
*   Designed a responsive, production-ready frontend using Bootstrap 5 and customized CSS, featuring interactive data visualizations via Chart.js.
*   Built secure authentication flows and enabled robust data export functionality (CSV/PDF) for offline user reporting.

### Technical Interview Q&A

**Q1: Why did you use Flask instead of Django for this project?**
*Answer:* I chose Flask because of its micro-framework architecture, which provides fine-grained control over the components I wanted to integrate. Since this project heavily involved custom Machine Learning models (Scikit-learn) and Data Analysis (Pandas), Flask allowed me to build lightweight APIs and services around these data tools without the overhead of Django's built-in ORM and monolithic structure, though I did use SQLAlchemy for robust database management.

**Q2: How does the expense prediction model work?**
*Answer:* I implemented a Simple Linear Regression model using `scikit-learn`. The model groups the user's historical expenses by month using Pandas. It treats the chronological months as the independent variable (X) and the total monthly spending as the dependent variable (y). By fitting this historical data, the model can predict the expected spending for the upcoming month (`n+1`).

**Q3: Explain how you detected unusual spending (Anomalies).**
*Answer:* I used the `IsolationForest` algorithm from Scikit-learn. Unlike standard statistical methods (like Z-score) which assume a normal distribution, Isolation Forest works well with multi-dimensional and non-parametric data. It isolates anomalies by randomly selecting a feature and a split value. Outliers require fewer splits to be isolated compared to normal data points. I set the contamination rate to 5%, meaning the model flags the top 5% most unusual transactions based on the user's historical transaction amounts.

**Q4: How did you structure your application for scalability?**
*Answer:* I used Flask Blueprints to separate the application logic into distinct modules: `auth`, `main` (dashboard), and `expenses`. All database interactions are abstracted via SQLAlchemy models, and business logic (like ML and Pandas processing) is segregated into a dedicated `services/` directory. This separation of concerns ensures that as the application grows, new features can be added without tangling the core routing logic.

### Future Enhancements
*   **Bank API Integration:** Use Plaid or similar APIs to automatically fetch real-time bank transactions.
*   **Receipt Scanning:** Implement OCR (Optical Character Recognition) using Tesseract to automatically parse physical receipts.
*   **Advanced ML Models:** Transition from Linear Regression to an LSTM (Long Short-Term Memory) neural network for more accurate time-series expense forecasting.
*   **Multi-currency Support:** Add real-time currency conversion for international travelers.
