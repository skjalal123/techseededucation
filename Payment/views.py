import uuid

from rest_framework.response import Response
from rest_framework.views import APIView
from Profile.models import myUser
from .models import Cart
from Course.models import Course
from Profile.Serializers import User
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
import json
from easebuzz_lib.easebuzz_payment_gateway import Easebuzz
from .Serializers import CartSerializer
from rest_framework import status
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
from datetime import datetime

"""
**************************************************************************
****************************** Ease Buzz *********************************
**************************************************************************
"""


class CartView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        user = request.user
        profile = myUser.objects.get(email=user.email)
        cart = Cart.objects.filter(student__email=user.email)
        userProfile = User(profile)
        amount = 0.00
        productinfo = []
        courseName = ''
        return Response(
            {"course_fee": amount, "productInfo": productinfo, "courseName": courseName, "user": userProfile.data})

    def post(self, request):
        courseUid = request.data
        email = self.request.user.email
        if 'course' in courseUid:
            previousCart = Cart.objects.filter(student__email=email, status__in=['PENDING', 'CANCEL'])
            if previousCart:
                for data in previousCart:
                    data.delete()
            course = Course.objects.get(uid=courseUid['course'])
            user = myUser.objects.get(email=email)
            cart = Cart(course=course, student=user, status="PENDING")
            cart.save()
            return Response(CartSerializer(cart).data, status=status.HTTP_201_CREATED)
        else:
            return Response({'course': 'course not found'}, status=status.HTTP_204_NO_CONTENT)


class Payment(APIView):
    # *************** Testing ******************
    MERCHANT_KEY = "2PBP7IABZ2"
    SALT = "DAH88E3UWQ"
    ENV = "test"
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    easebuzzObj = Easebuzz(MERCHANT_KEY, SALT, ENV)

    def get(self, request):
        user = request.user
        cart = Cart.objects.get(student__email=user.email, status="PENDING")
        productInfo = CartSerializer(cart)
        return Response({"productInfo": productInfo.data}, status=status.HTTP_200_OK)

    def post(self, request):
        postData = request.data
        postData['_mutable'] = False;
        postData['surl'] = "https://jocastaairobotics.com/payment/paymentapiresponse"
        postData['furl'] = "https://jocastaairobotics.com/payment/paymentapiresponse"
        final_response = self.easebuzzObj.initiatePaymentAPI(postData)
        result = json.loads(final_response)

        if result['status'] == 1:
            return Response(result['data'])
        else:
            return Response({'Error': result})

    # def put(self, request, pk, format=None):
    #
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PaymentAPIResponse(APIView):
    # *************** Production ******************
    MERCHANT_KEY = "91EMI5CYKC"
    SALT = "GKPCBVAJEU"
    ENV = 'prod'
    # *************** Testing ******************
    #MERCHANT_KEY = "2PBP7IABZ2"
    #SALT = "DAH88E3UWQ"
    #ENV = "test"
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [JWTAuthentication]

    easebuzzObj = Easebuzz(MERCHANT_KEY, SALT, ENV)

    def post(self, request):
        final_response = self.easebuzzObj.easebuzzResponse(request.POST)
        final_responseDict = json.loads(final_response)
        data = final_responseDict['data']
        cart = Cart.objects.get(id=data['txnid'], student__email=data['email'])
        url = "https://techseededucation.com/payment/"+data['txnid']
        if data['status'] == 'success':
            cart.status = 'SUCCESS'
            cart.confirm = datetime.now()
            cart.save()
            return redirect(to=url)
        else:
            cart.status = 'FAIL'
            cart.confirm = datetime.now()
            cart.save()
            return redirect(to=url)


class PaymentStatus(APIView):

    def get(self,request):
        uid = request.query_params['uid']
        try:
            cart = Cart.objects.get(id = uid)
            serialize = CartSerializer(cart).data
            return Response({"status":serialize['status']}, status=status.HTTP_202_ACCEPTED)
        except ObjectDoesNotExist:
            return Response({"not found": "Invoice not found"} , status=status.HTTP_204_NO_CONTENT)
