from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    
    path('<str:username>/', views.profile, name='profile'), # 다른 기능들보다 아래에 있어야 함.
    path('<str:username>/follow/', views.follow, name='follow'),

]