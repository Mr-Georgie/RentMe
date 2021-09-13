from django.http import JsonResponse, response

def error_404(request, exception):
    message = ('This endpoint was not found')
    
    response = JsonResponse(data={
        'message':message,
        'status_code': 404
    })
    response.status_code = 404
    return response


def error_500(request):
    message = ("A server error occurred. Please contact our customer care immediately")
    
    response = JsonResponse(data={
        'message':message,
        'status_code': 500
    })
    response.status_code = 500
    return response
