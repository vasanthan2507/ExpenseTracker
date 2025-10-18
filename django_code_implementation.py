# AI EXPENSE TRACKER - COMPLETE DJANGO CODE IMPLEMENTATION

## TABLE OF CONTENTS
1. Models Implementation
2. Views Implementation
3. Forms Implementation
4. URLs Configuration

================================================================================
## 1. MODELS IMPLEMENTATION
================================================================================

# apps/users/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
import re


class CustomUser(AbstractUser):
    """Extended user model with Aadhar authentication"""
    aadhar_number = models.CharField(
        max_length=14,
        unique=True,
        help_text="Format: XXXX XXXX XXXX (12 digits with spaces)"
    )
    phone_number = models.CharField(max_length=15, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ['-date_joined']

    def clean(self):
        """Validate Aadhar number format"""
        super().clean()
        pattern = r'^[2-9]{1}[0-9]{3}\s[0-9]{4}\s[0-9]{4}$'
        if not re.match(pattern, self.aadhar_number):
            raise ValidationError({
                'aadhar_number': 'Invalid Aadhar format. Must be XXXX XXXX XXXX (cannot start with 0 or 1)'
            })

    def __str__(self):
        return f"{self.username} ({self.aadhar_number})"


# apps/expenses/models.py
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
from decimal import Decimal


class ExpenseCategory(models.Model):
    """Pre-defined expense categories"""
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, help_text="Font Awesome icon class")
    color = models.CharField(max_length=7, help_text="Hex color code")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Expense Category"
        verbose_name_plural = "Expense Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class Expense(models.Model):
    """User expense records"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='expenses'
    )
    category = models.ForeignKey(
        ExpenseCategory,
        on_delete=models.PROTECT,
        related_name='expenses'
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    description = models.TextField()
    date = models.DateField()
    receipt_image = models.ImageField(
        upload_to='receipts/%Y/%m/',
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Expense"
        verbose_name_plural = "Expenses"
        ordering = ['-date', '-created_at']
        indexes = [
            models.Index(fields=['user', 'date']),
            models.Index(fields=['category']),
            models.Index(fields=['date']),
        ]

    def __str__(self):
        return f"{self.category.name} - ₹{self.amount} on {self.date}"

    @property
    def formatted_amount(self):
        return f"₹{self.amount:,.2f}"


# apps/predictions/models.py
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class AIPrediction(models.Model):
    """AI-generated expense predictions"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='predictions'
    )
    prediction_month = models.CharField(
        max_length=7,
        help_text="Format: YYYY-MM"
    )
    predicted_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))]
    )
    confidence_score = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(100.0)],
        help_text="Confidence percentage (0-100)"
    )
    news_sources = models.JSONField(
        default=list,
        help_text="List of news headlines used for prediction"
    )
    category_breakdown = models.JSONField(
        default=dict,
        help_text="Predicted amount by category"
    )
    algorithm_version = models.CharField(max_length=10, default="1.0")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "AI Prediction"
        verbose_name_plural = "AI Predictions"
        ordering = ['-created_at']
        unique_together = [['user', 'prediction_month']]
        indexes = [
            models.Index(fields=['user', 'prediction_month']),
        ]

    def __str__(self):
        return f"Prediction for {self.prediction_month} - ₹{self.predicted_amount}"

    @property
    def formatted_confidence(self):
        return f"{self.confidence_score:.1f}%"


================================================================================
## 2. VIEWS IMPLEMENTATION
================================================================================

# apps/users/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, LoginForm


