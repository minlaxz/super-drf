# from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import exceptions, status
from rest_framework.permissions import AllowAny
from django_fsm import can_proceed
from .models import TodoTask
from .serializers import TodoTaskSerializer
import socket

# Create your views here.


class ApiIndexViewSet(ModelViewSet):
    queryset = TodoTask.objects.all()
    serializer_class = TodoTaskSerializer

    def get_queryset(self):
        queryset = TodoTask.objects.all()
        state = self.request.query_params.get("state", None)
        if state is not None:
            queryset = queryset.filter(state=state)
        return queryset

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.state == "Closed":
            return super().destroy(request, *args, **kwargs)
        raise exceptions.ValidationError(
            {"error": "Cannot delete an open task, please close it first."}
        )

    @action(detail=False, methods=["get"], permission_classes=[AllowAny])
    def test(self, request):

        return Response(
            {
              "message": f"{socket.gethostname()}",
              "isAnonymous": request.user.is_anonymous
            }
        )

    @action(detail=False, methods=["get"])
    def get_all_tasks(self, request):
        tasks = TodoTask.objects.all()
        serializer = TodoTaskSerializer(tasks, many=True, context={"request": request})
        return Response(serializer.data)

    @action(detail=False, methods=["post"])
    def create_task(self, request):
        serializer = TodoTaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["get"])
    def start_task(self, request, pk):
        task = self.get_object()
        if not can_proceed(task.trans_start):
            raise exceptions.ValidationError("Transition is not allowed")
        task.trans_start()
        task.save()
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"])
    def resolve_task(self, request, pk):
        task = self.get_object()
        if not can_proceed(task.trans_resolve):
            raise exceptions.ValidationError("Transition is not allowed")
        task.trans_resolve()
        task.save()
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"])
    def close_task(self, request, pk):
        task = self.get_object()
        if not can_proceed(task.trans_close):
            raise exceptions.ValidationError("Transition is not allowed")
        task.trans_close()
        task.save()
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=["get"])
    def reopen_task(self, request, pk):
        task = self.get_object()
        if not can_proceed(task.trans_reopen):
            raise exceptions.ValidationError("Transition is not allowed")
        task.trans_reopen()
        task.save()
        return Response(status=status.HTTP_200_OK)
