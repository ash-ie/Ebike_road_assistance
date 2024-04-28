from django.urls import path

from customer_app import views

urlpatterns = [
    path('customer_home/',views.customer_home,name='customer_home'),
    path('workers/',views.worker_view_customer,name='workers'),
    path('add-request/',views.add_request,name='add-request'),
    path('requests/',views.view_request,name='requests'),
    path('approved-requests/',views.view_approved_request,name='approved-requests'),
    path('delete-request/<int:pk>/',views.delete_request,name='delete-request'),
    path('add-feedback',views.add_feedback,name='add-feedback'),
    path('feedbacks',views.view_feedback,name='feedbacks'),
    path('bill-pay/<int:id>/',views.pay_bill,name='bill-pay'),
    path('direct-pay/<int:id>/',views.pay_in_direct,name='direct-pay'),
]