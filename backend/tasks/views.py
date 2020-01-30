from django.http import JsonResponse, HttpResponse
from django.views import View
from django.views.generic import UpdateView
from django.views.decorators.csrf import csrf_exempt
from tasks.models import Todo
import json


class API_CRUD(UpdateView, View):
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super(API_CRUD, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if 'pk' in kwargs:
            pk = kwargs['pk']
            tasks = [Todo.objects.get(id=pk).to_dict()]
        else:
            tasks = [task.to_dict() for task in Todo.objects.all()]
        return JsonResponse({'tasks': tasks})
    
    def post(self, request, *args, **kwargs):
        params = json.loads(request.body)
        task = Todo(**params)
        task.save()
        return HttpResponse(status=201)

    def put(self, request, *args, **kwargs):
        pk = kwargs['pk']
        params = json.loads(request.body)
        task = Todo(id=pk, **params)
        task.save()
        return HttpResponse(status=201)

    def delete(self, request, *args, **kwargs):
        pk = kwargs['pk']
        Todo.objects.get(id=pk).delete()
        return HttpResponse(status=201)

