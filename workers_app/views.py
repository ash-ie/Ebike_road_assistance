from django.shortcuts import render,redirect
from accounts.forms import *
from accounts.models import *
from customer_app.models import *
from workers_app.forms import *
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required(login_url='sign-in')
def worker_home(request):
    return render(request,'workertemp/index.html')

@login_required(login_url='sign-in')
def work_assigned(request):
    worker=User.objects.get(username=request.user)
    works=Request.objects.all().filter(mechanic=worker)
    return render(request,'workertemp/work_assigned.html',{'works':works})

@login_required(login_url='sign-in')
def update_work_status(request,pk):
    if request.method=='POST':
        form=MechanicUpdateStatusForm(request.POST)
        if form.is_valid():
            enquiry_x=Request.objects.get(id=pk)
            enquiry_x.status=form.cleaned_data['status']
            enquiry_x.save()
            return redirect('work-assigned')
    else:
        form=MechanicUpdateStatusForm()
    return render(request,'workertemp/work_update.html',{'form':form})

@login_required(login_url='sign-in')
def profile_view(request):
    data = UserProfile.objects.filter(user=request.user)
    return render(request,'workertemp/profile.html',{'data':data})

@login_required(login_url='sign-in')
def update_profile(request):
    worker = UserProfile.objects.get(user=request.user)
    form = WorkerRegistrationForm(instance=worker)
    if request.method == 'POST':
        form = WorkerRegistrationForm(request.POST or None, instance=worker or None)
        if form.is_valid():
            form.save()
            return redirect('profile')
    return render(request, 'workertemp/update_profile.html', {'form': form, })

@login_required(login_url='sign-in')
def view_feedback_worker(request):
    data = Feedback.objects.all()
    context = {'data':data}
    return render(request, 'workertemp/feedback.html', context)

