from django.core.exceptions import PermissionDenied

def check_docket_locked(docket):
    if docket.locked:
        raise PermissionDenied('This docket has been completed and is therefore locked.')
