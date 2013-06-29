from django.contrib import admin
from django.contrib.admin.sites import AdminSite
from django.contrib.admin.forms import AdminAuthenticationForm
from django import forms
from django.utils.translation import ugettext_lazy
from django.contrib.auth import authenticate

ERROR_MESSAGE = ugettext_lazy("Please enter the correct username and password "
        "for a staff account. Note that both fields are case-sensitive.")

class UserAdminAuthenticationForm(AdminAuthenticationForm):
    """
    Same as Django's AdminAuthenticationForm but allows to login
    any user who is not staff.
    """
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        message = ERROR_MESSAGE

        if username and password:
            self.user_cache = authenticate(username=username, password=password)
            if self.user_cache is None:
                if u'@' in username:
                    # Mistakenly entered e-mail address instead of username? Look it up.
                    try:
                        user = User.objects.get(email=username)
                    except (User.DoesNotExist, User.MultipleObjectsReturned):
                        # Nothing to do here, moving along.
                        pass
                    else:
                        if user.check_password(password):
                            message = _("Your e-mail address is not your username."
                                        " Try '%s' instead.") % user.username
                raise forms.ValidationError(message)
            elif not self.user_cache.is_active:
                raise forms.ValidationError(message)
        self.check_for_test_cookie()
        return self.cleaned_data

        
class UserAdmin(AdminSite):
    # Anything we wish to add or override
    login_form = UserAdminAuthenticationForm
    
    def has_permission(self, request):
        return request.user.is_active

    
user_admin_site = UserAdmin(name='usersadmin')
# Run user_admin_site.register() for each model we wish to register
# for our admin interface for users
 