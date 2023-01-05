def nav_panel_names(request):
    list = [{'url': 'about:author', 'name': 'Об авторе'},
            {'url': 'about:tech', 'name': 'Технологии'}]
    auth_list = list.copy() + (
        [
            {'url': 'posts:post_create', 'name': 'Новая запись'},
            {'url': 'users:password_change', 'name': 'Изменить пароль'},
            {'url': 'users:logout', 'name': 'Выйти'},
        ]
    )
    unauth_list = list.copy() + (
        [
            {'url': 'users:login', 'name': 'Войти'},
            {'url': 'users:signup', 'name': 'Регистрация'},
        ]
    )
    return {
        'authenticated_nav_panel_names': auth_list,
        'unauthenticated_nav_panel_names': unauth_list,
    }
