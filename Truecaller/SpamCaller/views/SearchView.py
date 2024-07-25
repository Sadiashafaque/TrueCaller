from rest_framework.views import APIView
from rest_framework import generics, status
from rest_framework.response import Response
from SpamCaller.models.models import RegisteredProfile, Contact, RandomSpam,ContactsProfilesMapping
from rest_framework.exceptions import ValidationError
from SpamCaller.serializers import RandomSpamSerializer, RegisteredProfileSerializer, ContactSerializer
from django.contrib.auth.models import User

class SearchByName(APIView):
    def get(self,request):
        name=request.data.get("name")
        if name is None:
            return Response(
				{
					"Error":"Name is not present"
				}, 
                status = status.HTTP_400_BAD_REQUEST
			)
        profile_start=RegisteredProfile.objects.filter(user__username__startswith = name)
        profile_containing=RegisteredProfile.objects.filter(user__username__contains = name).exclude(user__username__startswith = name)
        contact_start=Contact.objects.filter(name__startswith = name)
        contact_containing=Contact.objects.filter(name__contains = name).exclude(name__startswith = name)

        profile_start_serialized = RegisteredProfileSerializer(profile_start,many=True).data
        profile_contain_serialized = RegisteredProfileSerializer(profile_containing,many=True).data
        contact_start_serialized = ContactSerializer(contact_start,many=True).data
        contact_contain_serialized = ContactSerializer(contact_containing,many=True).data

        profile_start_serialized.extend(profile_contain_serialized)
        profile_start_serialized.extend(contact_start_serialized)
        profile_start_serialized.extend(contact_contain_serialized)
        print(len(profile_contain_serialized))
        # if not profile_contain_serialized:
        #     return Response({"Message": "No profiles found"})
        return Response({'profiles': profile_start_serialized})
    

class SearchByNumber(APIView):
    def get(self, request):
        phone_number=request.data.get("phone_number")
        if phone_number is None:
            return Response(
				{
					"Error":"Name is not present"
				}, 
                status = status.HTTP_400_BAD_REQUEST
			)
        profile_search=RegisteredProfile.objects.filter(phone=phone_number)

        if profile_search:
            profile_search_serialized = RegisteredProfileSerializer(profile_search,many=True).data
            user_id_profile = profile_search.first().user
            mappings = ContactsProfilesMapping.objects.filter(profile=user_id_profile)
            contacts = [mapping.contact for mapping in mappings]
            contacts_serialized = ContactSerializer(contacts, many=True).data
            phone_numbers_all_contacts = [item.get('phone') for item in contacts_serialized]
            print(phone_numbers_all_contacts)

            user = request.user
            curr_user = RegisteredProfile.objects.filter(user=user)
            sererialized = RegisteredProfileSerializer(curr_user,many=True).data
            print(user)
            curr_user_phone = sererialized[0].get('phone')
            print(curr_user_phone)
            if curr_user_phone in phone_numbers_all_contacts:
                return Response({'Search Result(Contact is Registered and present in User)': profile_search_serialized})
            profiles_no_email = profile_search.values('id', 'user__username', 'phone', 'spam')
            return Response({'Search Result(Contact is Registered and not present in User)': profiles_no_email})
        
        contacts=Contact.objects.filter(phone=phone_number)
        if contacts:
            serialized_contacts = ContactSerializer(contacts,many=True).data
            return Response({'Contacts': serialized_contacts},status=status.HTTP_200_OK)
        spamnumber = RandomSpam.objects.filter(phone_number=phone_number)
        if spamnumber:
            sererialized_spam = RandomSpamSerializer(spamnumber,many=True).data
            for item in sererialized_spam:
                item['Name'] = 'Unknown'
            return Response({'Number found in random spam': sererialized_spam},status=status.HTTP_200_OK)
        return Response({'Error': "No contacts or profile found with given  number"},status=status.HTTP_404_NOT_FOUND)
        






        

