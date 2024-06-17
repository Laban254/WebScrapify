from django.urls import path
from . import views
app_name = "webscrapify_app"
urlpatterns = [
            path('', views.home, name='home'),
            # path('accounts/login/', views.google_login_redirect, name='account_login'),
            path('scrape/', views.scrape, name='scrape'),
            path('download/', views.download_file, name='download_file'),
            path('schedule/', views.schedule_scrape, name='schedule_scrape'),
            # path('login/', views.login_view, name='login'),
            path('scheduled-tasks/', views.scheduled_tasks, name='scheduled_tasks'),
            
        ]
        