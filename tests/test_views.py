import pytest
from django.urls import reverse
from django.core import mail
from unittest.mock import patch

from mainapp.models import Project, Blog, ContactSubmission, ServiceCategory

@pytest.mark.django_db
def test_homepage_view(client):
    url = reverse('mainapp:homepage')
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_project_list_view(client):
    url = reverse('mainapp:project_list')
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_project_detail_hit_count(client):
    project = Project.objects.create(title="Hit Count Test", status='PUBLISHED', brief_description="Test")
    url = reverse('mainapp:project_detail', kwargs={'slug': project.slug})
    
    with patch('mainapp.models.HitCount.objects.increment') as mock_increment:
        response = client.get(url)
        assert response.status_code == 200
        mock_increment.assert_called_once()

@pytest.mark.django_db
def test_contact_view_post_success():
    """Tests successful submission of the contact form."""
    ServiceCategory.objects.create(name='General Inquiry')
    url = reverse('mainapp:contact')
    form_data = {
        'first_name': 'John',
        'last_name': 'Doe',
        'email': 'john.doe@example.com',
        'service_inquiry': ServiceCategory.objects.first().pk,
        'message': 'This is a test message.'
    }

    # Use pytest-django's client fixture
    from django.test import Client
    client = Client()
    response = client.post(url, form_data)

    assert response.status_code == 302 # Should redirect on success
    assert 'success=1' in response.url
    assert ContactSubmission.objects.count() == 1
    submission = ContactSubmission.objects.first()
    assert submission.email == 'john.doe@example.com'
    assert submission.notified is True # Because email sending is mocked to succeed
    assert len(mail.outbox) == 1 # Check that one email was sent
    assert mail.outbox[0].subject == 'New Contact Inquiry from John Doe'

@pytest.mark.django_db
@patch('mainapp.views.send_mail', side_effect=Exception("SMTP Error"))
def test_contact_view_post_email_failure(mock_send_mail):
    """Tests that the submission is saved even if email sending fails."""
    ServiceCategory.objects.create(name='General Inquiry')
    url = reverse('mainapp:contact')
    form_data = {
        'first_name': 'Jane',
        'last_name': 'Doe',
        'email': 'jane.doe@example.com',
        'service_inquiry': ServiceCategory.objects.first().pk,
        'message': 'Another test message.'
    }

    from django.test import Client
    client = Client()
    response = client.post(url, form_data)

    assert response.status_code == 302
    assert 'success=1' in response.url
    assert ContactSubmission.objects.count() == 1
    submission = ContactSubmission.objects.first()
    assert submission.email == 'jane.doe@example.com'
    assert submission.notified is False # Should be False on email failure
    assert len(mail.outbox) == 0 # No email should be sent
