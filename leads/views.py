from django.shortcuts import render
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Lead
from django.views import generic
from .forms import LeadForm, LeadModelForm, CustomUserCreationForm, AssignAgentForm, LeadCategoryUpdateForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from agents.mixins import OrganizerAndLoginRequiredMixin



# My class-based views.
class SignUpView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse("login")

class LandingPageView(generic.TemplateView):
    template_name = "landing.html"  

class LeadIndexView(LoginRequiredMixin, generic.ListView):
    template_name = "leads/index.html"
    context_object_name = "leads"

    def get_queryset(self):
        user = self.request.user
        
        # If the user is an organizer, show all leads in their organization
        if user.is_organizer:
            queryset = user.profile.leads.filter(
                agent__isnull=False  # Only show leads that have an agent assigned
            )

        # Filter leads by the agent associated with the logged-in user
        else:
            agent = user.agent_profile
            queryset = agent.assigned_leads.all()
            
        return queryset
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        user = self.request.user

        # Filter for unassigned leads
        if user.is_organizer:
            queryset = user.profile.leads.filter(
                agent__isnull=True
            )
            context.update({
                "unassigned_leads": queryset,
            })

        return context
        

class LeadDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "leads/lead_detail.html"
    context_object_name = "lead"

    def get_queryset(self):
        user = self.request.user
        agent = user.agent_profile
        
        # If the user is an organizer, show all leads in their organization
        if user.is_organizer:
            queryset = user.profile.leads.all()

        # Filter leads by the agent associated with the logged-in user
        else:
            queryset = agent.assigned_leads.all()
            
        return queryset

class LeadCreateView(OrganizerAndLoginRequiredMixin, generic.CreateView):
    template_name = "leads/lead_create.html"
    form_class = LeadModelForm

    def form_valid(self, form):
        user = self.request.user
        lead = form.save(commit=False)
        lead.organization = user.profile  # Set the organization to the user's profile
        lead.save()
        messages.success(self.request, "Lead created successfully!")
        send_mail(
            subject="A new lead has been created",
            message="Go to the admin panel to view the lead.",
            from_email="test@test.com",
            recipient_list=["test2@test.com"]
        )
        
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse("leads:index")
    
class LeadUpdateView(OrganizerAndLoginRequiredMixin, generic.UpdateView):
    template_name = "leads/lead_update.html"
    form_class = LeadModelForm
    context_object_name = "lead"

    def get_queryset(self):
        user = self.request.user
        
        # Show all leads in their organization
        queryset = user.profile.leads.all()
            
        return queryset
    
    def form_valid(self, form):
        messages.success(self.request, "Lead updated successfully!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("leads:index")

class LeadDeleteView(OrganizerAndLoginRequiredMixin, generic.DeleteView):
    template_name = "leads/lead_delete.html"
    context_object_name = "lead"

    def get_queryset(self):
        user = self.request.user
        
        # Initial queryset of all leads in their organization
        queryset = Lead.objects.filter(organization=user.profile)
            
        return queryset
    
    def form_valid(self, form):
        messages.success(self.request, "Lead successfully deleted!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("leads:index")
    
class AssignAgentView(OrganizerAndLoginRequiredMixin, generic.FormView):
    template_name = "leads/assign_agent.html"
    form_class = AssignAgentForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request

        return kwargs
    
    def form_valid(self, form):
        agent = form.cleaned_data["agent"]
        lead = Lead.objects.get(id=self.kwargs["pk"])
        lead.agent = agent
        lead.save()
        messages.success(self.request, f"You have successfully assigned agent {agent.user.username} to {lead.first_name}")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("leads:index")

class CategoryListView(LoginRequiredMixin, generic.ListView):
    template_name = "leads/category_list.html"
    context_object_name = "categories"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        agent = user.agent_profile

        if user.is_organizer:
            queryset = user.profile.leads.all()
        else:
            queryset = agent.organization.categories.all()
 
        context.update({
            "unassigned_lead_count": queryset.filter(category__isnull=True).count()
        })

        return context

    def get_queryset(self):
        user = self.request.user

        # Return queryset category of leads under user's organization
        if user.is_organizer:
            queryset = user.profile.categories.all()
        else:
            queryset = user.agent_profile.organization.categories.all()

        return queryset

class CategoryDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "leads/category_detail.html"
    context_object_name = "category"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        category = self.get_object()  

        # Get leads in this category
        if user.is_organizer:
            leads = category.leads.filter(organization=user.profile)
        else:
            leads = category.leads.filter(organization=user.agent_profile.organization)

        context.update({
            "leads": leads,
        })

        return context

    def get_queryset(self):
        user = self.request.user

        # Return queryset category of leads under user's organization
        if user.is_organizer:
            queryset = user.profile.categories.all()
        else:
            queryset = user.agent_profile.organization.categories.all()

        return queryset
    
class LeadCategoryUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "leads/lead_category_update.html"
    form_class = LeadCategoryUpdateForm
    context_object_name = "lead"

    def get_queryset(self):
        user = self.request.user
        
        # Return queryset of leads under user's organization
        if user.is_organizer:
            queryset = user.profile.leads.all()
        else:
            agent = user.agent_profile
            queryset = agent.assigned_leads.all()
            
        return queryset
    
    def form_valid(self, form):
        messages.success(self.request, "Lead category updated successfully!")
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("leads:lead_detail", kwargs={"pk": self.get_object().pk})

# My function-based views.

def landing_page(request):
    return render(request, "landing.html")

def index(request):
    leads = Lead.objects.all()

    return render(request, "leads/index.html", {
        "leads": leads,
    })

def lead_detail(request, pk):
    lead = Lead.objects.get(id=pk)


    return render(request, "leads/lead_detail.html", {
        "lead": lead,
    })

def lead_create(request):
    form = LeadModelForm()

    if request.method == "POST":
        form = LeadModelForm(request.POST)

        # Validate form
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("leads:index"))
    return render(request, "leads/lead_create.html", {
        "form": form
    })

def lead_update(request, pk):

    # Set form instance
    lead = Lead.objects.get(id=pk)
    form = LeadModelForm(instance=lead)

    # Update data of lead instance
    if request.method == "POST":
        form = LeadModelForm(request.POST, instance=lead)

        if form.is_valid():
            form.save()

            return HttpResponseRedirect(reverse("leads:index"))

    return render(request, "leads/lead_update.html", {
        "lead": lead,
        "form": form,
    })

def lead_delete(request, pk):
    lead = Lead.objects.get(id=pk)
    lead.delete()
    return HttpResponseRedirect(reverse("leads:index"))
    
    
# end def



# def lead_create(request):
#     form = LeadForm()

#     if request.method == "POST":
#         form = LeadForm(request.POST)

#         # Validate form
#         if form.is_valid():
#             print("The form is valid")
#             print(form.cleaned_data)
#             first_name = form.cleaned_data["first_name"]
#             last_name = form.cleaned_data["last_name"]
#             age = form.cleaned_data["age"]
#             agent = Agent.objects.first()

#             # Create the new lead in the database
#             Lead.objects.create(
#                 first_name=first_name,
#                 last_name=last_name,
#                 age=age,
#                 agent=agent
#             )
#             print("Lead created successfully in database")
#             return HttpResponseRedirect(reverse("leads:index"))
#     return render(request, "leads/lead_create.html", {
#         "form": form
#     })