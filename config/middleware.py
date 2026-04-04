from django.shortcuts import redirect
from django.urls import reverse, resolve, NoReverseMatch
from django.utils.translation import get_language, activate


class ProfileCompleteMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.exempt_view_names = [
            'accounts:update_user',
            'accounts:create_gallery',
            'accounts:update_gallery',
            'accounts:my_profile',
            'accounts:create_profile',
            'accounts:profile_image',
            'accounts:update_profile',
            'accounts:create_preference',
            'accounts:update_preference',
            'accounts:ajax_load_states',
            'accounts:ajax_load_cities',
            'notifications:count',
            'company:home',
            'account_logout',
            '/accounts/ajax/load-states/',
            '/accounts/ajax/load-cities/',
        ]

    def __call__(self, request):
        if request.user.is_authenticated:
            try:
                current_url_name = resolve(request.path_info).view_name
            except Exception:
                current_url_name = None

            if request.path.startswith('/accounts/ajax/'):
                return self.get_response(request)

            is_exempt = current_url_name in self.exempt_view_names

            if not is_exempt:
                try:
                    profile = request.user.matrimony_profile
                    if not profile.is_profile_completed:
                        return redirect('accounts:my_profile')
                except AttributeError:
                    return redirect('accounts:my_profile')

        return self.get_response(request)
