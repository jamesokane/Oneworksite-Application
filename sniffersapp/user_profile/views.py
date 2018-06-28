from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, DetailView, UpdateView
from django.urls import reverse
from extra_views import UpdateWithInlinesView, InlineFormSet
from invitations.models import Invitation

from .models import UserProfile

class UserListView(ListView):
    model = User

class UserDetailView(DetailView):
    model = User
    slug_field = slug_url_kwarg = 'username'

class UserProfileInline(InlineFormSet):
    model = UserProfile
    fields = ('name',)

class UserEditView(UpdateWithInlinesView):
    """
    Allows editing of the user instance while also inlining the UserProfile
    one-to-one model.
    """

    model = User
    inlines = [UserProfileInline]
    fields = ('first_name', 'last_name', 'email')

    def get_object(self):
        """
        Removes the need for providing <slug> or <pk> in urlpattern by fetching
        the current user object.
        """
        return self.request.user

    def get_success_url(self):
        return reverse('users:detail', kwargs={'username': self.object.username})

class PendingInvites(ListView):
     model = Invitation
     template_name = 'invitations/invitation_list.html'
     queryset = Invitation.objects.all().filter(accepted=0)

class AdminUpdateView(UpdateView):
    """
    TODO SK: refactor this
    """
    model = User
    fields = ['is_superuser', 'is_active', ]

def resend_invitation(request, pk):
    """
    Resend the invite email of  an existing invitation.
    """
    invite = get_object_or_404(Invitation, pk=pk)
    invite.send_invitation(request)
    messages.success(request, 'Invitation request re-sent to ' + invite.email)
    return redirect('users:pending-invites')
