import pytest
from django.contrib.admin.sites import AdminSite
from mainapp.admin import ProjectAdmin, ProjectImageInline, ProjectFactInline
from mainapp.models import Project

@pytest.mark.django_db
def test_project_admin_inlines():
    """Tests that ProjectImageInline and ProjectFactInline are registered with ProjectAdmin."""
    site = AdminSite()
    project_admin = ProjectAdmin(Project, site)
    
    assert ProjectImageInline in project_admin.inlines
    assert ProjectFactInline in project_admin.inlines
