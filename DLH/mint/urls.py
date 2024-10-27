from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views


#html,views,url

urlpatterns =[
    path("", views.home, name="home"),
    path('join/', views.join, name='join'),
    path('login/', views.login, name='login'),
    path('meetup/<int:meetup_id>/', views.meetup_detail, name='meetup_detail'),
    path('manage_meetup', views.manage_meetup , name='manage_meetup'),
    path('add_meetup/', views.add_meetup, name='add_meetup'),
    path('update_meetup/<int:meetup_id>/', views.update_meetup, name='update_meetup'),
    path('delete_meetup/<int:meetup_id>/', views.delete_meetup, name='delete_meetup'),
    path('approve-registration/<int:registration_id>/', views.approve_registration, name='approve_registration'),
    path('reject-registration/<int:registration_id>/', views.reject_registration, name='reject_registration'),
    path('student_profile', views.student_profile, name='student_profile'),
    path('logout/', views.logout, name='logout'),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
