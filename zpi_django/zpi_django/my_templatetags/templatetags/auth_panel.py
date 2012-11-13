from django import template

register = template.Library()
from zpi_django.auth.auth_forms import LoginForm

@register.inclusion_tag('templatetags/auth_template.html', takes_context = True)
def show_auth_panel(context):
    request = context['request']
    if request.user.is_authenticated():
        return {}
    else:
        login_form = LoginForm()
        return {'login_form': login_form}
