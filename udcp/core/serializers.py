from django.contrib.auth.models import User, Group
from rest_framework import exceptions, serializers
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken, SlidingToken, UntypedToken
from django.views.decorators.csrf import csrf_exempt
from .models import UserProfile, UserLoginAudit, UserOccupation
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.validators import UniqueValidator
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.password_validation import validate_password
import datetime, time
from django.contrib.auth import authenticate, user_logged_in
import re


class OccupationSerializer(serializers.ModelSerializer):
    #user = serializers.PrimaryKeyRelatedField( read_only=True)

    class Meta:
        model = UserOccupation
        fields = ['id', 'user', 'ocpName', 'ocpSalary', 'createBy', 'createDate']





class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)

        # Add custom claims
        token['email'] = user.email
        return token


class PasswordField(serializers.CharField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('style', {})
        kwargs['style']['input_type'] = 'password'
        kwargs['write_only'] = True

        super().__init__(*args, **kwargs)


class TokenObtainSerializer(serializers.Serializer):
    email_field = User.EMAIL_FIELD
    #businessentity_field = BusinessEntity.pk
    default_error_messages = {
        'no_active_account': ' Default No active account found with the given credentials'
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[self.email_field] = serializers.CharField()
        self.fields['password'] = PasswordField()

    def validate(self, attrs):
        authenticate_kwargs = {
            self.email_field: attrs[self.email_field],
            'password': attrs['password'],
        }

        try:
            authenticate_kwargs['request'] = self.context['request']
        except KeyError:
            pass



        self.user = authenticate(**authenticate_kwargs)

        if self.user is None or not self.user.is_active:
            raise exceptions.AuthenticationFailed(
                self.error_messages['no_active_account'],
                'no_active_account',
            )

        return {}

    @classmethod
    def get_token(cls, user):
        raise NotImplementedError('Must implement `get_token` method for `TokenObtainSerializer` subclasses')



class TokenObtainPairSerializer(TokenObtainSerializer):
    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    @csrf_exempt
    def validate(self, attrs):
        data = super().validate(attrs)

        user_logged_in.send(sender=self.user.__class__, request=self.context['request'], user=self.user)

        try:
            userProfile = UserProfile.objects.get(user=self.user)


            if userProfile:
                refresh = self.get_token(self.user)
                data['refresh'] = str(refresh)
                data['access'] = str(refresh.access_token)


                return data
            else:
                error = { "detail xxx": "No active account found with the given credentials...."}
                return error
        except:
            error = { "detail ee": "No active account found with the given credentials"}
            return error


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email','password', 'password2')


    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})


        return attrs

    def create(self, validated_data):
        split_email = validated_data['email'].split("@", 1)
        username = str(split_email[0])
        emaildomain = split_email[1]

        user = User.objects.create(
            username=username,
            email=validated_data['email']
        )

        user.set_password(validated_data['password'])
        user.save()

        up = UserProfile.objects.create(
            user=user,
        )

        if emaildomain == "sinw.com":
            userGroup = Group.objects.get(name="admin")
            userGroup.user_set.add(user)
            up.memcode="ADM"
        else:
            userGroup = Group.objects.get(name="normal")
            userGroup.user_set.add(user)
            up.memcode = "NRM"

        up.save()


        #return Response(context, status=status.HTTP_200_OK)
        return user



class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']
