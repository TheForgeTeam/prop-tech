from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from properties.models import Owner, Property, Deal
from django.utils import timezone
from datetime import timedelta
import random

class Command(BaseCommand):
    help = 'Populates the database with test data'

    def handle(self, *args, **kwargs):
        # Create test users and owners
        test_owners_data = [
            {'username': 'john_doe', 'email': 'john@example.com', 'first_name': 'John', 'last_name': 'Doe'},
            {'username': 'jane_smith', 'email': 'jane@example.com', 'first_name': 'Jane', 'last_name': 'Smith'},
            {'username': 'bob_wilson', 'email': 'bob@example.com', 'first_name': 'Bob', 'last_name': 'Wilson'},
        ]

        owners = []
        for owner_data in test_owners_data:
            user, created = User.objects.get_or_create(
                username=owner_data['username'],
                defaults={
                    'email': owner_data['email'],
                    'first_name': owner_data['first_name'],
                    'last_name': owner_data['last_name']
                }
            )
            if created:
                user.set_password('testpass123')
                user.save()
                
            owner, _ = Owner.objects.get_or_create(
                user=user,
                defaults={
                    'phone': f'+1555{random.randint(1000000, 9999999)}',
                    'address': f'{random.randint(100, 999)} Test Street, Test City'
                }
            )
            owners.append(owner)

        # Create test properties
        property_titles = [
            'Luxury Downtown Apartment', 'Suburban Family Home', 'Beach House',
            'Mountain Cabin', 'City Center Studio', 'Commercial Space',
            'Modern Loft', 'Garden Apartment', 'Penthouse Suite'
        ]

        properties = []
        for title in property_titles:
            property = Property.objects.create(
                owner=random.choice(owners),
                title=title,
                property_type=random.choice(['house', 'apartment', 'commercial', 'land']),
                address=f'{random.randint(100, 999)} {random.choice(["Main", "Oak", "Maple", "Cedar"])} Street',
                size=random.randint(50, 500),
                bedrooms=random.randint(0, 5),
                bathrooms=random.randint(1, 4),
                price=random.randint(100000, 1000000),
                description=f'This is a test description for {title}',
                is_available=random.choice([True, True, False])  # 2/3 chance of being available
            )
            properties.append(property)

        # Create test deals
        for property in properties:
            # Create 1-3 deals for each property
            for _ in range(random.randint(1, 3)):
                start_date = timezone.now() - timedelta(days=random.randint(0, 365))
                deal_type = random.choice(['rent', 'sale'])
                
                Deal.objects.create(
                    property=property,
                    deal_type=deal_type,
                    status=random.choice(['pending', 'active', 'completed', 'cancelled']),
                    price=property.price * (0.004 if deal_type == 'rent' else 1),  # Monthly rent is roughly 0.4% of property value
                    start_date=start_date,
                    end_date=start_date + timedelta(days=365) if deal_type == 'rent' else None
                )

        self.stdout.write(self.style.SUCCESS('Successfully created test data'))