from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from .models import Job, SavedJob, JobAlert
from .serializers import JobSerializer, SavedJobSerializer, JobAlertSerializer
from django.contrib.auth.models import User
from rest_framework import status

class JobListView(generics.ListAPIView):
    serializer_class = JobSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = Job.objects.filter(is_active=True).select_related('company')
        q = self.request.query_params.get('q')
        job_type = self.request.query_params.get('type')
        location = self.request.query_params.get('location')
        platform = self.request.query_params.get('platform')

        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) |
                Q(description__icontains=q) |
                Q(company__name__icontains=q) |
                Q(skills__contains=[q])
            )
        if job_type:
            queryset = queryset.filter(job_type=job_type)
        if location:
            queryset = queryset.filter(location__icontains=location)
        if platform:
            queryset = queryset.filter(source_platform=platform)

        return queryset.order_by('-scraped_at')


class JobDetailView(generics.RetrieveAPIView):
    queryset = Job.objects.filter(is_active=True).select_related('company')
    serializer_class = JobSerializer
    permission_classes = [permissions.AllowAny]


class SavedJobListView(generics.ListCreateAPIView):
    serializer_class = SavedJobSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SavedJob.objects.filter(user=self.request.user).select_related('job__company')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SavedJobDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SavedJobSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SavedJob.objects.filter(user=self.request.user)


class JobAlertListView(generics.ListCreateAPIView):
    serializer_class = JobAlertSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return JobAlert.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        
        
class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email', '')

        if not username or not password:
            return Response(
                {'error': 'Username dan password wajib diisi'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(username=username).exists():
            return Response(
                {'error': 'Username sudah dipakai'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.create_user(
            username=username,
            password=password,
            email=email
        )

        return Response(
            {'message': f'User {user.username} berhasil dibuat'},
            status=status.HTTP_201_CREATED
        )