from typing import Literal

    
class TranslatorRunner:
    def get(self, path: str, **kwargs) -> str: ...
    
    button: Button
    ask: Ask
    thanks: Thanks
    my: My
    edit: Edit
    user: User

    @staticmethod
    def click() -> Literal["""Нажми на кнопку"""]: ...

    @staticmethod
    def cancel() -> Literal["""Вернутся назад"""]: ...


class Button:
    my: ButtonMy
    order: ButtonOrder
    edit: ButtonEdit
    ask: ButtonAsk

    @staticmethod
    def cancel() -> Literal["""Вернуть назад"""]: ...


class ButtonMy:
    @staticmethod
    def profile() -> Literal["""Мой профиль"""]: ...


class ButtonOrder:
    an: ButtonOrderAn


class ButtonOrderAn:
    @staticmethod
    def order() -> Literal["""Заказ"""]: ...


class ButtonEdit:
    phone: ButtonEditPhone

    @staticmethod
    def email() -> Literal["""Почту"""]: ...


class ButtonEditPhone:
    @staticmethod
    def number() -> Literal["""Номер телефона"""]: ...


class ButtonAsk:
    phone: ButtonAskPhone


class ButtonAskPhone:
    @staticmethod
    def number() -> Literal["""Поделится номером"""]: ...


class Ask:
    order: AskOrder


class AskOrder:
    @staticmethod
    def text() -> Literal["""Введии текст заказа
Ограничения в 2000 символов"""]: ...


class Thanks:
    for_: ThanksFor_


class ThanksFor_:
    @staticmethod
    def order() -> Literal["""Спасибо за заказ!"""]: ...


class My:
    @staticmethod
    def profile(*, tid, username, datetime, phone_number, email) -> Literal["""Айди: &lt;code&gt;{ $tid }&lt;/code&gt;
Никнейм: { $username }
Дата регистрации: { $datetime }
Номер телефона: { $phone_number }
Эл. почта: { $email }

Для редактирования данных нажмите на соответствующую кнопку"""]: ...


class Edit:
    phone: EditPhone

    @staticmethod
    def email() -> Literal["""Введите свою почту"""]: ...

    @staticmethod
    def save() -> Literal["""Изменения сохранены"""]: ...


class EditPhone:
    @staticmethod
    def number() -> Literal["""Введите свой номер или нажмите «Поделиться номером»"""]: ...


class User:
    order: UserOrder


class UserOrder:
    no: UserOrderNo

    @staticmethod
    def data(*, text) -> Literal["""
Текст: { $text }"""]: ...


class UserOrderNo:
    @staticmethod
    def data(*, tid, username, text) -> Literal["""Айди: &lt;code&gt;{ $tid }&lt;/code&gt;
Никнейм: { $username }
Текст: { $text }"""]: ...

