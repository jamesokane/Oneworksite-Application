from django.shortcuts import get_object_or_404
from django.http import Http404

def get_object_or_404_perms(cls, user, **kwargs):
    """
    Extended version of get_object_or_404() that returns a 404 if the non-admin
    or non-staff user does not match the `cls.user` field.
    """
    obj = get_object_or_404(cls, **kwargs)
    if not user.is_superuser and not user.is_staff:
        if obj.created_user != user:
            raise Http404
    return obj
