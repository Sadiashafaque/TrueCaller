from rest_framework import serializers
from SpamCaller.models.models import RegisteredProfile, ContactsProfilesMapping, Contact,RandomSpam
from django.contrib.auth.models import User
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

class RegisteredProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = RegisteredProfile
        fields = ['user', 'phone', 'email', 'spam']

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(
            username=user_data['username'],
            password=user_data['password']
        )
        registered_profile = RegisteredProfile.objects.create(user=user, **validated_data)
        return registered_profile
    


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user is None:
                raise serializers.ValidationError("Invalid login credentials")
            if not user.is_active:
                raise serializers.ValidationError("User account is disabled.")
            data['user'] = user
        else:
            raise serializers.ValidationError("Must include 'username' and 'password'.")

        return data
    

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'

class ContactsProfilesMappingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactsProfilesMapping
        fields = '__all__'

class RandomSpamSerializer(serializers.ModelSerializer):
    class Meta:
        model = RandomSpam
        fields = '__all__'