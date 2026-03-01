
from django.urls import path
from . import views
from .views import chatbot

urlpatterns = [
    path('', views.home, name='home'),

    path('categories/', views.notice_categories, name='notice_categories'),
    path('notices/category/<str:cat>/', views.notice_by_category, name='notice_by_category'),
    path('notices/', views.notice_list, name='notice_list'),
    path('create/', views.create_notice, name='create_notice'),
    path('notices/<int:pk>/', views.notice_detail, name='notice_detail'),
    path('notices/delete/<int:pk>/', views.delete_notice, name='delete_notice'),
    path('events/', views.all_events, name='all_events'),
    path('notices/update/<int:pk>/', views.update_notice, name='update_notice'),

    path('select/', views.choose_category, name='choose_category'),
    path('register/student/', views.register_student, name='register_student'),
    path('register/hod/', views.register_hod, name='register_hod'),
    path('register/staff/', views.register_staff, name='register_staff'),

    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('about/', views.about, name='about')

]
