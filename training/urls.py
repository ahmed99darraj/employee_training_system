from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Authentication URLs
    path('accounts/login/', auth_views.LoginView.as_view(template_name='training/login.html'), name='login'),
    path('accounts/logout/', views.logout_view, name='logout'),
    path('accounts/register/', views.register, name='register'),
    
    # Home page
    path('', views.dashboard, name='home'),
    
    # Dashboard Panel URLs
    path('dashboard/panel/', views.admin_panel, name='admin_panel'),
    
    # Instructor Management
    path('dashboard/instructors/', views.manage_instructors, name='manage_instructors'),
    path('dashboard/instructors/add/', views.add_instructor, name='add_instructor'),
    path('dashboard/instructors/<int:instructor_id>/edit/', views.edit_instructor, name='edit_instructor'),
    path('dashboard/instructors/<int:instructor_id>/delete/', views.delete_instructor, name='delete_instructor'),
    
    # User Management
    path('dashboard/users/', views.manage_users, name='manage_users'),
    path('dashboard/users/<int:user_id>/edit/', views.edit_user, name='edit_user'),
    path('dashboard/users/<int:user_id>/delete/', views.delete_user, name='delete_user'),
    
    # Office Management
    path('dashboard/offices/', views.manage_offices, name='manage_offices'),
    path('dashboard/offices/add/', views.add_office, name='add_office'),
    path('dashboard/offices/<int:office_id>/edit/', views.edit_office, name='edit_office'),
    path('dashboard/offices/<int:office_id>/delete/', views.delete_office, name='delete_office'),
    
    # Course Management
    path('dashboard/courses/', views.manage_courses, name='manage_courses'),
    path('dashboard/courses/add/', views.add_course, name='add_course'),
    
    # Course List and Details and Attendance
    path('courses/', views.course_list, name='course_list'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('courses/<int:course_id>/attendance/', views.mark_attendance, name='mark_attendance'),
    path('courses/<int:course_id>/attendance/summary/', views.attendance_summary, name='attendance_summary'),
    
    # Room Management
    path('dashboard/rooms/', views.manage_rooms, name='manage_rooms'),
    path('dashboard/rooms/add/', views.add_room, name='add_room'),
    path('dashboard/rooms/<int:room_id>/edit/', views.edit_room, name='edit_room'),
    path('dashboard/rooms/<int:room_id>/delete/', views.delete_room, name='delete_room'),
    
    # Password Reset
    path('password-reset/',
         auth_views.PasswordResetView.as_view(template_name='training/password_reset.html'),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='training/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='training/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='training/password_reset_complete.html'),
         name='password_reset_complete'),
    
    # Office Views
    path('offices/', views.office_list, name='office_list'),
    path('office/<int:office_id>/courses/', views.office_courses, name='office_courses'),
    
    # Course Enrollment
    path('enroll/<int:course_id>/', views.enroll_course, name='enroll_course'),
    path('my-courses/', views.my_courses, name='my_courses'),
]
