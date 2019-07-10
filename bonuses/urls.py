from django.urls import path

from bonuses import views

urlpatterns = [
    path('user/detail/<int:pk>/', views.UserDetailView.as_view()),
    path('users/all/', views.UserListView.as_view()),
]
