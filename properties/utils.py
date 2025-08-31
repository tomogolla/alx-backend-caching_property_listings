from django.core.cache import cache
from django_redis import get_redis_connection
from .models import Property
import logging

# Configure logger
logger = logging.getLogger('cache_metrics')
logging.basicConfig(
    filename='/tmp/cache_metrics_log.txt',
    level=logging.INFO,
    format='%(asctime)s - Cache Metrics: Hits=%(hits)s, Misses=%(misses)s, Hit Ratio=%(hit_ratio)s'
)

def get_all_properties():
    # Check cache for all_properties
    properties = cache.get('all_properties')
    
    if properties is None:
        # Fetch from database if not in cache
        properties = Property.objects.all()
        # Store in cache for 1 hour (3600 seconds)
        cache.set('all_properties', properties, 3600)
    
    return properties

def get_redis_cache_metrics():
    try:
        # Connect to Redis
        redis_conn = get_redis_connection('default')
        
        # Get Redis INFO stats
        info = redis_conn.info('stats')
        
        # Extract hits and misses
        keyspace_hits = info.get('keyspace_hits', 0)
        keyspace_misses = info.get('keyspace_misses', 0)
        
        # Calculate hit ratio
        total_requests = keyspace_hits + keyspace_misses
        hit_ratio = (keyspace_hits / total_requests) if total_requests > 0 else 0.0
        
        # Log metrics
        logger.info(
            '',
            extra={
                'hits': keyspace_hits,
                'misses': keyspace_misses,
                'hit_ratio': f'{hit_ratio:.2%}'
            }
        )
        
        # Return metrics dictionary
        return {
            'keyspace_hits': keyspace_hits,
            'keyspace_misses': keyspace_misses,
            'hit_ratio': hit_ratio
        }
    
    except Exception as e:
        logger.error(f'Error retrieving cache metrics: {str(e)}')
        return {
            'keyspace_hits': 0,
            'keyspace_misses': 0,
            'hit_ratio': 0.0,
            'error': str(e)
        }