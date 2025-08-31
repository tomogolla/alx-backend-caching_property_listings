"""
Django management command to populate the database with sample properties.
Run with: python manage.py populate_properties
"""

from django.core.management.base import BaseCommand
from properties.models import Property
from decimal import Decimal
import random


class Command(BaseCommand):
    help = 'Populate database with sample property listings'

    def add_arguments(self, parser):
        parser.add_argument(
            '--count',
            type=int,
            default=50,
            help='Number of properties to create (default: 50)'
        )

    def handle(self, *args, **options):
        count = options['count']
        
        # Sample data
        titles = [
            "Modern Downtown Apartment", "Cozy Family Home", "Luxury Villa with Pool",
            "Spacious Suburban House", "Charming Cottage", "Contemporary Condo",
            "Historic Brownstone", "Beachfront Property", "Mountain Cabin Retreat",
            "Urban Loft Space", "Traditional Colonial", "Garden View Apartment",
            "Penthouse Suite", "Renovated Victorian", "Minimalist Studio"
        ]
        
        descriptions = [
            "Beautiful property with stunning views and modern amenities.",
            "Perfect for families, featuring spacious rooms and a large garden.",
            "Luxury living at its finest with premium finishes throughout.",
            "Quiet neighborhood location with easy access to schools and shopping.",
            "Charming character home with original features and modern updates.",
            "Contemporary design with open floor plan and natural light.",
            "Historic charm meets modern convenience in this unique property.",
            "Rare opportunity to own waterfront property with private access.",
            "Peaceful retreat surrounded by nature and outdoor activities.",
            "Urban living with rooftop terrace and city skyline views."
        ]
        
        locations = [
            "Downtown", "Westside", "Eastbrook", "Riverside", "Highland Park",
            "Oakwood", "Maple Grove", "Cedar Heights", "Pine Valley", "Sunset District",
            "Harbor View", "College Town", "Historic District", "Lakewood", "Forest Hills"
        ]

        # Clear existing properties
        Property.objects.all().delete()
        self.stdout.write("Cleared existing properties.")

        # Create new properties
        properties_created = 0
        for i in range(count):
            title = f"{random.choice(titles)} #{i+1}"
            description = random.choice(descriptions)
            price = Decimal(random.randint(100000, 2000000))
            location = random.choice(locations)
            
            Property.objects.create(
                title=title,
                description=description,
                price=price,
                location=location
            )
            properties_created += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully created {properties_created} property listings.'
            )
        )