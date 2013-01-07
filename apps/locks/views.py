# coding: utf8
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.db.transaction import commit_on_success
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.loader import get_template
from locks.forms import CreateForm
from locks.models import Lock


@login_required
def index(request):
    c = {
        'locks': Lock.objects.filter(
            user_profile=request.user.get_profile()).order_by('-locked_at'),
    }
    return render_to_response('locks/index.html', c,
        context_instance=RequestContext(request))


@login_required
@commit_on_success
def create(request):

    # TODO:
    # - 二重投稿対策と重いファイルの際のNow loading表示

    if request.method == 'POST':
        form = CreateForm(request.POST, request.FILES)
        if form.is_valid():
            Lock.objects.create_by_user(
                request.user,
                form.cleaned_data['locked_file'],
                form.cleaned_data['period'],
                form.cleaned_data['saved_hours'],
            )
            return HttpResponseRedirect(reverse('locks:index'))
    else:
        form = CreateForm()

    c = dict(form=form)
    return render_to_response('locks/create.html', c,
        context_instance=RequestContext(request))


@login_required
@commit_on_success
def delete_file(request, id):
    return HttpResponse('delete' + str(id))
