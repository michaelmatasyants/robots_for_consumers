from django.conf.global_settings import DEFAULT_FROM_EMAIL

EMAIL = {
    'subject': '',
    'text': 'Добрый день!\n'
            'Недавно вы интересовались нашим роботом модели {model}, версии '
            '{version}.\nЭтот робот теперь в наличии. Если вам подходит этот '
            'вариант - пожалуйста, свяжитесь с нами.',
    'from_whom': DEFAULT_FROM_EMAIL,
}
