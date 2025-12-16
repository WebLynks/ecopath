from django.contrib import admin
from django.db.models import Sum
from django.utils.html import format_html
from .models import (
    ServiceCategory, Clientele, Testimonial, TeamMember, 
    Project, ProjectImage, ProjectFact, Blog, ContactSubmission, HitCount
)

@admin.register(ServiceCategory)
class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')

@admin.register(Clientele)
class ClienteleAdmin(admin.ModelAdmin):
    list_display = ('name', 'website_url', 'created_at')

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'author_title', 'is_featured', 'created_at')
    list_filter = ('is_featured',)
    search_fields = ('author_name', 'quote')

@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'order', 'photo_preview')
    list_editable = ('order',)
    readonly_fields = ('photo_preview',)

    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="100" />', obj.photo.url)
        return "(No photo)"
    photo_preview.short_description = 'Photo Preview'

class ProjectImageInline(admin.TabularInline):
    model = ProjectImage
    extra = 1
    ordering = ('order',)

class ProjectFactInline(admin.TabularInline):
    model = ProjectFact
    extra = 1

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'is_featured_home', 'created_at', 'hit_count_display')
    list_filter = ('status', 'is_featured_home', 'created_at')
    search_fields = ('title', 'brief_description')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProjectImageInline, ProjectFactInline]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        # Annotate with total hits to avoid N+1 queries in hit_count_display
        queryset = queryset.annotate(total_hits=Sum('hitcount__hits'))
        return queryset

    def hit_count_display(self, obj):
        return obj.total_hits or 0
    hit_count_display.short_description = 'Total Hits'
    hit_count_display.admin_order_field = 'total_hits'

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'published_date', 'hit_count_display')
    list_filter = ('status', 'published_date')
    search_fields = ('title', 'summary')
    prepopulated_fields = {'slug': ('title',)}

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(total_hits=Sum('hitcount__hits'))
        return queryset

    def hit_count_display(self, obj):
        return obj.total_hits or 0
    hit_count_display.short_description = 'Total Hits'
    hit_count_display.admin_order_field = 'total_hits'

@admin.register(ContactSubmission)
class ContactSubmissionAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'submission_date')
    list_filter = ('submission_date',)
    search_fields = ('first_name', 'last_name', 'email', 'message')
    readonly_fields = ('first_name', 'last_name', 'email', 'mobile_number', 'message', 'submission_date')
    actions = ['export_as_csv']

    def export_as_csv(self, request, queryset):
        # NOTE: A more robust implementation would use the csv module and stream the response.
        import csv
        from django.http import HttpResponse
        
        meta = self.model._meta
        # Limit exported fields to relevant submission fields
        field_names = ['first_name', 'last_name', 'email', 'mobile_number', 'message', 'submission_date']
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)
        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])
        return response
    export_as_csv.short_description = "Export Selected as CSV"

@admin.register(HitCount)
class HitCountAdmin(admin.ModelAdmin):
    list_display = ('content_object', 'hits', 'created_at', 'last_hit')
    list_filter = ('created_at', 'content_type')
    readonly_fields = ('content_type', 'object_id', 'content_object', 'hits', 'created_at', 'last_hit')
