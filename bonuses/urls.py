from django.urls import path

from bonuses import views

urlpatterns = [
    path('users/detail/<int:pk>/', views.UserDetailView.as_view()),
    path('users/all/', views.UserListView.as_view()),
    path('bonuses/increase/', views.OperationIncreaseView.as_view()),
    path('bonuses/decrease/', views.OperationDecreaseView.as_view()),
    path('bonuses/multiple-increase/', views.MultipleIncreaseOperationView.as_view()),
]