def register_view(request):
    """User registration with Aadhar validation"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful! Please login.')
            return redirect('login')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()

    return render(request, 'users/register.html', {'form': form})


def login_view(request):
    """User login"""
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})


@login_required
def logout_view(request):
    """User logout"""
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('home')


# apps/expenses/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, Avg
from django.db.models.functions import TruncMonth, TruncDate
from django.utils import timezone
from datetime import timedelta
from .models import Expense, ExpenseCategory
from .forms import ExpenseForm
import json


@login_required
def dashboard_view(request):
    """Main dashboard with expense summary"""
    user = request.user
    today = timezone.now().date()
    first_day_month = today.replace(day=1)

    # Calculate statistics
    total_expenses = Expense.objects.filter(user=user).aggregate(
        total=Sum('amount')
    )['total'] or 0

    month_expenses = Expense.objects.filter(
        user=user,
        date__gte=first_day_month
    ).aggregate(total=Sum('amount'))['total'] or 0

    categories_used = Expense.objects.filter(user=user).values(
        'category'
    ).distinct().count()

    avg_daily = Expense.objects.filter(
        user=user,
        date__gte=today - timedelta(days=30)
    ).aggregate(avg=Avg('amount'))['avg'] or 0

    # Recent expenses
    recent_expenses = Expense.objects.filter(user=user)[:5]

    # Category breakdown for chart
    category_data = Expense.objects.filter(
        user=user,
        date__gte=first_day_month
    ).values('category__name', 'category__color').annotate(
        total=Sum('amount')
    ).order_by('-total')

    context = {
        'total_expenses': total_expenses,
        'month_expenses': month_expenses,
        'categories_used': categories_used,
        'avg_daily_expense': avg_daily,
        'recent_expenses': recent_expenses,
        'category_data': json.dumps(list(category_data)),
    }

    return render(request, 'expenses/dashboard.html', context)


@login_required
def add_expense_view(request):
    """Add new expense"""
    if request.method == 'POST':
        form = ExpenseForm(request.POST, request.FILES)
        if form.is_valid():
            expense = form.save(commit=False)
            expense.user = request.user
            expense.save()
            messages.success(request, 'Expense added successfully!')
            return redirect('dashboard')
    else:
        form = ExpenseForm()

    return render(request, 'expenses/add_expense.html', {'form': form})


@login_required
def expense_list_view(request):
    """View all expenses with filters"""
    expenses = Expense.objects.filter(user=request.user)

    # Apply filters
    category_filter = request.GET.get('category')
    if category_filter:
        expenses = expenses.filter(category_id=category_filter)

    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    if date_from:
        expenses = expenses.filter(date__gte=date_from)
    if date_to:
        expenses = expenses.filter(date__lte=date_to)

    # Prepare chart data
    # Bar chart - by category
    category_chart = expenses.values('category__name', 'category__color').annotate(
        total=Sum('amount')
    ).order_by('-total')

    # Line chart - over time
    time_chart = expenses.annotate(
        expense_date=TruncDate('date')
    ).values('expense_date').annotate(
        total=Sum('amount')
    ).order_by('expense_date')

    # Pie chart - category distribution
    pie_chart = list(category_chart)

    context = {
        'expenses': expenses,
        'categories': ExpenseCategory.objects.filter(is_active=True),
        'category_chart': json.dumps(list(category_chart)),
        'time_chart': json.dumps(list(time_chart), default=str),
        'pie_chart': json.dumps(pie_chart),
        'total_amount': expenses.aggregate(Sum('amount'))['amount__sum'] or 0,
    }

    return render(request, 'expenses/expense_list.html', context)


@login_required
def delete_expense_view(request, expense_id):
    """Delete an expense"""
    expense = get_object_or_404(Expense, id=expense_id, user=request.user)
    expense.delete()
    messages.success(request, 'Expense deleted successfully!')
    return redirect('expense_list')


# apps/predictions/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Avg
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
import random
from apps.expenses.models import Expense, ExpenseCategory
from .models import AIPrediction


@login_required
def ai_prediction_view(request):
    """Generate and display AI expense predictions"""
    user = request.user

    if request.method == 'POST':
        # Generate new prediction
        prediction = generate_prediction(user)
        context = {
            'prediction': prediction,
            'show_results': True,
        }
    else:
        # Show form and historical predictions
        historical = AIPrediction.objects.filter(user=user)[:5]
        context = {
            'historical_predictions': historical,
            'show_results': False,
        }

    return render(request, 'predictions/ai_prediction.html', context)


def generate_prediction(user):
    """AI prediction algorithm"""
    # Get last 3 months of data
    three_months_ago = timezone.now().date() - timedelta(days=90)
    expenses = Expense.objects.filter(
        user=user,
        date__gte=three_months_ago
    )

    # Calculate category averages
    category_breakdown = {}
    for category in ExpenseCategory.objects.filter(is_active=True):
        cat_expenses = expenses.filter(category=category)
        avg_amount = cat_expenses.aggregate(Avg('amount'))['amount__avg'] or 0

        # Apply trend factor (simulated)
        trend_factor = random.uniform(1.05, 1.15)  # 5-15% increase

        # Apply news sentiment (simulated)
        news_factor = random.uniform(0.95, 1.10)

        predicted = Decimal(str(avg_amount)) * Decimal(str(trend_factor)) * Decimal(str(news_factor))
        category_breakdown[category.name] = float(predicted)

    # Calculate total
    total_predicted = sum(category_breakdown.values())

    # Calculate confidence score
    data_points = expenses.count()
    confidence = min((data_points / 90) * 100, 95.0)  # Max 95%

    # Sample news headlines
    news_headlines = [
        "Economic indicators show 3% inflation rate this quarter",
        "Consumer spending up 5% in retail sector",
        "Healthcare costs expected to rise by 8% next year",
        "Transportation fuel prices stabilizing",
        "Digital entertainment subscriptions see 12% increase"
    ]

    # Get next month
    next_month = (timezone.now() + timedelta(days=30)).strftime('%Y-%m')

    # Create prediction record
    prediction = AIPrediction.objects.create(
        user=user,
        prediction_month=next_month,
        predicted_amount=Decimal(str(total_predicted)),
        confidence_score=confidence,
        news_sources=news_headlines,
        category_breakdown=category_breakdown,
    )

    return prediction


================================================================================
## 3. FORMS IMPLEMENTATION
================================================================================

# apps/users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from .models import CustomUser
import re


class CustomUserCreationForm(UserCreationForm):
    """Custom registration form with Aadhar validation"""
    aadhar_number = forms.CharField(
        max_length=14,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '2XXX XXXX XXXX',
            'pattern': '[2-9]{1}[0-9]{3}\s[0-9]{4}\s[0-9]{4}',
        }),
        help_text="Format: XXXX XXXX XXXX (12 digits with spaces)"
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'aadhar_number', 'password1', 'password2')

    def clean_aadhar_number(self):
        aadhar = self.cleaned_data.get('aadhar_number')

        # Validate format
        pattern = r'^[2-9]{1}[0-9]{3}\s[0-9]{4}\s[0-9]{4}$'
        if not re.match(pattern, aadhar):
            raise ValidationError(
                'Invalid Aadhar format. Must be XXXX XXXX XXXX (cannot start with 0 or 1)'
            )

        # Check for duplicates
        if CustomUser.objects.filter(aadhar_number=aadhar).exists():
            raise ValidationError(
                'This Aadhar number is already registered. Each person can register only once.'
            )

        return aadhar

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError('This email is already registered.')
        return email


class LoginForm(forms.Form):
    """User login form"""
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    remember_me = forms.BooleanField(required=False)


# apps/expenses/forms.py
from django import forms
from .models import Expense, ExpenseCategory


class ExpenseForm(forms.ModelForm):
    """Form for adding/editing expenses"""

    class Meta:
        model = Expense
        fields = ['category', 'amount', 'description', 'date', 'receipt_image']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0.01',
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
            }),
            'receipt_image': forms.FileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = ExpenseCategory.objects.filter(is_active=True)


================================================================================
## 4. URLs CONFIGURATION
================================================================================

# config/urls.py (Main project URLs)
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('users/', include('apps.users.urls')),
    path('expenses/', include('apps.expenses.urls')),
    path('predictions/', include('apps.predictions.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


# apps/users/urls.py
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]


# apps/expenses/urls.py
from django.urls import path
from . import views

app_name = 'expenses'

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('add/', views.add_expense_view, name='add_expense'),
    path('list/', views.expense_list_view, name='expense_list'),
    path('delete/<int:expense_id>/', views.delete_expense_view, name='delete_expense'),
]


# apps/predictions/urls.py
from django.urls import path
from . import views

app_name = 'predictions'

urlpatterns = [
    path('', views.ai_prediction_view, name='ai_prediction'),
]

