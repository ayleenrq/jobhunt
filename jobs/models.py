from django.db import models
from django.contrib.auth.models import User


class Company(models.Model):
    name = models.CharField(max_length=255)
    industry = models.CharField(max_length=100, blank=True)
    logo_url = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name


class Job(models.Model):
    JOB_TYPE_CHOICES = [
        ('internship', 'Magang'),
        ('fulltime', 'Full Time'),
        ('parttime', 'Part Time'),
        ('remote', 'Remote'),
    ]

    title = models.CharField(max_length=255)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='jobs')
    description = models.TextField(blank=True)
    salary_min = models.IntegerField(null=True, blank=True)
    salary_max = models.IntegerField(null=True, blank=True)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default='fulltime')
    location = models.CharField(max_length=100, blank=True)
    skills = models.JSONField(default=list)
    source_url = models.TextField(unique=True)
    source_platform = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    scraped_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.company.name}"


class SavedJob(models.Model):
    STATUS_CHOICES = [
        ('saved', 'Disimpan'),
        ('applied', 'Dilamar'),
        ('interview', 'Interview'),
        ('rejected', 'Ditolak'),
        ('offered', 'Ditawari'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_jobs')
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='saved_by')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='saved')
    notes = models.TextField(blank=True)
    applied_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'job')

    def __str__(self):
        return f"{self.user.username} - {self.job.title}"


class JobAlert(models.Model):
    FREQUENCY_CHOICES = [
        ('realtime', 'Real-time'),
        ('daily', 'Harian'),
        ('weekly', 'Mingguan'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_alerts')
    keywords = models.JSONField(default=list)
    filters = models.JSONField(default=dict)
    frequency = models.CharField(max_length=20, choices=FREQUENCY_CHOICES, default='daily')
    is_active = models.BooleanField(default=True)
    last_sent_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Alert {self.user.username} - {self.keywords}"