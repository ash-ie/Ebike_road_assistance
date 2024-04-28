from django.shortcuts import render,redirect
from accounts.models import *
from customer_app.forms import *
from customer_app.models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
# Create your views here.
@login_required(login_url='sign-in')
def customer_home(request):
    return render(request,'customertemp/index.html')

@login_required(login_url='sign-in')
def worker_view_customer(request):
    data = User.objects.filter(role=2)
    w_data = UserProfile.objects.filter(user__in=data)
    return render(request, 'customertemp/worker_view.html',{'w_data':w_data})

@login_required(login_url='sign-in')
def add_request(request):
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            requestobj=form.save(commit=False)
            requestobj.customer = request.user
            requestobj.save()
            return redirect('requests')
    else:
        form = RequestForm()
    context = {'form': form}
    return render(request, 'customertemp/add_request.html', context)

@login_required(login_url='sign-in')
def view_request(request):
    customer=User.objects.get(username=request.user)
    enquiries=Request.objects.all().filter(customer_id=customer.id , status="Pending")
    return render(request,'customertemp/view_requests.html',{'customer':customer,'enquiries':enquiries})

@login_required(login_url='sign-in')
def view_approved_request(request):
    customer=User.objects.get(username=request.user)
    enquiries=Request.objects.all().filter(customer_id=customer.id).exclude(status='Pending')
    return render(request,'customertemp/approved_requests.html',{'customer':customer,'enquiries':enquiries})

@login_required(login_url='sign-in')
def delete_request(request,pk):
    enquiry=Request.objects.get(id=pk)
    enquiry.delete()
    return redirect('requests')

@login_required(login_url='sign-in')
def add_feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            requestobj=form.save(commit=False)
            requestobj.user = request.user
            requestobj.save()
            return redirect('feedbacks')
    else:
        form = FeedbackForm()
    context = {'form': form}
    return render(request, 'customertemp/add_feedback.html', context)

@login_required(login_url='sign-in')
def view_feedback(request):
    data = Feedback.objects.all()
    context = {'data':data}
    return render(request, 'customertemp/feedback.html', context)

@login_required(login_url='sign-in')
def pay_bill(request, id):
    bi = Request.objects.get(id=id)
    if request.method == 'POST':
        card = request.POST.get('card')
        c = request.POST.get('cvv')
        da = request.POST.get('exp')
        CreditCard(card_no=card, card_cvv=c, expiry_date=da).save()
        bi.bill_status = 1
        bi.save()
        messages.info(request, 'Bill Paid  Successfully')
        return redirect('approved-requests')
    return render(request, 'customertemp/pay_bill.html', )

@login_required(login_url='sign-in')
def pay_in_direct(request, id):
    bi = Request.objects.get(id=id)
    bi.bill_status = 2
    bi.save()
    messages.info(request, 'Choosed to Pay Fee Direct in office')
    return redirect('approved-requests')




