from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Agent
from .serializers import AgentSerializer

@api_view(['POST'])
def register_agent(request):
    serializer = AgentSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Agent registered"})
    return Response(serializer.errors)

@api_view(['GET'])
def list_agents(request):
    agents = Agent.objects.filter(status='active')
    return Response(AgentSerializer(agents, many=True).data)

@api_view(['GET'])
def search_agents(request):
    capability = request.GET.get('capability')
    agents = Agent.objects.filter(capabilities__contains=[capability])
    return Response(AgentSerializer(agents, many=True).data)