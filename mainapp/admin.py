from django.contrib import admin
from django.db.models import Sum
from django.utils.html import format_html
from .models import (
    ServiceCategory, Clientele, Testimonial, Testimonial, TeamMember, Leadership, HomepageTestimonial,
    Project, ProjectImage, ProjectFact, Blog, ContactSubmission, HitCount, ProjectHomeBanner
)

class ServiceCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')

@admin.register(Clientele)
class ClienteleAdmin(admin.ModelAdmin):
    list_display = ('name', 'website_url', 'created_at')


@admin.register(Leadership)
class LeadershipAdmin(admin.ModelAdmin):
    list_display = ('name', 'designation', 'photo_preview')
    search_fields = ('name', 'designation')
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
    save_on_top = False
    list_display = ('title', 'status', 'feature_on_project_page', 'created_at', 'main_image')
    list_filter = ('status', 'feature_on_project_page', 'created_at')
    search_fields = ('title', 'brief_description')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [ProjectImageInline, ProjectFactInline]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    save_on_top = False
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
        import csv
        from django.http import HttpResponse
        
        meta = self.model._meta
        field_names = ['first_name', 'last_name', 'email', 'mobile_number', 'message', 'submission_date']
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename={}.csv'.format(meta)
        writer = csv.writer(response)
        writer.writerow(field_names)
        for obj in queryset:
            row = writer.writerow([getattr(obj, field) for field in field_names])
        return response
    export_as_csv.short_description = "Export Selected as CSV"

class HitCountAdmin(admin.ModelAdmin):
    list_display = ('content_object', 'hits', 'created_at', 'last_hit')
    list_filter = ('created_at', 'content_type')
    readonly_fields = ('content_type', 'object_id', 'content_object', 'hits', 'created_at', 'last_hit')


@admin.register(ProjectHomeBanner)
class ProjectHomeBannerAdmin(admin.ModelAdmin):
    list_display = ('project', 'cement_eliminated', 'water_saved')
    search_fields = ('project__title', 'scope', 'tech_used', 'performance_impact')


@admin.register(HomepageTestimonial)
class HomepageTestimonialAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'customer_designation')
    search_fields = ('customer_name', 'customer_designation', 'testimonial')