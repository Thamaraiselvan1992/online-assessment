
import json
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template import loader
from django.urls import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from apps.home.forms import AssesmentForm, CandidateForm
from apps.home.models import Assesment, Candidate, CandidateAssessment


@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


# @login_required(login_url="/login/")
# def pages(request):
#     context = {}
#     # All resource paths end in .html.
#     # Pick out the html file name from the url. And load that template.
#     try:

#         load_template = request.path.split('/')[-1]

#         if load_template == 'admin':
#             return HttpResponseRedirect(reverse('admin:index'))
#         context['segment'] = load_template

#         html_template = loader.get_template('home/' + load_template)
#         return HttpResponse(html_template.render(context, request))

#     except template.TemplateDoesNotExist:

#         html_template = loader.get_template('home/page-404.html')
#         return HttpResponse(html_template.render(context, request))

#     except:
#         html_template = loader.get_template('home/page-500.html')
#         return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def assesments(request):
    # context = {}
    
    # return render(request,'home/assesments.html')
    assesments =Assesment.objects.filter().order_by('-id')
    # students = User.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(assesments, 5)
    try:
        assesments = paginator.page(page)
    except PageNotAnInteger:
        assesments = paginator.page(1)
    except EmptyPage:
        assesments = paginator.page(paginator.num_pages)
    return render(request,'home/assesments.html',{'assesment_list':assesments})

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
            list=[]
            option_a =request.POST.getlist('option_a[]')
            option_b =request.POST.getlist('option_b[]')
            option_c =request.POST.getlist('option_c[]')
            option_d =request.POST.getlist('option_d[]')
            answer =request.POST.getlist('answer[]')
            # return HttpResponse(request.POST.getlist('questions[]'))
            for idx,x in enumerate(request.POST.getlist('questions[]')):
                ques={}
                ques['question']=x
                # ques['answer']=form.cleaned_data['questions'][idx]
                ques['marks']=request.POST.get('mark')
                ques['times']=request.POST.get('times')
                ques['options']=[option_a[idx],option_b[idx],option_c[idx],option_d[idx]]
                ques['answer']=answer[idx]
                list.append(ques)

            obj = Assesment() #gets new object
            obj.title = form.cleaned_data['title']
            obj.description = form.cleaned_data['description']
            obj.questions = json.dumps(list)
            obj.save()

            msg = 'Assessment Sucessfully created.'
            success = True

            return redirect("/assessments/")

        else:
            msg = 'Form is not valid'

        
    else:
        form = AssesmentForm()
    # return HttpResponse(form)
        return render(request, "home/create-assesments.html", {"form": form, "msg": msg, "success": success})

@login_required(login_url="/login/")
def add_candidate(request,id):
    msg = None
    success = False
    assesments =Assesment.objects.get(id=id)
    if request.method =='POST':
        if not Candidate.objects.filter(candidate_email=request.POST.get('candidate_email')).exists():
            obj = Candidate() #gets new object
            obj.candidate_name = request.POST.get('candidate_name')
            obj.candidate_email = request.POST.get('candidate_email')
            obj.candidate_mobile = request.POST.get('candidate_mobile')
            obj.save()

        candidate =Candidate.objects.get(candidate_email=request.POST.get('candidate_email'))
        if candidate:
            if not CandidateAssessment.objects.filter(candidate_id=candidate.id,assessment_id=request.POST.get('assessment_id')).exists():
                canAssessment = CandidateAssessment() #gets new object
                canAssessment.candidate_id = candidate.id
                canAssessment.token = uuid.uuid4()
                canAssessment.assessment_id = request.POST.get('assessment_id')
                canAssessment.save()
                return redirect("/assessments/")
            else:
                msg = 'This candidate already added this assignments'
        else:
             msg = 'Candidate Not Created try again'

    else:
      
        questions = json.loads(assesments.questions)
        form = CandidateForm()
    return render(request,'home/add_candidate.html',{'assesment':assesments,'questions':questions,'form':form,'msg':msg})

def send_mail_test(request):
    subject = 'welcome to GFG world'
    message = f'Hi Selvan, thank you for registering in geeksforgeeks.'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = ['tsthamarai4@gmail.com', ]
    send_mail( subject, message, email_from, recipient_list )
