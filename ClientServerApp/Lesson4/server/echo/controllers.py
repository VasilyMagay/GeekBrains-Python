from protocol import make_response
from decorators import logged, login_required


@logged
@login_required
def echo_controller(request):
    data = request.get('data')
    return make_response(request, 200, data)
