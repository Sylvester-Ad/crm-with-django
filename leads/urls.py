from django.urls import path
from . import views

app_name = "leads"
urlpatterns = [
    path("", views.LeadIndexView.as_view(), name="index"),
    path("<int:pk>/", views.LeadDetailView.as_view(), name="lead_detail"),
    path("<int:pk>/update/", views.LeadUpdateView.as_view(), name="lead_update"),
    path("<int:pk>/delete/", views.LeadDeleteView.as_view(), name="lead_delete"),
    path("<int:pk>/assign_agent", views.AssignAgentView.as_view(), name="assign_agent"),
    path("<int:pk>/category", views.LeadCategoryUpdateView.as_view(), name="lead_category_update"),
    path("create/", views.LeadCreateView.as_view(), name="lead_create"),
    path("categories/", views.CategoryListView.as_view(), name="category_list"),
    path("categories/<int:pk>/", views.CategoryDetailView.as_view(), name="category_detail"),
]
