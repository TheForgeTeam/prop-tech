from django.shortcuts import render
from django.db.models import Count, Sum
from .models import Property, Deal
from decimal import Decimal
import json  # Add this import

# Add this custom JSON encoder
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)

def dashboard(request):
    # Get summary statistics
    total_properties = Property.objects.count()
    total_rentals = Deal.objects.filter(deal_type='rent', status='active').count()
    total_sales = Deal.objects.filter(deal_type='sale', status='completed').count()
    
    # Get recent rental deals
    recent_rentals = Deal.objects.filter(
        deal_type='rent'
    ).select_related('property').order_by('-created_at')[:5]
    
    # Get recent sale deals
    recent_sales = Deal.objects.filter(
        deal_type='sale'
    ).select_related('property').order_by('-created_at')[:5]
    
    # Get data for charts
    deals_by_type = Deal.objects.values('deal_type').annotate(
        count=Count('id'),
        total_value=Sum('price')
    )
    
    property_by_type = Property.objects.values('property_type').annotate(
        count=Count('id')
    )

    # Convert querysets to JSON-safe format with our custom encoder
    deals_by_type_data = list(deals_by_type)
    property_by_type_data = list(property_by_type)

    context = {
        'total_properties': total_properties,
        'total_rentals': total_rentals,
        'total_sales': total_sales,
        'recent_rentals': recent_rentals,
        'recent_sales': recent_sales,
        'deals_by_type_json': json.dumps(deals_by_type_data, cls=DecimalEncoder),  # Use custom encoder
        'property_by_type_json': json.dumps(property_by_type_data, cls=DecimalEncoder),  # Use custom encoder
    }
    
    return render(request, 'properties/dashboard.html', context)



def rentals(request):
    return render(request, 'properties/rentals.html')

def properties(request):
    return render(request, 'properties/properties.html')