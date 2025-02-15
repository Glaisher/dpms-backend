from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model


class EmployeeIDBackend(BaseBackend):
    def authenticate(self, request, employee_id=None, password=None, **kwargs):
        try:
            user = get_user_model().objects.get(employee_id=employee_id)
            if user.check_password(password):
                return user
        except get_user_model().DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return get_user_model().objects.get(pk=user_id)
        except get_user_model().DoesNotExist:
            return None
