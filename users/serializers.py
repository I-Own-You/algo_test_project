from rest_framework import serializers
from users.models import User



class UserSerializer(serializers.HyperlinkedModelSerializer):

    cars = serializers.HyperlinkedRelatedField(many=True, view_name='car-detail', read_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'id', 'cars']
