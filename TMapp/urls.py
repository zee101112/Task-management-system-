from django.urls import path
from TMapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.landingPage, name='landingPage'),
    path('auth/', views.login_user, name='login_user'),
    path('login/', views.logout_user, name='logout_user'),

    path('dashboard/', views.home, name='home'),
    path('register/', views.Register, name='register_user'),

    path('forget-password/', views.reset_password, name='reset-password'),
    path('change-password/<token>', views.change_password, name='update-password'),
    
    path('verify/<token>', views.verify , name='verify'),

    path('users/', views.Users, name='users'),
    path('get_user_data/<int:user_id>/', views.get_user_data, name='get_user_data'),
    path('delete_user/', views.delete_user, name='delete_user'),
    path('verify_user/', views.verify_user, name='verify_user'),

    path('projects/', views.Projects, name='projects'),
    path('get_project_data/<int:project_id>/', views.get_project_data, name='get_project_data'),
    path('delete_project/', views.delete_project, name='delete_project'),
    
    
    path('tasks/', views.Tasks, name='tasks'),
    path('get_task_data/<int:task_id>/', views.get_task_data, name='get_task_data'),
    path('delete_task/', views.delete_project, name='delete_task'),

    path('profile/', views.profile_setting, name='profile'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)