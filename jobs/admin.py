from django.contrib import admin
from .models import Company, Job, SavedJob, JobAlert

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'industry', 'location')
    search_fields = ('name',)

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'job_type', 'location', 'source_platform', 'scraped_at')
    list_filter = ('job_type', 'source_platform', 'is_active')
    search_fields = ('title', 'company__name')

@admin.register(SavedJob)
class SavedJobAdmin(admin.ModelAdmin):
    list_display = ('user', 'job', 'status', 'created_at')

@admin.register(JobAlert)
class JobAlertAdmin(admin.ModelAdmin):
    list_display = ('user', 'keywords', 'frequency', 'is_active')