from django.views.decorators.cache import cache_page
from django.http import JsonResponse
from .utils import get_all_properties

@cache_page(60 * 15)  # Cache for 15 minutes
def property_list(request):
    properties = get_all_properties()
    data = [
        {
            'id': prop.id,
            'title': prop.title,
            'description': prop.description,
            'price': str(prop.price),  # Convert Decimal to string for JSON
            'location': prop.location,
            'created_at': prop.created_at.isoformat()
        }
        for prop in properties
    ]
    return JsonResponse({'properties': data})