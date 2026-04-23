import requests
import uuid
from rest_framework.decorators import api_view
from rest_framework.response import Response
from agents_registry.models import Agent
from .models import Task

@api_view(['POST'])
def handle_task(request):
    try:
        capability = request.data.get('capability')
        input_data = request.data.get('input', {})

        # 🔹 Validate input
        if not capability:
            return Response({"error": "Capability is required"}, status=400)

        if not isinstance(input_data, dict) or "text" not in input_data:
            return Response({"error": "Invalid input format. Expected {'text': '...'}"}, status=400)

        # 🔹 Find agent
        agent = Agent.objects.filter(
            capabilities__contains=[capability],
            status='active'
        ).first()

        if not agent:
            return Response({"error": f"No agent found for capability '{capability}'"}, status=404)

        # 🔹 Create task
        task_id = str(uuid.uuid4())

        payload = {
            "task_id": task_id,
            "capability": capability,
            "input": input_data,
            "context": {}
        }
        try:
            res = requests.post(agent.endpoint_url, json=payload, timeout=10)
            if res.status_code != 200:
                raise Exception(f"Agent returned status {res.status_code}")
            try:
                result = res.json()
            except Exception:
                raise Exception(f"Invalid JSON response from agent: {res.text}")

        except Exception as e:
            result = {
                "task_id": task_id,
                "status": "error",
                "result": None,
                "error": f"Agent call failed: {str(e)}"
            }

        # 🔹 Save task (always save, even on error)
        Task.objects.create(
            task_id=task_id,
            capability=capability,
            input_text=str(input_data),
            result=str(result.get("result")),
            status=result.get("status", "error"),
            error=result.get("error")
        )

        return Response(result)

    except Exception as e:
        return Response({
            "error": f"Server error: {str(e)}"
        }, status=500)


@api_view(['GET'])
def list_tasks(request):
    try:
        tasks = Task.objects.all().order_by('-created_at')

        data = []
        for t in tasks:
            data.append({
                "task_id": t.task_id,
                "capability": t.capability,
                "input": t.input_text,
                "result": t.result,
                "status": t.status,
                "error": t.error
            })

        return Response(data)

    except Exception as e:
        return Response({
            "error": f"Failed to fetch tasks: {str(e)}"
        }, status=500)