import pytest
from mainapp.models import Project, Blog, ProjectFact

@pytest.mark.django_db
def test_project_slug_creation():
    """Tests that a slug is auto-generated for a Project if not provided."""
    project = Project.objects.create(title="My Test Project", brief_description="Test")
    assert project.slug == "my-test-project"

@pytest.mark.django_db
def test_project_slug_uniqueness():
    """Tests that auto-generated project slugs are unique."""
    project1 = Project.objects.create(title="My Test Project", brief_description="Test")
    project2 = Project.objects.create(title="My Test Project", brief_description="Test")
    assert project1.slug == "my-test-project"
    assert project2.slug == "my-test-project-1"

@pytest.mark.django_db
def test_blog_slug_creation():
    """Tests that a slug is auto-generated for a Blog if not provided."""
    blog = Blog.objects.create(title="A Blog Post", summary="Summary")
    assert blog.slug == "a-blog-post"

@pytest.mark.django_db
def test_project_fact_uniqueness():
    """Tests the unique_together constraint on ProjectFact."""
    project = Project.objects.create(title="Project With Facts", brief_description="Test")
    ProjectFact.objects.create(project=project, key="Location", value="City A")
    with pytest.raises(Exception): # IntegrityError
        ProjectFact.objects.create(project=project, key="Location", value="City B")
