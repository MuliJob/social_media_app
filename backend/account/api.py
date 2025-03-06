from django.http import JsonResponse
from django.contrib.auth.forms import PasswordChangeForm
from rest_framework.decorators import api_view, authentication_classes, permission_classes

# from notification.utils import create_notification

from .forms import SignupForm, ProfileForm
from .models import FriendshipRequest, User
from .serializers import FriendshipRequestSerializer, UserSerializer

@api_view(['GET'])
def me(request):
    """User view"""
    return JsonResponse({
        'id': request.user.id,
        'name': request.user.name,
        'email': request.user.email,
        'avatar': request.user.get_avatar()
    })


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def signup(request):
    """Signup function"""
    data = request.data
    message = 'success'

    form = SignupForm({
        'email': data.get('email'),
        'name': data.get('name'),
        'password1': data.get('password1'),
        'password2': data.get('password2'),
    })

    if form.is_valid():
        user = form.save()
        user.is_active = False
        user.save()

        # url = f'{settings.WEBSITE_URL}/activateemail/?email={user.email}&id={user.id}'

        # send_mail(
        #     "Please verify your email",
        #     f"The url for activating your account is: {url}",
        #     "noreply@wey.com",
        #     [user.email],
        #     fail_silently=False,
        # )
    else:
        message = form.errors.as_json()

    print(message)

    return JsonResponse({'message': message}, safe=False)

@api_view(['GET'])
def friends(request, pk):
    """Friends api view"""
    user = User.objects.get(pk=pk)
    requests = []

    if user == request.user:
        requests = FriendshipRequest.objects.filter(created_for=request.user,
                                                    status=FriendshipRequest.SENT)
        requests = FriendshipRequestSerializer(requests, many=True)
        requests = requests.data

    friendship = user.friends.all()

    return JsonResponse({
        'user': UserSerializer(user).data,
        'friends': UserSerializer(friendship, many=True).data,
        'requests': requests
    }, safe=False)


@api_view(['POST'])
def edit_profile(request):
    """Editing user profile"""
    user = request.user
    email = request.data.get('email')

    if User.objects.exclude(id=user.id).filter(email=email).exists():
        return JsonResponse({'message': 'email already exists'})
    else:
        form = ProfileForm(request.POST, request.FILES, instance=user)

        if form.is_valid():
            form.save()

        serializer = UserSerializer(user)

        return JsonResponse({'message': 'information updated', 'user': serializer.data})


@api_view(['POST'])
def edit_password(request):
    """Changing password"""
    user = request.user

    form = PasswordChangeForm(data=request.POST, user=user)

    if form.is_valid():
        form.save()

        return JsonResponse({'message': 'success'})
    else:
        return JsonResponse({'message': form.errors.as_json()}, safe=False)


@api_view(['POST'])
def send_friendship_request(request, pk):
    """Sending friendship request"""
    user = User.objects.get(pk=pk)

    check1 = FriendshipRequest.objects.filter(created_for=request.user).filter(created_by=user)
    check2 = FriendshipRequest.objects.filter(created_for=user).filter(created_by=request.user)

    if not check1 or not check2:
        FriendshipRequest.objects.create(created_for=user, created_by=request.user)

        # notification = create_notification(request,
        #                                    'new_friendrequest', friendrequest_id=friendrequest.id)

        return JsonResponse({'message': 'friendship request created'})
    else:
        return JsonResponse({'message': 'request already sent'})

@api_view(['POST'])
def handle_request(request, pk, status):
    """Accepting and Rejecting friendship requests"""
    user = User.objects.get(pk=pk)
    friendship_request = FriendshipRequest.objects.filter(
        created_for=request.user).get(created_by=user)
    friendship_request.status = status
    friendship_request.save()

    user.friends.add(request.user)
    user.friends_count = user.friends_count + 1
    user.save()

    request_user = request.user
    request_user.friends_count = request_user.friends_count + 1
    request_user.save()

    # notification = create_notification(request,
    #                                     'accepted_friendrequest',
    #                                     friendrequest_id=friendship_request.id)

    return JsonResponse({'message': 'friendship request updated'})
