from django.urls import path
from . import views

urlpatterns = [

    path('', views.dashboard, name="dashboard"),

    path('login/', views.user_login, name="login"),
    path('register/', views.register, name="register"),
    path('logout/', views.user_logout, name="logout"),

    path('submit/', views.submit_complaint, name="submit"),
    path('track/', views.track_complaint, name="track"),

    path('update/<int:id>/', views.update_status, name="update"),
    path('delete/<int:id>/', views.delete_complaint, name="delete"),

    path('download/<int:id>/', views.download_report, name="download"),

    # ✅ THESE FIX YOUR ERROR
    path('pending/', views.pending_list, name="pending"),
    path('progress/', views.progress_list, name="progress"),
    path('resolved/', views.resolved_list, name="resolved"),
]