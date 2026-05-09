from app import create_app, db, bcrypt
from app.models.user import User
from app.models.expense import Expense
from datetime import datetime, timedelta
import random

def seed_database():
    app = create_app()
    with app.app_context():
        # Drop all tables and recreate them to ensure a clean slate
        db.drop_all()
        db.create_all()

        print("Seeding database...")

        # Create a test user
        hashed_password = bcrypt.generate_password_hash('password123').decode('utf-8')
        user = User(username='testuser', email='test@example.com', password_hash=hashed_password, monthly_budget=50000)
        db.session.add(user)
        db.session.commit()

        print(f"Created user: {user.username} with password: password123")

        categories = ['Food', 'Travel', 'Shopping', 'Education', 'Entertainment', 'Bills', 'Health', 'Investments', 'Others']
        
        # Generate data for the last 6 months
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=180)
        
        expenses = []
        current_date = start_date
        
        while current_date <= end_date:
            # Generate 1 to 4 expenses per day
            num_expenses = random.randint(1, 4)
            for _ in range(num_expenses):
                category = random.choice(categories)
                
                # Base amounts vary by category
                if category == 'Bills':
                    amount = random.uniform(1000, 5000)
                elif category == 'Investments':
                    amount = random.uniform(5000, 15000)
                elif category == 'Food':
                    amount = random.uniform(200, 1500)
                elif category == 'Travel':
                    amount = random.uniform(100, 800)
                else:
                    amount = random.uniform(500, 3000)
                    
                # Occasionally inject an anomaly (very high expense)
                if random.random() < 0.02:  # 2% chance
                    amount *= random.uniform(5, 10)
                    print(f"Injected anomaly: {category} for Rs.{amount:.2f} on {current_date.strftime('%Y-%m-%d')}")
                    
                expense = Expense(
                    amount=amount,
                    category=category,
                    description=f"Sample {category} expense",
                    date=current_date,
                    user_id=user.id
                )
                expenses.append(expense)
                
            current_date += timedelta(days=1)
            
        db.session.bulk_save_objects(expenses)
        db.session.commit()
        
        print(f"Successfully added {len(expenses)} expenses for {user.username}.")

if __name__ == '__main__':
    seed_database()
