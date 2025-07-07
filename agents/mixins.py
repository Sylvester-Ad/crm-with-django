from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect


class OrganizerAndLoginRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated and is an organizer."""

    def dispatch(self, request, *args, **kwargs):

        # Check if the user is authenticated and is an organizer
        if not request.user.is_authenticated or not request.user.is_organizer:
            return redirect("leads:index")
        return super().dispatch(request, *args, **kwargs)