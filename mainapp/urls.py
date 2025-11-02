from django.urls import path
from . import views

app_name = 'mainapp'

urlpatterns = [
    path('', views.HomepageView.as_view(), name='homepage'),
    path('projects/', views.ProjectListView.as_view(), name='project_list'),
    path('projects/<slug:slug>/', views.ProjectDetailView.as_view(), name='project_detail'),
    path('blog/', views.BlogListView.as_view(), name='blog_list'),
    path('blog/<slug:slug>/', views.BlogDetailView.as_view(), name='blog_detail'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('about/', views.AboutUsView.as_view(), name='about'),
    path('technology-products/', views.TechnologyProductsView.as_view(), name='technology_products'),
    path('services/', views.ServicesView.as_view(), name='services'),
    path('sustainability/', views.SustainabilityView.as_view(), name='sustainability'),
]
