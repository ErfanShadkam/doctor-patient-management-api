from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "is_doctor", "is_patient"]
        extra_kwargs = {
            "is_doctor":{'read_only':True},
            "is_patient":{'read_only':True},
        }




    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.is_patient = True
        user.is_doctor = False
        user.save()
        return user

class MakeDoctorSerializer(serializers.Serializer):
    message = serializers.CharField(max_length=200)