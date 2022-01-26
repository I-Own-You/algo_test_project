from dataclasses import fields
from rest_framework import serializers
from products.models import Car, Images


class CarSerializer(serializers.HyperlinkedModelSerializer):

    owner = serializers.ReadOnlyField(source='owner.email')
    image = serializers.HyperlinkedRelatedField(many=True,view_name='images-detail',read_only=True)

    class Meta:
        model = Car
        fields = ['id', 'owner', 'image', 'name', 'description', 'price', 'date_added', 'date_changed', 'url']

class ImagesSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Images
        fields = ['id', 'owner', 'images']
