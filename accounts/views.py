from datetime import datetime
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from accounts.forms import *
from accounts.models import *
from customer_app.models import *
from django.contrib.auth.decorators import login_required
# Create your views here.
def index(request):
    return render(request,'index.html')

def customer_signup(request):
    if request.method == 'POST':
        form = CustomerRegistrationForm(request.POST)
        u_form = UserRegistrationForm(request.POST)
        if form.is_valid() and u_form.is_valid():
            user = u_form.save(commit=False)
            user.role = 3
            user.is_active = True
            user.save()
            customer = form.save(commit=False)
            customer.user = user
            customer.save()
            return redirect('sign-in') 
    else:
        form = CustomerRegistrationForm()
        u_form = UserRegistrationForm()
    return render(request,'register.html',{'form':form,'u_form':u_form})

def sign_in(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_active:
                login(request, user)
                if user.role == 1:
                    return redirect('admin_home')
                elif user.role == 2:
                    return redirect('worker_home')
                elif user.role == 3:
                    return redirect('customer_home')
            else:
                messages.info(request, 'Invalid Credentials')
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
    return render(request, 'login.html')

def sign_out(request):
    logout(request)
    return redirect('/')

@login_required(login_url='sign-in')
def admin_home(request):
    return render(request,'admintemp/index.html')

@login_required(login_url='sign-in')
def worker_register(request):
    if request.method == 'POST':
        form = WorkerRegistrationForm(request.POST,request.FILES)
        u_form = UserRegistrationForm(request.POST)
        if form.is_valid() and u_form.is_valid():
            user = u_form.save(commit=False)
            user.role = 2
            user.is_active = True
            user.save()
            customer = form.save(commit=False)
            customer.user = user
            customer.save()
            return redirect('workers-admin') 
    else:
        form = WorkerRegistrationForm()
        u_form = UserRegistrationForm()
    return render(request, 'admintemp/worker_register.html', {'form': form,'u_form':u_form})

@login_required(login_url='sign-in')
def worker_view_admin(request):
    data = User.objects.filter(role=2)
    w_data = UserProfile.objects.filter(user__in=data)
    return render(request, 'admintemp/worker_view.html',{'w_data':w_data})

@login_required(login_url='sign-in')
def customer_view(request):
    data = User.objects.filter(role=3)
    c_data = UserProfile.objects.filter(user__in=data)
    return render(request, 'admintemp/customer_view.html',{'c_data':c_data})

@login_required(login_url='sign-in')
def customer_enquiry(request):
    data=Request.objects.all().order_by('-id')
    return render(request,'admintemp/customer_enquiry.html',{'data':data})

@login_required(login_url='sign-in')
def Workers_report(request):
    data = Request.objects.all().order_by('-id')
    return render(request,'admintemp/workers_report.html',{'data':data})

@login_required(login_url='sign-in')
def approve_request(request,pk):
    if request.method=='POST':
        form=AdminApproveRequestForm(request.POST)
        if form.is_valid():
            enquiry_x=Request.objects.get(id=pk)
            enquiry_x.mechanic=form.cleaned_data['mechanic']
            enquiry_x.cost=form.cleaned_data['cost']
            enquiry_x.status=form.cleaned_data['status']
            enquiry_x.save()
            return redirect('customer-enquiry')
    else:
        form=AdminApproveRequestForm()
    return render(request,'admintemp/approve_request.html',{'form':form})

@login_required(login_url='sign-in')
def customer_invoice(request):
    enquiry=Request.objects.all().exclude(status='Pending')
    return render(request,'admintemp/customer_invoice.html',{'enquiry':enquiry})

def view_feedback_admin(request):
    data = Feedback.objects.all()
    context = {'data':data}
    return render(request, 'admintemp/feedback.html', context)

# def generate_report(request):
#     if request.method == 'POST':
#         start_date = request.POST.get('start_date')
#         end_date = request.POST.get('end_date')
        
#         # Convert string dates to datetime objects
#         start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
#         end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        
#         # Query users based on the date range
#         users = User.objects.filter(date_joined__range=[start_date, end_date])
        
#         # Get profile data for the users
#         user_profiles = UserProfile.objects.filter(user__in=users,user__role=2)
        
#         # Prepare data for the report
#         report_data = []
#         for profile in user_profiles:
#             report_data.append({
#                 'username': profile.user.username,
#                 'name': profile.name,
#                 'start_date': profile.user.date_joined,
#                 'end_date': profile.user.last_login
#                 # Add more fields as needed
#             })
        
#         # Render the report template with the data
#         return render(request, 'admintemp/report_template.html', {'report_data': report_data})
    
#     # If the request method is not POST, render the form
#     return render(request, 'admintemp/report_form.html')

def generate_report(request):
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        
        # Convert string dates to datetime objects
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        
        # Query users based on the date range
        users = User.objects.filter(date_joined__range=[start_date, end_date])
        
        # Get profile data for the users
        user_profiles = UserProfile.objects.filter(user__in=users,user__role=2)
        
        # Get request data for the users
        requests = Request.objects.filter(mechanic__in=users, date__range=[start_date, end_date])
        
        # Prepare data for the report
        report_data = []
        for profile in user_profiles:
            user_requests = requests.filter(mechanic=profile.user)
            for req in user_requests:
                report_data.append({
                    'name': profile.name,
                    'category': req.category,
                    'vehicle_no': req.vehicle_no,
                    'vehicle_name': req.vehicle_name,
                    'vehicle_model': req.vehicle_model,
                    'vehicle_brand': req.vehicle_brand,
                    'problem_description': req.problem_description,
                    'date': req.date,
                    'cost': req.cost,
                    'status': req.status,
                    'location': req.location
                    # Add more fields as needed
                })
        
        # Render the report template with the data
        return render(request, 'admintemp/report_template.html', {'report_data': report_data})
    
    # If the request method is not POST, render the form
    return render(request, 'admintemp/report_form.html')


def worker_report(request, pk):
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        
        # Convert string dates to datetime objects
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        
        # Query requests assigned to the worker within the date range
        worker_requests = Request.objects.filter(mechanic_id=pk, date__range=[start_date, end_date])
        
        # Render the worker report template with the filtered requests
        return render(request, 'admintemp/worker_report.html', {'worker_requests': worker_requests})
    
    # If the request method is not POST, render the form to input start and end dates
    return render(request, 'admintemp/worker_report_form.html', {'worker_pk': pk})