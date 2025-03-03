from django.http import JsonResponse

from rest_framework.decorators import api_view, authentication_classes, permission_classes

from .forms import SignupForm

@api_view(['GET'])
def me(request):
    """User view"""
    return JsonResponse({
        'id': request.user.id,
        'name': request.user.name,
        'email': request.user.email,
        # 'avatar': request.user.get_avatar()
    })


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def signup(request):
    """Signup API View"""
    data = request.data
    message = 'success'

    form = SignupForm({
        'name': data.get('name'),
        'email': data.get('email'),
        'password1': data.get('password1'),
        'password2': data.get('password2'),
    })

    if form.is_valid():
        form.save()

        #send verification email later!
    else:
        message = 'error'

    return JsonResponse({'message': message})
