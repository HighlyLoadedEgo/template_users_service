from enum import Enum


class MessageExchanges(str, Enum):
    USERS_MAILING = "users-mailing"


class MessageRoutingKey(str, Enum):
    MAILING_WELCOME = "mailing.welcome"
    MAILING_UPDATE = "mailing.update"
    MAILING_DELETE = "mailing.delete"
    MAILING_LOGIN = "mailing.login"
