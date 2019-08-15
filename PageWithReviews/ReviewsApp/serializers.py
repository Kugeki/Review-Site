from rest_framework import serializers
from .models import Review, Person

class PersonSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100, required=False)
    account = serializers.CharField(max_length=200, required=False)

class ReviewSerializer(serializers.Serializer):
    blogger = PersonSerializer()
    person = PersonSerializer()
    content = serializers.CharField(max_length=1000)
    rating = serializers.IntegerField()

    def create(self, validated_data):
        blogger_data = validated_data.pop('blogger')
        blogger = Person.objects.create(**blogger_data)
        person_data = validated_data.pop('person')
        person = Person.objects.create(**person_data)
        review = Review.objects.create(blogger=blogger, person=person, **validated_data)
        return review
