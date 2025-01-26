from rest_framework import serializers
from projects.models import Project,Tag,Review
from users.models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Profile
        fields = '__all__'

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Tag
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Review
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):
    owner = ProfileSerializer(many=False)  #This way work when the field (owner, tags) is inside model (Project)
    tags = TagSerializer(many=True)
    reviews = serializers.SerializerMethodField()  #Using SerializerMethodField because Review model is a child of Project

    class Meta:
        model  = Project
        fields = '__all__'

    def get_reviews(self,obj):    #Standard Practice to make a member function to get all reviews related to the project
        reviews =obj.review_set.all()
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data
    


    