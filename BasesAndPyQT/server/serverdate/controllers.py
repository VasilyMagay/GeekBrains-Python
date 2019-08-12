from datetime import datetime
from protocol import make_response
from decorators import logged, login_required


@logged
@login_required
def server_date_controller(request):
    return make_response(request, 200, datetime.now().timestamp())
