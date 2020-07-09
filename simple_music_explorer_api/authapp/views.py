from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace'])
def url_redirect_404(request):
    return Response(status=status.HTTP_404_NOT_FOUND)
