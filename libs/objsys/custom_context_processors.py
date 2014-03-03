#Ref: http://rubayeet.com/2009/10/31/django-how-to-make-a-variable-available-in-all-templates/


from allauth.account.forms import LoginForm

def head_form(request):
    form_class = LoginForm
    if request.method == "POST":
        form = form_class(request.POST)
        if form.is_valid():
            return form.login(request, redirect_url=success_url)
    else:
        form = form_class()
    return {"head_form" : form}