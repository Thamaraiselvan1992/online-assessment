
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import loader
from django.urls import reverse

from apps.home.forms import AssesmentForm


@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def assesments(request):
    context = {}
    
    return render(request,'home/assesments.html')
@login_required(login_url="/login/")
def test(request):
    context = {}
    
    return render(request,'home/test.html')

@login_required(login_url="/login/")
def create_assesment(request):
    msg = None
    success = False

    if request.method == "POST":
        form = AssesmentForm(request.POST)
        if form.is_valid():
            form.save()

            msg = 'Assesment Sucessfully created.'
            success = True

            # return redirect("/login/")

        else:
            msg = 'Form is not valid'
    else:
        form = AssesmentForm()
    # return HttpResponse(form)
    return render(request, "home/create-assesments.html", {"form": form, "msg": msg, "success": success})
