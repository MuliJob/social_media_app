from rest_framework.decorators import api_view

from django.db.models import Q
from django.http import JsonResponse

from account.models import User
from account.serializers import UserSerializer

from .forms import PostForm
from .models import Post, Like
from .serializers import PostSerializer, PostDetailSerializer


@api_view(['GET'])
def post_list(request):
    """Posting a post"""
    user_ids = [request.user.id]

    for user in request.user.friends.all():
        user_ids.append(user.id)

    posts = Post.objects.filter(created_by_id__in=list(user_ids))

    trend = request.GET.get('trend', '')

    if trend:
        posts = posts.filter(body__icontains='#' + trend).filter(is_private=False)

    serializer = PostSerializer(posts, many=True)

    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def post_detail(request, pk):
    """Post detail function"""
    user_ids = [request.user.id]

    for user in request.user.friends.all():
        user_ids.append(user.id)

    post = Post.objects.filter(Q(created_by_id__in=list(user_ids)) | Q(is_private=False)).get(pk=pk)

    return JsonResponse({
        'post': PostDetailSerializer(post).data
    })

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


@api_view(['POST'])
def post_like(request, pk):
    """Liking a post"""
    post = Post.objects.get(pk=pk)

    if not post.likes.filter(created_by=request.user):
        like = Like.objects.create(created_by=request.user)

        post = Post.objects.get(pk=pk)
        post.likes_count = post.likes_count + 1
        post.likes.add(like)
        post.save()

        # notification = create_notification(request, 'post_like', post_id=post.id)

        return JsonResponse({'message': 'like created'})
    else:
        return JsonResponse({'message': 'post already liked'})
