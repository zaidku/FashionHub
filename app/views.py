from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.http import HttpRequest
from django.db.models import Sum, Count, Avg
from django.utils import timezone
from .models import Product, Sale, SaleItem, Category
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models.functions import TruncMonth





def home(request):
    """Renders the home page (now will be our dashboard)."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/dashboard.html',  # Changed from index.html to dashboard.html
        {
            'title': 'Dashboard',
            'year': datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title': 'Contact',
            'message': 'Your contact page.',
            'year': datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title': 'About',
            'message': 'Your application description page.',
            'year': datetime.now().year,
        }
    )

# Inventory System Views
def dashboard(request):
    # Calculate date ranges
    today = timezone.now().date()
    last_month = today - timedelta(days=30)
    
    # Sales data
    total_sales = Sale.objects.aggregate(total=Sum('total'))['total'] or 0
    sales_count = Sale.objects.count()
    monthly_sales = Sale.objects.filter(date__gte=last_month).aggregate(total=Sum('total'))['total'] or 0
    previous_month_sales = Sale.objects.filter(
        date__gte=last_month - timedelta(days=30),
        date__lt=last_month
    ).aggregate(total=Sum('total'))['total'] or 0
    
    # Calculate percentage change
    if previous_month_sales > 0:
        sales_change_percent = ((monthly_sales - previous_month_sales) / previous_month_sales) * 100
        ales_change_percent = abs(sales_change)
    else:
        sales_change = 0
        sales_change_percent = 0

    # Inventory data
    total_products = Product.objects.count()
    low_stock_count = Product.objects.filter(quantity__lte=5).count()
    out_of_stock_count = Product.objects.filter(quantity=0).count()
    
    # Recent sales
    recent_sales = Sale.objects.select_related('customer').order_by('-date')[:4]
    
    # Low stock items
    low_stock_items = Product.objects.filter(quantity__lte=5).order_by('quantity')[:4]
    
    # Sales chart data
    sales_data = []
    for i in range(6, -1, -1):
        date = today - timedelta(days=i*5)
        total = Sale.objects.filter(date__date=date).aggregate(total=Sum('total'))['total'] or 0
        sales_data.append(total)
    
    # Product category distribution
    categories = Product.objects.values('category__name').annotate(total=Count('id')).order_by('-total')[:5]
    
    return render(request, 'app/dashboard.html', {
        'title': 'Dashboard',
        'year': datetime.now().year,
        'total_sales': total_sales,
        'sales_count': sales_count,
        'sales_change': sales_change,
        'sales_change_percent': sales_change_percent,
        'sales_change_positive': sales_change_percent >= 0,
        'sales_data': sales_data,
        'sales_labels': [(today - timedelta(days=i*5)).strftime('%b %d') for i in range(6, -1, -1)],
        'monthly_sales': monthly_sales,
        'previous_month_sales': previous_month_sales,
        'total_products': total_products,
        'low_stock_count': low_stock_count,
        'out_of_stock_count': out_of_stock_count,
        'recent_sales': recent_sales,
        'low_stock_items': low_stock_items,
        'categories': categories,
        'category_labels': [c['category__name'] for c in categories],
        'category_data': [c['total'] for c in categories],

    })



def inventory(request):
    products = Product.objects.all().order_by('-created_at')
    categories = Category.objects.all()
    
    return render(request, 'app/inventory.html', {
        'products': products,
        'categories': categories,
        'title': 'Inventory Management'
    })




def sales(request):
    sales = Sale.objects.all().order_by('-date')[:50]
    return render(
        request,
        'app/sales.html',
        {
            'title': 'Sales Management',
            'year': datetime.now().year,
            'sales': sales,
        }
    )



def accounting(request):
    monthly_totals = Sale.objects.annotate(
        month=TruncMonth('date')
    ).values('month').annotate(
        total=Sum('total')
    ).order_by('-month')[:12]
    
    return render(
        request,
        'app/accounting.html',
        {
            'title': 'Accounting',
            'year': datetime.now().year,
            'monthly_totals': monthly_totals,
        }
    )




def settings(request):
    """Renders the settings page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/settings.html',
        {
            'title': 'Settings',
            'year': datetime.now().year,
        }
    )


from .forms import ProductForm
# Add Product Function
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                product = form.save()
                messages.success(request, f'Product "{product.name}" added successfully!')
                return redirect('inventory')
            except Exception as e:
                messages.error(request, f'Error saving product: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProductForm()
    
    return render(request, 'app/add_product.html', {
        'form': form,
        'title': 'Add Product'
    })
