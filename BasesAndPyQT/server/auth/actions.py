from .controllers import (
    get_users_controller, add_user_controller, del_user_controller,
    login_controller, registration_controller, logout_controller
)

actionnames = [
    {'action': 'get_users', 'controller': get_users_controller},
    {'action': 'add_user', 'controller': add_user_controller},
    {'action': 'del_user', 'controller': del_user_controller},
    {'action': 'login', 'controller': login_controller},
    {'action': 'registrate', 'controller': registration_controller},
    {'action': 'logout', 'controller': logout_controller},
]
