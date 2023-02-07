from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework import status


class ListCreateAPIViewMixin(ListCreateAPIView):
    related_model = None

    def get(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(user=request.user)
        return super().get(request, *args, **kwargs)
    

class RetrieveUpdateDestroyAPIViewMixin(RetrieveUpdateDestroyAPIView):

    def get(self, request, *args, **kwargs):
        try:
            self.queryset = self.queryset.filter(user=request.user)
            return super().retrieve(request, *args, **kwargs)
        except self.model.DoesNotExist:
            return Response({'message': 'object not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def patch(self, request, *args, **kwargs):
        try:
            self.queryset = self.queryset.filter(user=request.user)
            return super().partial_update(request, *args, **kwargs)
        except self.model.DoesNotExist:
            return Response({'message': 'object not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, *args, **kwargs):
        try:
            self.queryset = self.queryset.filter(user=request.user)
            return super().destroy(request, *args, **kwargs)
        except self.model.DoesNotExist:
            return Response({'message': 'object not found'}, status=status.HTTP_404_NOT_FOUND)
