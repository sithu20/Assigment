from django.contrib.auth.models import User, Group
import datetime, time

from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView

from django.http import Http404
from . import serializers as userSerializer
from .models import UserOccupation as UOP, UserProfile as UP, UserLoginAudit as ULA



class RegisterView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request, format='json'):
        serializer = userSerializer.RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                context = {
                    "Status": {
                        "Code": "01",
                        "Message": "Success"
                    },
                    'Message': 'Register Successfully',
                    "Error": None,
                    "ResponseTime": time.strftime("%Y%m%d%H%M%S"),
                    'Data': serializer.data,
                }
                return Response(context, status=status.HTTP_201_CREATED)
        else:
            context = {
                "Status": {
                    "Code": "500",
                    "Message": "Fail"
                },
                "Error": serializer.errors,
                "ResponseTime": time.strftime("%Y%m%d%H%M%S"),
            }

            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET','POST'])
def user_detail(request):
    if request.method == 'GET':
        try:
            userobj = User.objects.get(pk=request.user.pk)
            userProfile = UP.objects.get(user=request.user)
            occupation = UOP.objects.filter(user=request.user)
            userGroup =[]
            groupQuery = Group.objects.filter(user = request.user)
            for g in groupQuery:
                userGroup.append(g.name)
            profileData = {
                "ID": request.user.pk,
                "userName": userobj.username,
                "userEmail": userobj.email,
                "userMemcode": userProfile.memcode,
                "userOccupation": list(occupation),
                "userGroup":userGroup
            }

            context = {
                "Status": {
                    "Code": "01",
                    "Message": "Success"
                },
                "Error": None,
                "ResponseTime": time.strftime("%Y%m%d%H%M%S"),
                "Data": profileData,
            }

            return Response(context, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            context = {
                "Status": {
                    "Code": "404",
                    "Message": "Fail"
                },
                "Error": "User Not Found",
                "ResponseTime": time.strftime("%Y%m%d%H%M%S")
            }
            return Response(context, status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'POST':
        pass



@api_view(['GET'])
def occupation(request,userid):
    if request.method == 'GET':
        try:
            userobj = User.objects.get(pk=userid)
            occupation = UOP.objects.filter(user=userobj)
            useroccupation = []
            for op in occupation:
                useroccupation.append(
                    {
                        "id": op.pk,
                        "occupation": op.ocpName,
                        "salary":op.ocpSalary,
                        "createdby":op.createBy,
                        "createdDate":op.createDate
                    }
                )

            context = {
                "Status": {"Code": "01","Message": "Success"},
                "Error": None,
                "ResponseTime": time.strftime("%Y%m%d%H%M%S"),
                "Data": useroccupation
            }
            return Response(context, status=status.HTTP_200_OK)
        except:
            context = {
                "Status": {"Code": "404","Message": "Fail"},
                "Error": "User Does Not Exist.",
                "ResponseTime": time.strftime("%Y%m%d%H%M%S")
            }
        return Response(context, status=status.HTTP_404_NOT_FOUND)

class AuthToken(TokenObtainPairView):
    serializer_class = userSerializer.TokenObtainPairSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = userSerializer.UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = userSerializer.GroupSerializer
    permission_classes = [permissions.IsAuthenticated]


class OccupationList(APIView):
    def get(self, request, format=None):
        occupations = UOP.objects.all()
        serializer = userSerializer.OccupationSerializer(occupations, many=True)

        context = {
            "Status": {"Code": "01", "Message": "Success"},
            "Error": None,
            "ResponseTime": time.strftime("%Y%m%d%H%M%S"),
            "Data": serializer.data
        }
        return Response(context, status=status.HTTP_200_OK)


class OccupationDetail(APIView):
    """
    Retrieve, update or delete
    """

    #def get_object(self, pk):

    def post(self, request, format='json'):
        requestData = request.data
        requestData['createBy'] = request.user.pk

        if 'user' in requestData and "ocpName" in requestData and "ocpSalary" in requestData:
            if request.user.groups.filter(name='normal').exists():
                requestData['user'] = request.user.pk

            serializer = userSerializer.OccupationSerializer(data=requestData)

            if serializer.is_valid():
                serializer.save()
                context = {
                    "Status": {"Code": "01", "Message": "Successfully Created"},
                    "Error": None,
                    "ResponseTime": time.strftime("%Y%m%d%H%M%S"),
                    "Data": serializer.data
                }
                return Response(context, status=status.HTTP_201_CREATED)
            else:
                context = {
                    "Status": {"Code": "500", "Message": "Fail"},
                    "Error": serializer.errors,
                    "ResponseTime": time.strftime("%Y%m%d%H%M%S")
                }
                return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            context = {
                "Status": {"Code": "500", "Message": "Fail"},
                "Error": "Incomplete Data",
                "ResponseTime": time.strftime("%Y%m%d%H%M%S")
            }
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, pk, format=None):
        try:
            occupation = UOP.objects.get(pk=pk)
            serializer = userSerializer.OccupationSerializer(occupation)
            if serializer.data:
                context = {
                    "Status": {"Code": "01", "Message": "Success"},
                    "Error": None,
                    "ResponseTime": time.strftime("%Y%m%d%H%M%S"),
                    "Data": serializer.data
                }
                return Response(context, status=status.HTTP_200_OK)

            return UOP.objects.get(pk=pk)
        except UOP.DoesNotExist:
            context = {
                "Status": {"Code": "404", "Message": "Fail"},
                "Error": "Not Found",
                "ResponseTime": time.strftime("%Y%m%d%H%M%S")
            }
            return Response(context, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk, format=None):

        try:
            occupation = UOP.objects.get(pk=pk)
            serializer = userSerializer.OccupationSerializer(occupation, data=request.data)

            if request.user.groups.filter(name='normal').exists() and request.data['user'] != request.user.pk:
                context = {
                    "Status": {"Code": "408", "Message": "Bad Request"},
                    "Error": "User can only update their occupation.Not allow to edit others",
                    "ResponseTime": time.strftime("%Y%m%d%H%M%S")
                }
                return Response(context, status=status.HTTP_400_BAD_REQUEST)

            if serializer.is_valid():
                serializer.save()
                if serializer.data:
                    context = {
                        "Status": {"Code": "01", "Message": "Successfully updated."},
                        "Error": None,
                        "ResponseTime": time.strftime("%Y%m%d%H%M%S"),
                        "Data": serializer.data
                    }

                return Response(context, status=status.HTTP_200_OK)

            context = {
                "Status": {"Code": "500", "Message": "Internal Server Error"},
                "Error": serializer.errors,
                "ResponseTime": time.strftime("%Y%m%d%H%M%S")
            }
            return Response(context, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except UOP.DoesNotExist:
            context = {
                "Status": {"Code": "404", "Message": "Fail"},
                "Error": "Not Found",
                "ResponseTime": time.strftime("%Y%m%d%H%M%S")
            }
            return Response(context, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk, format=None):
        ocp = self.get_object(pk)

        if request.user.groups.filter(name='normal').exists() and request.data['user'] != request.user.pk:
            context = {
                "Status": {"Code": "408", "Message": "Bad Request"},
                "Error": "User can only delete their occupation.Not allow to delete others",
                "ResponseTime": time.strftime("%Y%m%d%H%M%S")
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

        ocp.delete()

        context = {
            "Status": {"Code": "204", "Message": "Successfully Deleted."},
            "Error": None,
            "ResponseTime": time.strftime("%Y%m%d%H%M%S")
        }
        return Response(context, status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def deletemembercode(request):
    if request.method == 'POST':
        try:
            #userobj = User.objects.get(pk=userid)
            userProfile = UP.objects.get(user=request.user)
            userProfile.memcode=None
            userProfile.save()

            context = {
                "Status": {"Code": "01","Message": "Successfully Deleted"},
                "Error": None,
                "ResponseTime": time.strftime("%Y%m%d%H%M%S")
            }
            return Response(context, status=status.HTTP_200_OK)
        except:
            context = {
                "Status": {"Code": "404","Message": "Fail"},
                "Error": "User Does Not Exist.",
                "ResponseTime": time.strftime("%Y%m%d%H%M%S")
            }
        return Response(context, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def get_user_login_logs(request):
    if request.method == 'GET':
        try:

            if request.user.groups.filter(name='admin').exists():
                loginlogs = ULA.objects.all()
                logsdata = []
                for ll in loginlogs:
                    logsdata.append(
                        {
                            "id":ll.pk,
                            "email":ll.emailaddress,
                            "agentinfo":ll.user_agent_info,
                            "status":ll.status,
                            "ip":ll.ip,
                            "datetime":ll.loginDateTime
                        }
                    )
                context = {
                    "Status": {"Code": "01","Message": "Success"},
                    "Error": None,
                    "ResponseTime": time.strftime("%Y%m%d%H%M%S"),
                    "Data":list(logsdata),
                }
            else:
                context = {
                    "Status": {"Code": "200", "Message": "Success"},
                    "Error": "Not Allow to Access for normal user!",
                    "ResponseTime": time.strftime("%Y%m%d%H%M%S")
                }
            return Response(context, status=status.HTTP_200_OK)
        except:
            context = {
                "Status": {"Code": "404","Message": "Fail"},
                "Error": "Logs Not Exist.",
                "ResponseTime": time.strftime("%Y%m%d%H%M%S")
            }
        return Response(context, status=status.HTTP_404_NOT_FOUND)



@api_view(['GET'])
def get_all_users(request):
    if request.method == 'GET':
        try:
            userobj = User.objects.all()
            #userProfile = UP.objects.get(user=request.user)
            #occupation = UOP.objects.filter(user=userobj)
            users = []
            for usr in userobj:
                users.append(
                    {
                        "id": usr.pk,
                        "email": usr.email,
                        "profile": str(request.get_host())+"/profile/"+str(usr.pk),
                        "occupation": str(request.get_host())+"/user/" + str(usr.pk)+"/occupation/"
                    }
                )

            context = {
                "Status": {"Code": "01","Message": "Success"},
                "Error": None,
                "ResponseTime": time.strftime("%Y%m%d%H%M%S"),
                "Data": users
            }
            return Response(context, status=status.HTTP_200_OK)
        except:
            context = {
                "Status": {"Code": "404","Message": "Fail"},
                "Error": "User Does Not Exist.",
                "ResponseTime": time.strftime("%Y%m%d%H%M%S")
            }
        return Response(context, status=status.HTTP_404_NOT_FOUND)