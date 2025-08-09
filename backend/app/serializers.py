from rest_framework import serializers
from .models import AskModel, QuestionModel, FactModel, SayingModel

class AskSerializer(serializers.ModelSerializer):
    class Meta:
        model = AskModel
        fields = ['question', 'prediction']
        
class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionModel
        fields = "__all__"

class FactSerializer(serializers.ModelSerializer):
    class Meta:
        model = FactModel
        fields = ["id", "text", "likes", "dislikes"]

class SayingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SayingModel
        fields = ["id", "text", "author", "likes", "dislikes"]
