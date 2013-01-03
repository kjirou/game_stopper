# coding: utf8
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth import login
from django.db.transaction import commit_on_success
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt
from accounts.forms import SignUpForm
from accounts.models import UserProfile


@commit_on_success
def sign_up(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user_profile = UserProfile.objects.create_with_user(
                form.cleaned_data['username'],
                form.cleaned_data['password']
            )
            login(request, user_profile.user)
            return HttpResponseRedirect(reverse('locks:index'))
    else:
        form = SignUpForm()

    c = dict(form=form)
    return render_to_response('accounts/sign_up.html', c,
        context_instance=RequestContext(request))
