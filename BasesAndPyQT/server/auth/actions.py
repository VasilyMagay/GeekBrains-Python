from .controllers import (
    get_users_controller, add_user_controller, del_user_controller
)

actionnames = [
    {'action': 'get_users', 'controller': get_users_controller},
    {'action': 'add_user', 'controller': add_user_controller},
    {'action': 'del_user', 'controller': del_user_controller},
]
