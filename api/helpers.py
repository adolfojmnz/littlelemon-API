def user_is_requested_user(request):

    current_user_pk = request.user.pk
    requested_user_pk = request.parser_context['kwargs'].get('pk')
    if current_user_pk == requested_user_pk and requested_user_pk is not None:
        return True
    return False