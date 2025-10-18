AI Expense Tracker

A comprehensive expense tracking application powered by AI for future expense forecasting and Aadhar-based authentication. Built with Django, Python, Bootstrap 5, JavaScript, and Chart.js.

Features

Aadhar-based registration and login prevents duplicate accounts and validates users with India's government ID.
Secure authentication techniques are used, including password hashing, session management, and CSRF protection.
You can add, edit, delete, and categorize expenses, and also upload receipts for your records.
Your expenses are presented with analytics and visualization through interactive bar, pie, and line charts using Chart.js.
The built-in AI can forecast next month’s expenses using your history and simulated financial news.
The application is designed with Bootstrap 5 for a modern, responsive, mobile-friendly UI.

Project Structure

The folder structure is as follows:
ai-expense-tracker/
config/
apps/
  users/
  expenses/
  predictions/
templates/
static/
media/
requirements.txt
README.md
Setup Instructions

Clone the repository by running:
git clone https://github.com/yourusername/ai-expense-tracker.git
cd ai-expense-tracker

Create a virtual environment:
python -m venv venv
source venv/bin/activate
On Windows, use: venv\Scripts\activate

Install dependencies:
pip install -r requirements.txt

Configure your environment. Create a .env file with:
DEBUG=True
SECRET_KEY=your-django-secret-key
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1

Migrate your database:
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

Run the server:
python manage.py runserver
Then, open http://127.0.0.1:8000 in your browser

Aadhar Validation

The format should be: XXXX XXXX XXXX (12 digits, cannot start with 0 or 1). Regex for validation: ^[2-9]{1}[0-9]{3}\s[0-9]{4}\s[0-9]{4}$. The application enforces that only one account per Aadhar is possible.
AI Prediction Algorithm
The application collects your last 3–6 months of expenses by category, applies statistical analysis and news sentiment simulation, and predicts next month’s expenses for each category. You will also be shown a confidence score for the prediction and recommendations.

Visualizations

The application features:
A bar chart for expenses by category;
A line chart for expense trends;
A pie chart for category distribution.

Testing

You can run the tests using:
python manage.py test
This covers authentication, expense logic, forms, permissions, and the prediction calculation.

Contributing

Fork the repo.
Create your feature branch (git checkout -b feature/AmazingFeature).
Commit your changes (git commit -m 'feat: add AmazingFeature').
Push to the branch (git push origin feature/AmazingFeature).
Open a Pull Request.

License

MIT License

Author

Your Name
GitHub: https://github.com/vasanthan2507
LinkedIn: https://linkedin.com/in/vasanthan-dev

Star this repo if you like it!

Quick Start

Commands to get started:
git clone https://github.com/vasanthan2507/ExpenseTracker.git
cd ai-expense-tracker
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

Ready to manage expenses with intelligence and insight!
