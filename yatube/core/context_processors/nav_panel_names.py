def nav_panel_names(request):
    nav_names = [{'url': 'about:author', 'name': 'Об авторе'},
                 {'url': 'about:tech', 'name': 'Технологии'}]
    auth_nav_names = nav_names.copy() + (
        [
            {'url': 'posts:post_create', 'name': 'Новая запись'},
            {'url': 'users:password_change', 'name': 'Изменить пароль'},
            {'url': 'users:logout', 'name': 'Выйти'},
        ]
    )
    unauth_nav_names = nav_names.copy() + (
        [
            {'url': 'users:login', 'name': 'Войти'},
            {'url': 'users:signup', 'name': 'Регистрация'},
        ]
    )
    return {
        'authenticated_nav_panel_names': auth_nav_names,
        'unauthenticated_nav_panel_names': unauth_nav_names,
    }
