from rest_framework.decorators import api_view
from django.http import JsonResponse

from .forms import PostForm
from .models import Post
from .serializers import PostSerializer

from account.models import User
from account.serializers import UserSerializer

@api_view(['GET'])
def post_list(request):
    """Posting a post"""
    posts = Post.objects.all()

    serializer = PostSerializer(posts, many=True)

    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def post_list_profile(request, id):
    """Profile list"""
    user = User.objects.get(pk=id)
    posts = Post.objects.filter(created_by_id=id)

    # if not request.user in user.friends.all():
    #     posts = posts.filter(is_private=False)

    posts_serializer = PostSerializer(posts, many=True)
    user_serializer = UserSerializer(user)

    # can_send_friendship_request = True

    # if request.user in user.friends.all():
    #     can_send_friendship_request = False

    # check1 = FriendshipRequest.objects.filter(created_for=request.user).filter(created_by=user)
    # check2 = FriendshipRequest.objects.filter(created_for=user).filter(created_by=request.user)

    # if check1 or check2:
    #     can_send_friendship_request = False

    return JsonResponse({
        'posts': posts_serializer.data,
        'user': user_serializer.data,
        # 'can_send_friendship_request': can_send_friendship_request
    }, safe=False)

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
