from django.urls import path
from workers_app import views

urlpatterns = [
    path('worker_home/',views.worker_home,name='worker_home'),
    path('work-assigned/',views.work_assigned,name='work-assigned'),
    path('update-work-status/<int:pk>/',views.update_work_status,name='update-work-status'),
    path('profile/',views.profile_view,name='profile'),
    path('edit-profile/',views.update_profile,name='edit-profile'),
    path('feedbacks_wo/',views.view_feedback_worker,name='feedbacks_wo'),
]