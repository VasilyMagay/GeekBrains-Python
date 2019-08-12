from protocol import make_response
from decorators import logged, login_required


@logged
@login_required
def server_error_controller(request):
    raise Exception('Server error message')
