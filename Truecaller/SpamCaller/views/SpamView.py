from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from SpamCaller.models.models import RegisteredProfile, Contact, RandomSpam
from SpamCaller.serializers import RandomSpamSerializer, RegisteredProfileSerializer, ContactSerializer

class MarkSpam(APIView):
    def get(self, request):
        spams=RandomSpam.objects.all()
        registeredSpam = RegisteredProfile.objects.filter(spam = True)
        contactspam = Contact.objects.filter(spam = True)
        combined_data = {
            "registed_numberss_spams" : RegisteredProfileSerializer(registeredSpam,many=True).data,
            "contact_spams" : ContactSerializer(contactspam,many=True).data,
            "random_numbers_Spams" : RandomSpamSerializer(spams,many=True).data
        }
        return Response(
			combined_data
		)
    
    def post(self, request):
        phone_number=request.data.get("phone_number")
        if phone_number is None:
            return Response(
				{
					"Error":"Phone number is not provided in request"
				},
				status = status.HTTP_400_BAD_REQUEST
			)
        contact = Contact.objects.filter(phone=phone_number).update(spam=True)
        profile = RegisteredProfile.objects.filter(phone=phone_number).update(spam=True)
        if (contact+profile):
             return Response(
				{
					"Message":"Contact marked as spam successfully!"
				},
				status = status.HTTP_200_OK
			)
        serialized = RandomSpamSerializer(data=request.data)
        if serialized.is_valid():
            serialized.save()
            return Response(
                {"Message":"Contact marked as random spam succesfully"}, 
                status=status.HTTP_201_CREATED)
        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
