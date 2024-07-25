from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from SpamCaller.models.models import Contact, ContactsProfilesMapping, RegisteredProfile
from SpamCaller.serializers import ContactSerializer, ContactsProfilesMappingSerializer
from django.contrib.auth.models import User
# from rest_framework.permissions import IsAuthenticated
# from rest_framework_simplejwt.authentication import JWTAuthentication



class CreateContactAndMappingView(APIView):
    # authentication_classes = [JWTAuthentication]
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        
        user = User.objects.filter(username=request.user)
        user_contacts_mapping = ContactsProfilesMapping.objects.filter(profile = user[0])


        user_contacts = [mapping.contact for mapping in user_contacts_mapping]
        contacts_serialized = ContactSerializer(user_contacts, many=True).data
        print(contacts_serialized)
        return Response({
                            'contacts for current user': contacts_serialized,
                        },
                          status=status.HTTP_201_CREATED
                        )

    def post(self, request, *args, **kwargs):
        contact_serializer = ContactSerializer(data=request.data)
        if contact_serializer.is_valid():
            contact = contact_serializer.save()
            profile_id = request.user
            print(profile_id)
            if profile_id:
                try:
                    #profile = User.objects.get(id=profile_id)
                    mapping_serializer = ContactsProfilesMappingSerializer(data={
                        'profile': profile_id.id,
                        'contact': contact.id
                    })
                    if mapping_serializer.is_valid():
                        mapping_serializer.save()
                        return Response({
                            'contact': contact_serializer.data,
                            'mapping': mapping_serializer.data
                        }, status=status.HTTP_201_CREATED)
                    else:
                        contact.delete()
                        return Response(mapping_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                except User.DoesNotExist:
                    contact.delete()
                    return Response({'detail': 'Profile not found'}, status=status.HTTP_404_NOT_FOUND)
            else:
                contact.delete()
                return Response({'detail': 'Profile ID not provided'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(contact_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
