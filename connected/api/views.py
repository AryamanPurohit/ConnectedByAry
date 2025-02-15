from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from .serializers import ProjectSerializer
from projects.models import Project,Review,Tag
from rest_framework.permissions import IsAuthenticated


@api_view(['GET'])
def getRoutes(request):

    routes = [
        {'GET': 'api/projects'},
        {'GET': 'api/projects/id'},
        {'POST': 'api/projects/id/vote'},

        {'POST': 'api/users/token'},
        {'POST': 'api/users/token/refresh'},
    ]

    return Response(routes)

@api_view(['GET'])
def getProjects(request):
    projects = Project.objects.all()
    serializer = ProjectSerializer(projects, many=True)

    return Response(serializer.data)

@api_view(['GET'])
def getProject(request,pk):
    project = Project.objects.get(id=pk)
    serializer = ProjectSerializer(project, many=False)

    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def projectVote(request, pk):
    project = Project.objects.get(id=pk)
    user = request.user.profile     #This wont come from session id as usually, for api requests we are using JWT, so this will come from that token

    data = request.data
    
    review, created = Review.objects.get_or_create(
        owner = user, 
        project = project,

    )

    review.value = data['value']
    review.save()
    project.voteCount


    serializer = ProjectSerializer(project, many=False)

    return Response(serializer.data)

@api_view(['DELETE'])
def removeTag(request):
    tagid = request.data['tag']
    projectid = request.data['project']

    project = Project.objects.get(id=projectid)
    tag = Tag.objects.get(id=tagid)

    project.tags.remove(tag)

    return Response('Tag was Removed!')