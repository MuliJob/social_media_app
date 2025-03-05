from rest_framework.decorators import api_view
from django.http import JsonResponse

from .forms import PostForm
from .models import Post
from .serializers import PostSerializer

@api_view(['GET'])
def post_list(request):
    """Posting a post"""
    posts = Post.objects.all()

    serializer = PostSerializer(posts, many=True)

    return JsonResponse(serializer.data, safe=False)

@api_view(['POST'])
def post_create(request):
    """Creating a post"""
    form = PostForm(request.POST)
    # attachment = None
    # attachment_form = AttachmentForm(request.POST, request.FILES)

    # if attachment_form.is_valid():
    #     attachment = attachment_form.save(commit=False)
    #     attachment.created_by = request.user
    #     attachment.save()

    if form.is_valid():
        post = form.save(commit=False)
        post.created_by = request.user
        post.save()

        # if attachment:
        #     post.attachments.add(attachment)

        user = request.user
        user.posts_count = user.posts_count + 1
        user.save()

        serializer = PostSerializer(post)

        return JsonResponse(serializer.data, safe=False)
    else:
        return JsonResponse({'error': 'add something here later!...'})
