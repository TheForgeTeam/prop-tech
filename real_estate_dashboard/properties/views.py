from django.shortcuts import render
from django.db.models import Count, Sum
from .models import Property, Deal
from decimal import Decimal
import json  # Add this import
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from decimal import Decimal, InvalidOperation
from django.contrib.auth.decorators import login_required

# Add this custom JSON encoder
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)

@login_required
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


@login_required
def rentals(request):
    # Get all rental deals with related property data
    rental_deals = Deal.objects.filter(
        deal_type='rent'
    ).select_related('property', 'property__owner', 'property__owner__user').order_by('-created_at')

    # Get available properties for the form
    available_properties = Property.objects.filter(is_available=True)

    context = {
        'rental_deals': rental_deals,
        'available_properties': available_properties,
    }
    return render(request, 'properties/rentals.html', context)

@login_required
@require_http_methods(["POST"])
def create_rental(request):
    try:
        property_id = request.POST.get('property')
        price = request.POST.get('price')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date') or None

        # Debug prints
        print("Received data:")
        print(f"Property ID: {property_id}")
        print(f"Price: {price}")
        print(f"Start date: {start_date}")
        print(f"End date: {end_date}")

        property_obj = Property.objects.get(id=property_id)
        
        new_deal = Deal.objects.create(
            property=property_obj,
            deal_type='rent',
            status='pending',
            price=price,
            start_date=start_date,
            end_date=end_date
        )

        return JsonResponse({'success': True})
    except Exception as e:
        print(f"Error creating rental: {str(e)}")  # Debug print
        return JsonResponse({'success': False, 'error': str(e)})

@login_required
def properties(request):
    # Get all sale deals with related property data
    sale_deals = Deal.objects.filter(
        deal_type='sale'
    ).select_related('property', 'property__owner', 'property__owner__user').order_by('-created_at')

    # Get available properties for the form
    available_properties = Property.objects.filter(is_available=True)

    context = {
        'sale_deals': sale_deals,
        'available_properties': available_properties,
    }
    return render(request, 'properties/properties.html', context)

@login_required
@require_http_methods(["POST"])
def create_sale(request):
    try:
        property_id = request.POST.get('property')
        price_str = request.POST.get('price')
        start_date = request.POST.get('start_date')

        # Validate and convert price to Decimal
        try:
            price = Decimal(price_str)
        except InvalidOperation:
            return JsonResponse({
                'success': False, 
                'error': 'Invalid price format. Please enter a valid number.'
            })

        property_obj = Property.objects.get(id=property_id)
        
        Deal.objects.create(
            property=property_obj,
            deal_type='sale',
            status='pending',
            price=price,
            start_date=start_date
        )

        return JsonResponse({'success': True})
    except Exception as e:
        print(f"Error creating sale: {str(e)}")  # Debug print
        return JsonResponse({'success': False, 'error': str(e)})