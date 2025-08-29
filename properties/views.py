from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.core.cache import cache
from django.conf import settings
from django.http import JsonResponse
from django.db.models import Q
from .models import Property
import logging

logger = logging.getLogger('properties')


class PropertyListView(ListView):
    """Cached view for listing all properties."""
    model = Property
    template_name = 'properties/property_list.html'
    context_object_name = 'properties'
    paginate_by = 10

    def get_queryset(self):
        """Get cached queryset or fetch from database."""
        cache_key = 'property_list_all'
        properties = cache.get(cache_key)
        
        if properties is None:
            logger.info(f"Cache MISS for key: {cache_key}")
            properties = list(Property.objects.all().order_by('-created_at'))
            cache.set(cache_key, properties, settings.CACHE_TTL['property_list'])
        else:
            logger.info(f"Cache HIT for key: {cache_key}")
        
        return properties


class PropertyDetailView(DetailView):
    """Cached view for individual property details."""
    model = Property
    template_name = 'properties/property_detail.html'
    context_object_name = 'property'

    def get_object(self):
        """Get cached property object or fetch from database."""
        pk = self.kwargs.get('pk')
        cache_key = f'property_detail_{pk}'
        property_obj = cache.get(cache_key)
        
        if property_obj is None:
            logger.info(f"Cache MISS for key: {cache_key}")
            property_obj = get_object_or_404(Property, pk=pk)
            cache.set(cache_key, property_obj, settings.CACHE_TTL['property_detail'])
        else:
            logger.info(f"Cache HIT for key: {cache_key}")
        
        return property_obj


class PropertySearchView(ListView):
    """Cached search view for properties."""
    model = Property
    template_name = 'properties/property_search.html'
    context_object_name = 'properties'
    paginate_by = 10

    def get_queryset(self):
        """Get cached search results or fetch from database."""
        query = self.request.GET.get('q', '')
        location = self.request.GET.get('location', '')
        
        if not query and not location:
            return Property.objects.none()
        
        cache_key = f'property_search_{query}_{location}'
        results = cache.get(cache_key)
        
        if results is None:
            logger.info(f"Cache MISS for search key: {cache_key}")
            queryset = Property.objects.all()
            
            if query:
                queryset = queryset.filter(
                    Q(title__icontains=query) | Q(description__icontains=query)
                )
            
            if location:
                queryset = queryset.filter(location__icontains=location)
            
            results = list(queryset.order_by('-created_at'))
            cache.set(cache_key, results, settings.CACHE_TTL['property_search'])
        else:
            logger.info(f"Cache HIT for search key: {cache_key}")
        
        return results

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        context['location'] = self.request.GET.get('location', '')
        return context


def cache_stats_view(request):
    """View to display cache statistics."""
    from django_redis import get_redis_connection
    
    try:
        redis_conn = get_redis_connection("default")
        cache_info = redis_conn.info()
        
        stats = {
            'redis_version': cache_info.get('redis_version'),
            'connected_clients': cache_info.get('connected_clients'),
            'used_memory_human': cache_info.get('used_memory_human'),
            'keyspace_hits': cache_info.get('keyspace_hits', 0),
            'keyspace_misses': cache_info.get('keyspace_misses', 0),
            'total_commands_processed': cache_info.get('total_commands_processed'),
        }
        
        # Calculate hit ratio
        hits = int(stats['keyspace_hits'])
        misses = int(stats['keyspace_misses'])
        total_requests = hits + misses
        
        if total_requests > 0:
            stats['hit_ratio'] = f"{(hits / total_requests) * 100:.2f}%"
        else:
            stats['hit_ratio'] = "0.00%"
        
        return JsonResponse(stats)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)