from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate

from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *
from .serializers import *



class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({"detail": "email and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token

            return Response({
                "refresh": str(refresh),
                "access": str(access_token),
                'role':user.role
            }, status=status.HTTP_200_OK)
        else:
            return Response({"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)



class RegisterView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')

        if not username or not password:
            return Response({"detail": "email and password are required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.create_user(username=username,first_name=first_name,last_name=last_name, password=password)
            user.save()
        except Exception as e: 
            return Response({"detail": "something went wrong.","error":str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "User registered successfully."}, status=status.HTTP_201_CREATED)
    



class List_view(GenericAPIView):
    def get(self,request):
        try:
            users=FarmerRegistration.objects.all()
            serializer=FarmerListSerializer(users,many=True)
            return Response({'message':'success','data':serializer.data},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message':'a error occurred','error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
class OfficerList_view(GenericAPIView):
    def get(self,request):
        admin_approved=request.GET.get('admin_status')
        try:
            users=OfficerRegistration.objects.all()
            if admin_approved == 'true':
                users=users.filter(admin_approved=True)
            if admin_approved == 'false':
                users=users.filter(admin_approved=False)
            serializer=OfficerListSerializer(users,many=True)
            return Response({'message':'success','data':serializer.data},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message':'a error occurred','error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class Notice_single_view(GenericAPIView):
    def get(self,request):
        try:
            notice_id=request.GET.get('notice_id')
            users=Notice.objects.get(id=notice_id)
            serializer=NoticeSerializer(users)
            return Response({'message':'success','data':serializer.data},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message':'a error occurred','error':str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)


from django.core.mail import send_mail
import random
class RequestOTPView(APIView):
    def post(self, request):
        email = request.data.get("email")
        try:
            user = User.objects.get(email=email)
            otp = str(random.randint(100000, 999999))
            OTPVerification.objects.create(user=user, otp=otp)

            send_mail(
                "Password Reset OTP",
                f"Your OTP is: {otp}",
                "your-email@gmail.com",
                [email],
                fail_silently=False,
            )

            return Response({"message": "OTP sent to your email"}, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response({"error": "User with this email not found"}, status=status.HTTP_404_NOT_FOUND)



from rest_framework.permissions import AllowAny

class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")
        new_password = request.data.get("new_password")

        try:
            user = Profile.objects.get(email=email)
            otp_entry = OTPVerification.objects.filter(user=user, otp=otp).first()

            if otp_entry and otp_entry.is_valid():
                user.set_password(new_password)
                user.save()
                otp_entry.delete()
                return Response({"message": "Password reset successful"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid or expired OTP"}, status=status.HTTP_400_BAD_REQUEST)

        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
