# AI Expense Tracker - Complete Django Project

![Django](https://img.shields.io/badge/Django-5.0-green)
![Python](https://img.shields.io/badge/Python-3.11+-blue)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5-purple)
![License](https://img.shields.io/badge/License-MIT-yellow)

A sophisticated expense tracking web application with AI-powered predictions and Aadhar-based authentication, built using Django, Python, Bootstrap, and Chart.js.

---

## 🌟 Key Features

### ✅ **Aadhar-Based Authentication**
- **Unique user registration** using Aadhar number validation
- **Prevents duplicate registrations** - one person, one account
- **Secure format validation**: XXXX XXXX XXXX (12 digits, cannot start with 0 or 1)
- **Real-time validation** with pattern matching

### 💰 **Expense Management**
- **Add, view, edit, and delete expenses** with ease
- **8 pre-defined categories** with icons and color coding:
  - 🍴 Food
  - 🚗 Transportation
  - 🎬 Entertainment
  - ❤️ Healthcare
  - 💡 Utilities
  - 🎓 Education
  - 🛒 Shopping
  - ⋯ Other
- **Receipt image uploads** for record keeping
- **Date-wise expense tracking**

### 📊 **Visual Analytics**
- **Interactive Chart.js visualizations**:
  - Bar charts for category-wise expenses
  - Line charts for expense trends over time
  - Pie charts for category distribution
- **Real-time data updates**
- **Responsive and mobile-friendly charts**

### 🤖 **AI-Powered Predictions**
- **Machine learning-based expense forecasting**
- **Analyzes 3-6 months** of historical data
- **Financial news integration** for market sentiment analysis
- **Category-wise predictions**
- **Confidence scoring** based on data availability
- **Trend analysis** and seasonal pattern detection

### 🎨 **Modern UI/UX**
- **Bootstrap 5** responsive design
- **Mobile-first approach**
- **Professional color schemes**
- **Smooth animations and transitions**
- **Intuitive navigation**

---

## 🏗️ Project Architecture

### Technology Stack

| Layer | Technologies |
|-------|-------------|
| **Backend** | Django 5.0, Python 3.11+ |
| **Frontend** | HTML5, CSS3, Bootstrap 5, JavaScript |
| **Database** | SQLite (Development), PostgreSQL (Production) |
| **Charts** | Chart.js 4.x |
| **Authentication** | Django Auth + Custom Aadhar Validation |
| **AI/ML** | LSTM concepts, Statistical Analysis |
| **Icons** | Font Awesome 6 |

### Project Structure

```
ai-expense-tracker/
├── manage.py
├── requirements.txt
├── README.md
├── .env
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/
│   ├── users/          # Authentication & user management
│   ├── expenses/       # Expense CRUD operations
│   └── predictions/    # AI prediction engine
├── templates/
│   ├── base.html
│   ├── home.html
│   ├── users/
│   ├── expenses/
│   └── predictions/
├── static/
│   ├── css/
│   ├── js/
│   └── img/
└── media/
    └── receipts/
```

---

## 🚀 Installation Guide

### Prerequisites

- **Python 3.11+** installed
- **pip** package manager
- **Virtual environment** (recommended)
- **Git** for version control

### Step 1: Clone Repository

```bash
git clone https://github.com/yourusername/ai-expense-tracker.git
cd ai-expense-tracker
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Configure Environment

Create `.env` file in root directory:

```env
DEBUG=True
SECRET_KEY=your-django-secret-key-here
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Step 5: Database Setup

```bash
# Create database tables
python manage.py makemigrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser

# Load initial expense categories
python manage.py loaddata initial_categories.json
```

### Step 6: Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### Step 7: Run Development Server

```bash
python manage.py runserver
```

🎉 **Access the application at**: http://127.0.0.1:8000/

---

## 📱 Application Modules

### 1. Home Page
- Landing page with feature highlights
- Call-to-action buttons
- Responsive design

### 2. User Registration
- Aadhar validation
- Email verification
- Password strength checking
- Duplicate prevention

### 3. User Login
- Username/Email authentication
- Remember me functionality
- Session management

### 4. Dashboard
- Expense summary cards
- Recent transactions
- Quick action buttons
- Category-wise mini chart

### 5. Add Expense
- Category selection
- Amount input
- Description field
- Date picker
- Receipt upload

### 6. View Expenses
- Filterable expense list
- Date range filters
- Category filters
- Multiple chart visualizations
- Export functionality

### 7. AI Prediction
- Generate predictions button
- Category-wise forecasts
- Confidence scoring
- News sentiment analysis
- Historical prediction tracking

---

## 🗄️ Database Schema

### Users Table (CustomUser)
```sql
- id (Primary Key)
- username (Unique)
- email (Unique)
- password (Hashed)
- aadhar_number (Unique, 14 chars)
- created_at
- updated_at
```

### Expense Categories Table
```sql
- id (Primary Key)
- name (Unique)
- description
- icon (Font Awesome class)
- color (Hex code)
- is_active
- created_at
```

### Expenses Table
```sql
- id (Primary Key)
- user_id (Foreign Key → CustomUser)
- category_id (Foreign Key → ExpenseCategory)
- amount (Decimal 10,2)
- description (Text)
- date (Date)
- receipt_image (ImageField)
- created_at
- updated_at
```

### AI Predictions Table
```sql
- id (Primary Key)
- user_id (Foreign Key → CustomUser)
- prediction_month (YYYY-MM)
- predicted_amount (Decimal)
- confidence_score (Float 0-100)
- news_sources (JSON)
- category_breakdown (JSON)
- created_at
```

---

## 🤖 AI Prediction Algorithm

### How It Works

1. **Data Collection**
   - Fetches last 3-6 months of user expenses
   - Aggregates by category

2. **Statistical Analysis**
   - Calculates moving averages
   - Identifies spending trends
   - Detects seasonal patterns

3. **Prediction Generation**
   - Applies trend multipliers (5-15% growth)
   - Integrates news sentiment factors
   - Generates category-wise forecasts

4. **Confidence Scoring**
   ```python
   confidence = (data_availability * 0.6) + (variance_stability * 0.4)
   ```

5. **News Integration**
   - Analyzes financial news headlines
   - Applies sentiment-based adjustments
   - Considers economic indicators

---

## 🔒 Aadhar Validation System

### Validation Rules

- **Format**: `XXXX XXXX XXXX` (12 digits with spaces)
- **First digit**: Must be 2-9 (cannot be 0 or 1)
- **Regex Pattern**: `^[2-9]{1}[0-9]{3}\s[0-9]{4}\s[0-9]{4}$`

### Implementation

```python
def validate_aadhar(aadhar_number):
    pattern = r'^[2-9]{1}[0-9]{3}\s[0-9]{4}\s[0-9]{4}$'
    if not re.match(pattern, aadhar_number):
        raise ValidationError('Invalid Aadhar format')
    
    if CustomUser.objects.filter(aadhar_number=aadhar_number).exists():
        raise ValidationError('Aadhar already registered')
```

### Why Aadhar-Based Authentication?

- **Prevents duplicate accounts**: One person = One account
- **Enhanced security**: Government-verified identity
- **Data integrity**: Ensures authentic user base
- **Trust building**: Users know real identities

---

## 📊 Chart.js Implementation

### Bar Chart - Category Expenses
```javascript
new Chart(ctx, {
    type: 'bar',
    data: {
        labels: categoryNames,
        datasets: [{
            label: 'Amount Spent',
            data: categoryAmounts,
            backgroundColor: categoryColors
        }]
    }
});
```

### Line Chart - Expense Trends
```javascript
new Chart(ctx, {
    type: 'line',
    data: {
        labels: dates,
        datasets: [{
            label: 'Daily Expenses',
            data: amounts,
            borderColor: '#4A90E2',
            tension: 0.4
        }]
    }
});
```

### Pie Chart - Category Distribution
```javascript
new Chart(ctx, {
    type: 'pie',
    data: {
        labels: categoryNames,
        datasets: [{
            data: percentages,
            backgroundColor: categoryColors
        }]
    }
});
```

---

## 🧪 Testing

### Run Tests

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test apps.users
python manage.py test apps.expenses
python manage.py test apps.predictions

# With coverage
coverage run --source='.' manage.py test
coverage report
```

### Test Coverage

- User registration with Aadhar validation
- Login/logout functionality
- Expense CRUD operations
- Chart data generation
- AI prediction algorithms
- Form validations

---

## 🚢 Deployment

### Production Checklist

- [ ] Set `DEBUG = False` in settings
- [ ] Generate new `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set up PostgreSQL database
- [ ] Configure static files (WhiteNoise)
- [ ] Set up media file storage (AWS S3)
- [ ] Enable HTTPS
- [ ] Configure CORS if needed
- [ ] Set up monitoring (Sentry)
- [ ] Configure backups

### Deploy to Heroku

```bash
# Install Heroku CLI
heroku login
heroku create your-app-name

# Add PostgreSQL
heroku addons:create heroku-postgresql:hobby-dev

# Set environment variables
heroku config:set SECRET_KEY=your-secret-key
heroku config:set DEBUG=False

# Deploy
git push heroku main
heroku run python manage.py migrate
heroku run python manage.py createsuperuser
```

---

## 📚 API Documentation (Optional)

### Django REST Framework Integration

If you want to add API endpoints:

```bash
pip install djangorestframework
```

### Sample API Endpoints

- `GET /api/expenses/` - List all expenses
- `POST /api/expenses/` - Create new expense
- `GET /api/expenses/{id}/` - Get expense details
- `PUT /api/expenses/{id}/` - Update expense
- `DELETE /api/expenses/{id}/` - Delete expense
- `GET /api/predictions/` - Get AI predictions

---

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/AmazingFeature`
3. **Commit changes**: `git commit -m 'Add AmazingFeature'`
4. **Push to branch**: `git push origin feature/AmazingFeature`
5. **Open a Pull Request**

### Code Style

- Follow **PEP 8** for Python code
- Use **Black** for code formatting
- Write **docstrings** for functions
- Add **type hints** where applicable

---

## 🐛 Troubleshooting

### Common Issues

**1. Aadhar validation not working**
```python
# Check regex pattern in validators.py
pattern = r'^[2-9]{1}[0-9]{3}\s[0-9]{4}\s[0-9]{4}$'
```

**2. Charts not displaying**
```javascript
// Ensure Chart.js CDN is loaded
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
```

**3. Database migration errors**
```bash
python manage.py migrate --fake-initial
python manage.py migrate
```

**4. Static files not loading**
```bash
python manage.py collectstatic --clear
```

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- LinkedIn: [Your Profile](https://linkedin.com/in/yourprofile)
- Email: your.email@example.com

---

## 🙏 Acknowledgments

- **Django Framework** - Web framework
- **Bootstrap** - CSS framework
- **Chart.js** - Data visualization
- **Font Awesome** - Icons
- **Community contributors**

---

## 📞 Support

For support, email support@expensetracker.com or join our Slack channel.

---

## 🗺️ Roadmap

### Version 2.0 (Planned)

- [ ] Mobile app (React Native)
- [ ] Receipt OCR scanning
- [ ] Multi-currency support
- [ ] Budget alerts and notifications
- [ ] Recurring expense automation
- [ ] Export to PDF/Excel
- [ ] Bank account integration
- [ ] Advanced AI recommendations
- [ ] Social expense sharing
- [ ] Tax calculation helper

---

## 📸 Screenshots

### Home Page
![Home Page](screenshots/home.png)

### Dashboard
![Dashboard](screenshots/dashboard.png)

### Expense Charts
![Charts](screenshots/charts.png)

### AI Predictions
![AI Predictions](screenshots/predictions.png)

---

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=yourusername/ai-expense-tracker&type=Date)](https://star-history.com/#yourusername/ai-expense-tracker&Date)

---

**Made with ❤️ for better financial management**

---

## Quick Start Commands

```bash
# Clone and setup
git clone https://github.com/yourusername/ai-expense-tracker.git
cd ai-expense-tracker
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# Database setup
python manage.py migrate
python manage.py createsuperuser
python manage.py loaddata initial_categories.json

# Run server
python manage.py runserver
```

**That's it! Visit http://127.0.0.1:8000/ 🚀**
