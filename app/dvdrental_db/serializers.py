from rest_framework import serializers
from dvdrental_db.models import Movies


class TutorialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movies
        fields = ('id', 'title', 'genre', 'rating', 'description',
                  'year')
