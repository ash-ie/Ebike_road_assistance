from django.urls import path
from accounts import views

urlpatterns = [
    path('',views.index,name='index'),
    path('sign-up/',views.customer_signup,name='sign-up'),
    path('sign-in/',views.sign_in,name='sign-in'),
    path('sign-out/',views.sign_out,name='sign-out'),
    path('admin_home/',views.admin_home,name='admin_home'),
    path('worker-signup/', views.worker_register, name='worker-signup'),
    path('workers-admin/', views.worker_view_admin, name='workers-admin'),
    path('customers/', views.customer_view, name='customers'),
    path('customer-enquiry/',views.customer_enquiry,name='customer-enquiry'),
    path('worker-report/',views.Workers_report,name='worker-report'),
    path('approve-request/<int:pk>/',views.approve_request,name='approve-request'),
    path('customer-invoice/',views.customer_invoice,name='customer-invoice'),
    path('feedback-admin/',views.view_feedback_admin,name='feedback-admin'),
    path('generate_report',views.generate_report,name="generate_report"),
     path('worker_report/<int:worker_pk>/', views.worker_report, name='worker_report'),

]