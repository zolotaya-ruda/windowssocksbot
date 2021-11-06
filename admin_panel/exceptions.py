class BotError(Exception):
    pass


class BotNotFound(BotError):
    def __str__(self, *args, **kwargs):
        return '[BotNotFound] --- Бот с такими параметрами на найден и будет создан сейчас.'
