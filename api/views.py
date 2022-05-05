# from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import exceptions, status
from django_fsm import can_proceed
from .models import TodoTask
from .serializers import TodoTaskSerializer
# Create your views here.

class ApiIndexViewSet(ModelViewSet):
    queryset = TodoTask.objects.all()
    serializer_class = TodoTaskSerializer

    def get_queryset(self):
        queryset = TodoTask.objects.all()
        state = self.request.query_params.get('state', None)
        if state is not None:
            queryset = queryset.filter(state=state)
        return queryset

    @action(detail=False, methods=['get'])
    def get_all_tasks(self, request):
        tasks = TodoTask.objects.all()
        serializer = TodoTaskSerializer(tasks, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def create_task(self, request):
        serializer = TodoTaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['get'])
    def start_task(self, request, pk):
        task = self.get_object()
        if not can_proceed(task.trans_start):
            raise exceptions.PermissionDenied('Transition is not allowed')
        task.trans_start()
        task.save()
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def resolve_task(self, request, pk):
        task = self.get_object()
        if not can_proceed(task.trans_resolve):
            raise exceptions.PermissionDenied('Transition is not allowed')
        task.trans_resolve()
        task.save()
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def close_task(self, request, pk):
        task = self.get_object()
        if not can_proceed(task.trans_close):
            raise exceptions.PermissionDenied('Transition is not allowed')
        task.trans_close()
        task.save()
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def reopen_task(self, request, pk):
        task = self.get_object()
        if not can_proceed(task.trans_reopen):
            raise exceptions.PermissionDenied('Transition is not allowed')
        task.trans_reopen()
        task.save()
        return Response(status=status.HTTP_200_OK)
