from decorators import logged
from auth.decorators import login_required


@logged
@login_required
def server_error_controller(request):
    raise Exception('Server error message')
