from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from tasks.models import Todo
from rest_framework.parsers import JSONParser
from tasks.serializers import TaskSerializer 
import q

@csrf_exempt
def api_CR(request):
    if request.method == 'GET':
        tasks = [task.to_dict() for task in Todo.objects.all()]
        # tasks = Todo.objects.all()
        # serializer = TaskSerializer(tasks, many=True)
        return JsonResponse({'tasks': tasks})

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = TaskSerializer(data=data)
        # q.d()
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

@csrf_exempt
def api_UD(request, uid):
    try:
        task = Todo.objects.get(pk=uid)
    except Todo.DoesNotExist:
        return HttpResponse(status=404)
    
    if request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = TaskSerializer(task, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    if request.method == 'DELETE':
        task.delete()
        return HttpResponse(status=204)