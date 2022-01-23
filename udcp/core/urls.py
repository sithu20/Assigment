from django.urls import include, path, re_path
from rest_framework import routers
from core import views as userView



urlpatterns = [
    path('login/', userView.AuthToken.as_view(), name='token_obtain_pair'),
    path('register/', userView.RegisterView.as_view(), name='auth_register'),
    path('profile/', userView.user_detail, name='user_detail'),
    path('loginlogs/', userView.get_user_login_logs, name='user_login_logs'),
    path('alloccupation/', userView.OccupationList.as_view(), name='occupation'),
    path('user/<int:userid>/occupation/', userView.occupation, name='useroccupation'),
    path('occupation/', userView.OccupationDetail.as_view()),
    path('occupation/<int:pk>', userView.OccupationDetail.as_view()),
    path('deletememcode/', userView.deletemembercode),
    path('allusers/', userView.get_all_users, name='allusers'),
    path('alloccupation/', userView.RegisterView.as_view(), name='alloccupation'),
]
