from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json


@csrf_exempt
@require_http_methods(["POST"])
def update(request):
    """
    Update server endpoint for webhook or deployment updates.
    """
    try:
        # Parse JSON data if present
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.POST
        
        # Basic response for update endpoint
        return JsonResponse({
            'status': 'success',
            'message': 'Server update received',
            'data': data
        })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)
