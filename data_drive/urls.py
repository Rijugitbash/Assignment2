from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("", views.home, name="home"),
    path("user_dashboard/", views.dashboard, name="dashboard"),
    path('create_folder/', views.CreateFolderView.as_view(), name='create_folder'),
    path('show_folder/<int:folder_id>/', views.ShowFolderView.as_view(), name='show_folder'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('previous_page/<int:previous_id>/', views.previous_page, name='previous_page'),
]