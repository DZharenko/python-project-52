from django.contrib import messages


class LoginSessionMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.session.pop("just_logged_in", False):
            messages.success(request, "Вы залогинены")
        response = self.get_response(request)
        return response