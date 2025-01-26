from django.db import models
import uuid
from users.models import Profile
# Create your models here.

class Project(models.Model):

    owner = models.ForeignKey(Profile,null=True, blank=True, on_delete=models.CASCADE) #1 To N reln between a Profile and Project (A profile can have many projects)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True,blank=True) #null for DB and blank for django forms

    image = models.ImageField(null=True, blank=True, default='default.jpg')
    demo_link = models.CharField(max_length=10000, null=True, blank=True)
    source_link= models.CharField(max_length=10000,null=True,blank=True)
    tags = models.ManyToManyField('Tag',blank=True) # N to N reln b/w Project and Tag models
    vote_total = models.IntegerField(null=True, blank=True, default=0)
    vote_ratio = models.IntegerField(null=True, blank=True, default=0)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.title
    class Meta:
        ordering = ['-vote_ratio' , '-vote_total']

    @property
    def voteCount(self):
        reviews = self.review_set.all()
        upVotes = reviews.filter(value='up').count()
        total = reviews.count()

        ratio = (upVotes/total)*100
        self.vote_total = total
        self.vote_ratio = ratio
        self.save()

    @property
    def reviewers(self):
        setOfReviewers = self.review_set.all().values_list('owner__id', flat =True)
        return setOfReviewers
    
class Review(models.Model):
    VOTE_TYPE =(
        ('up','Up Vote'),
        ('down','Down Vote'),
    )

    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)  # 1 to N reln (A project can have Many reviews)
    body = models.TextField(null=True,blank=True)
    value = models.CharField(max_length=100, choices=VOTE_TYPE)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    class Meta:
        unique_together = [['owner', 'project']]

    def __str__(self):
        return self.value
    
class Tag(models.Model):
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name


