class BrokerBaseException(Exception):
    default_text = "Проблема с брокером"

    def __init__(self, text: str = None, detail: str = None):
        if text is None:
            text = self.default_text
        self.text = text
        if detail:
            self.detail = detail.lower()
            self.text = f"{self.text}: {self.detail}"

    def __str__(self):
        return self.text


class RabbitMQNotConnected(BrokerBaseException):
    default_text = "Отсутствует подключение к RabbitMQ"


class BrokerNotSet(BrokerBaseException):
    default_text = "MessageBroker не задан в state FastAPI приложения"


class ChannelNotCreated(BrokerBaseException):
    default_text = "Новый channel в RabbitMQ не создан"


class MessagePublishException(BrokerBaseException):
    default_text = "Ошибка при отправке сообщений в брокер"


class DisallowedRequestMethod(BrokerBaseException):
    default_text = "Неразрешенный метод при обращении к эндпойнту"
