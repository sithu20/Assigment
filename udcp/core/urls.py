from django.urls import include, path, re_path
from rest_framework import routers
from core import views as userView


'''

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
'''

router = routers.SimpleRouter()
router.register(r'users', userView.UserViewSet)
router.register(r'groups', userView.GroupViewSet)



# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    #path('api-auth/', include('rest_framework.urls', namespace='rest___framework'))

    #path('token-auth/', include('rest_auth.urls'), name='token_obtain_pair')
    #path('token-auth/', TokenObtainPairView.as_view(), name='admintoken_obtain_pair'),
    path('login/', userView.AuthToken.as_view(), name='token_obtain_pair'),
    path('register/', userView.RegisterView.as_view(), name='auth_register'),
    path('profile/', userView.user_detail, name='user_detail'),

    path('alloccupation/', userView.OccupationList.as_view(), name='occupation'),
    path('user/<int:userid>/occupation/', userView.occupation, name='useroccupation'),
    path('occupation/', userView.OccupationDetail.as_view()),
    path('occupation/<int:pk>', userView.OccupationDetail.as_view()),
    path('deletememcode/', userView.deletemembercode),



    path('membercode/', userView.RegisterView.as_view(), name='membercode'),
    path('allusers/', userView.RegisterView.as_view(), name='allusers'),
    path('alloccupation/', userView.RegisterView.as_view(), name='alloccupation'),





]
