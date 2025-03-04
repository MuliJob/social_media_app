from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.http import JsonResponse

from .models import Post
from .serializers import PostSerializer

@api_view(['GET'])
# @authentication_classes([])
# @permission_classes([])
def post_list(request):
    """Posting a post"""
    posts = Post.objects.all()

    serializer = PostSerializer(posts, many=True)

    return JsonResponse({'data': serializer.data})
