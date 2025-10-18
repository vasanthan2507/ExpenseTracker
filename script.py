
# Create comprehensive data structure for the Django AI Expense Tracker project
# This will be used for the app generation

project_data = {
    "project_name": "AI Expense Tracker",
    "description": "Smart expense tracking system with AI-powered predictions and Aadhar-based authentication",
    
    "features": [
        "User Registration & Login with Aadhar verification",
        "Duplicate prevention via Aadhar number",
        "Expense input with category selection",
        "Visual expense representation (bar charts, flow charts)",
        "AI-powered expense prediction using financial news",
        "Responsive Bootstrap design",
        "SQLite database backend"
    ],
    
    "pages": [
        {
            "name": "Home Page",
            "route": "/",
            "description": "Landing page with project overview, features, and call-to-action"
        },
        {
            "name": "Register",
            "route": "/register",
            "description": "User registration with Aadhar validation"
        },
        {
            "name": "Login",
            "route": "/login",
            "description": "User authentication page"
        },
        {
            "name": "Dashboard",
            "route": "/dashboard",
            "description": "Main dashboard showing expense summary"
        },
        {
            "name": "Add Expense",
            "route": "/add-expense",
            "description": "Form to input new expenses with categories"
        },
        {
            "name": "View Expenses",
            "route": "/expenses",
            "description": "Display expenses with charts and category breakdown"
        },
        {
            "name": "AI Prediction",
            "route": "/ai-prediction",
            "description": "AI-generated future expense predictions based on news data"
        }
    ],
    
    "database_models": {
        "User": {
            "fields": [
                "id (Primary Key, Auto)",
                "username (CharField, unique)",
                "email (EmailField, unique)",
                "password (CharField, hashed)",
                "aadhar_number (CharField, unique, 12 digits)",
                "created_at (DateTimeField)",
                "updated_at (DateTimeField)"
            ]
        },
        "ExpenseCategory": {
            "fields": [
                "id (Primary Key, Auto)",
                "name (CharField)",
                "description (TextField)",
                "icon (CharField)",
                "created_at (DateTimeField)"
            ],
            "default_categories": ["Food", "Transportation", "Entertainment", "Healthcare", "Utilities", "Education", "Shopping", "Other"]
        },
        "Expense": {
            "fields": [
                "id (Primary Key, Auto)",
                "user (ForeignKey to User)",
                "category (ForeignKey to ExpenseCategory)",
                "amount (DecimalField)",
                "description (TextField)",
                "date (DateField)",
                "created_at (DateTimeField)"
            ]
        },
        "AIPrediction": {
            "fields": [
                "id (Primary Key, Auto)",
                "user (ForeignKey to User)",
                "prediction_month (CharField)",
                "predicted_amount (DecimalField)",
                "confidence_score (FloatField)",
                "news_sources (TextField)",
                "created_at (DateTimeField)"
            ]
        }
    },
    
    "technologies": {
        "backend": "Django (Python)",
        "frontend": "HTML, CSS, Bootstrap 5, JavaScript",
        "database": "SQLite",
        "charts": "Chart.js",
        "ai_ml": "LSTM Neural Networks (conceptual)",
        "validation": "Aadhar regex validation"
    },
    
    "aadhar_validation": {
        "pattern": "^[2-9]{1}[0-9]{3}\\s[0-9]{4}\\s[0-9]{4}$",
        "description": "12 digits with spaces after every 4 digits, not starting with 0 or 1"
    }
}

# Save project structure
print("PROJECT STRUCTURE FOR AI EXPENSE TRACKER")
print("="*60)
print(f"\nProject: {project_data['project_name']}")
print(f"Description: {project_data['description']}")

print("\n\nKEY FEATURES:")
for i, feature in enumerate(project_data['features'], 1):
    print(f"{i}. {feature}")

print("\n\nPAGES:")
for page in project_data['pages']:
    print(f"\n{page['name']} ({page['route']})")
    print(f"  - {page['description']}")

print("\n\nDATABASE MODELS:")
for model, details in project_data['database_models'].items():
    print(f"\n{model}:")
    for field in details['fields']:
        print(f"  - {field}")

print("\n\nTECH STACK:")
for key, value in project_data['technologies'].items():
    print(f"  {key}: {value}")

print("\n\n✓ Project data prepared successfully!")
