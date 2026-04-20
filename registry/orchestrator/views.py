import requests
import uuid
from rest_framework.decorators import api_view
from rest_framework.response import Response
from agents_registry.models import Agent
from .models import Task

@api_view(['POST'])
def handle_task(request):
    capability = request.data.get('capability')
    input_data = request.data.get('input')

    agent = Agent.objects.filter(
        capabilities__contains=[capability],
        status='active'
    ).first()

    if not agent:
        return Response({"error": "No agent found"})

    task_id = str(uuid.uuid4())

    payload = {
        "task_id": task_id,
        "capability": capability,
        "input": input_data,
        "context": {}
    }

    try:
        response = requests.post(agent.endpoint_url, json=payload)
        result = response.json()
    except Exception as e:
        result = {
            "task_id": task_id,
            "status": "error",
            "result": None,
            "error": str(e)
        }

    # ✅ SAVE TASK (THIS IS WHAT YOU ARE MISSING)
    Task.objects.create(
        task_id=task_id,
        capability=capability,
        input_text=str(input_data),
        result=result.get("result"),
        status=result.get("status"),
        error=result.get("error")
    )

    return Response(result)

@api_view(['GET'])
def list_tasks(request):
    tasks = Task.objects.all().order_by('-created_at')

    data = []
    for t in tasks:
        data.append({
            "task_id": t.task_id,
            "capability": t.capability,
            "input": t.input_text,
            "result": t.result,
            "status": t.status
        })

    return Response(data)