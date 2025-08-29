"""
Django signals for cache invalidation.
This ensures cache consistency when Property objects are modified.
"""

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from .models import Property
import logging

logger = logging.getLogger('cache')


@receiver(post_save, sender=Property)
def invalidate_property_cache_on_save(sender, instance, created, **kwargs):
    """
    Invalidate relevant cache keys when a Property is saved.
    """
    # Clear specific property cache
    property_cache_key = f'property_detail_{instance.pk}'
    cache.delete(property_cache_key)
    logger.info(f"Invalidated cache key: {property_cache_key}")
    
    # Clear list cache
    list_cache_key = 'property_list_all'
    cache.delete(list_cache_key)
    logger.info(f"Invalidated cache key: {list_cache_key}")
    
    # Clear search caches (pattern-based deletion would be ideal, but we'll use a simple approach)
    # In a production environment, you might want to use Redis pattern deletion
    cache.clear()  # This clears all cache - in production, use more selective clearing
    
    action = "Created" if created else "Updated"
    logger.info(f"Property {action}: {instance.title} (ID: {instance.pk})")


@receiver(post_delete, sender=Property)
def invalidate_property_cache_on_delete(sender, instance, **kwargs):
    """
    Invalidate relevant cache keys when a Property is deleted.
    """
    # Clear specific property cache
    property_cache_key = f'property_detail_{instance.pk}'
    cache.delete(property_cache_key)
    logger.info(f"Invalidated cache key: {property_cache_key}")
    
    # Clear list cache
    list_cache_key = 'property_list_all'
    cache.delete(list_cache_key)
    logger.info(f"Invalidated cache key: {list_cache_key}")
    
    # Clear search caches
    cache.clear()  # This clears all cache - in production, use more selective clearing
    
    logger.info(f"Property Deleted: {instance.title} (ID: {instance.pk})")