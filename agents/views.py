import random

from django.shortcuts import render
from django.contrib import messages
from django.urls import reverse
from django.views import generic
from leads.models import Agent
from .forms import AgentModelForm
from .mixins import OrganizerAndLoginRequiredMixin
from django.core.mail import send_mail



class AgentListView(OrganizerAndLoginRequiredMixin, generic.ListView):
    """
    View to list all agents.
    Requires the user to be logged in.
    """
    model = Agent
    template_name = "agents/agent_list.html"
    context_object_name = "agents"

    def get_queryset(self):
        request_user_organization = self.request.user.profile
        return self.model.objects.filter(organization=request_user_organization)
    

class AgentCreateView(OrganizerAndLoginRequiredMixin, generic.CreateView):
    """
    View to create a new agent.
    Requires the user to be logged in.
    """
    template_name = "agents/agent_create.html"
    form_class = AgentModelForm
    
    def get_success_url(self):
        return reverse("agents:agent_list")
    
    def form_valid(self, form):
        
        # Create user and set the user as an agent
        user = form.save(commit=False)
        user.is_agent = True
        user.is_organizer = False
        user.set_password(f"{random.randint(0, 10000000)}")
        user.save()

        # Create agent instance and associate it with the user's organization
        Agent.objects.create(
            user=user,
            organization=self.request.user.profile
        )

        # Send mail to the new agent 
        send_mail(
            subject="You are invited to be an agent",
            message="You have been added as an agent in our system. Please log in to your account to start working.", 
            from_email="admin@test.com",
            recipient_list=[user.email],
        )

        messages.success(self.request, "Agent created successfully!")

        return super(AgentCreateView, self).form_valid(form)


class AgentDetailView(OrganizerAndLoginRequiredMixin, generic.DetailView):
    """
    View to display details of a specific agent.
    Requires the user to be logged in.
    """
    model = Agent
    template_name = "agents/agent_detail.html"
    context_object_name = "agent"

    def get_queryset(self):
        request_user_organization = self.request.user.profile
        return self.model.objects.filter(organization=request_user_organization)

class AgentUpdateView(OrganizerAndLoginRequiredMixin, generic.UpdateView):
    """
    View to update an existing agent.
    Requires the user to be logged in.
    """
    template_name = "agents/agent_update.html"
    context_object_name = "agent"
    form_class = AgentModelForm

    def get_queryset(self):
        user = self.request.user
        return user.profile.agents.all()

    def form_valid(self, form):
        messages.success(self.request, "Agent update successful!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("agents:agent_list")

    
class AgentDeleteView(OrganizerAndLoginRequiredMixin, generic.DeleteView):
    """
    View to delete an existing agent.
    Requires the user to be logged in.
    """
    model = Agent
    template_name = "agents/agent_delete.html"
    context_object_name = "agent"

    def get_queryset(self):
        request_user_organization = self.request.user.profile
        return self.model.objects.filter(organization=request_user_organization)
    
    
    def get_success_url(self):
        return reverse("agents:agent_list")
    
