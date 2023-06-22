from django.contrib.auth import get_user_model
from django.contrib import messages

UserModel = get_user_model()

class ProfileMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if request.user.is_authenticated:
            try:
                user = UserModel.objects.get(pk=request.user.id)
                if not hasattr(user, 'role'):
                    # Handle the case when the user model doesn't have a 'role' attribute
                    pass
                elif user.role == UserModel.Role.TAXIPASSENGER:
                    # Logic for Taxi Passenger role
                    request.user = user  # Assign the user object to the request
                    # Additional logic specific to Taxi Passenger role
                    # For example, set request.passenger or request.role
                else:
                    # Handle the case when the user has a different role (e.g., Taxi Driver)
                    pass
            except UserModel.DoesNotExist:
                # Handle the case when the user is not found
                messages.error(request, 'User not found.')

        return response
