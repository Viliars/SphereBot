# VK LIBS
import vk_api.vk_api
from vk_api.bot_longpoll import VkBotLongPoll
from vk_api.bot_longpoll import VkBotEventType
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api import VkUpload
from vk_api.utils import get_random_id

class VKBot:
    def __init__(self, api_token, group_id, func):
        self.token = api_token
        self.group = group_id
        self.func = func
        # Для Long Poll
        self.vk_session = vk_api.VkApi(token=api_token)

        # Для загрузки файлов
        self.upload = VkUpload(self.vk_session)

        # Для использования Long Poll API
        self.long_poll = VkBotLongPoll(self.vk_session, group_id)

        # Для вызова методов vk_api
        self.vk = self.vk_session.get_api()

    def start(self):
        for event in self.long_poll.listen():  # Слушаем сервер

            # TODO сделать обработку иключений, чтобы бот не падал просто так

            # Создаем словарь параметров для передачи в функцию CoreBot`a
            params = {"ID": event.object.from_id,
                      "trigger": event.object.text.lower()}

            # Передаем данные в CoreBot и получаем ответ по протоколу
            try:
                answer = self.func(**params)
            except Exception as e:
                print(e)
                continue

            params = {"peer_id": answer['ID'], "random_id": get_random_id()}

            # Смотрим, существуют ли кнопки
            keyboard = answer.get('keyboard')
            if keyboard is not None:
                # Создаем VkKeyboard и добавляем туда кнопки, согласно протоколу
                buttons = VkKeyboard(one_time=False)
                for i, line in enumerate(keyboard):
                    for button in line:
                        buttons.add_button(button, color=VkKeyboardColor.PRIMARY)
                    if i + 1 < len(keyboard):
                        buttons.add_line()
                # Добавляем клавиатуру в параметры сообщения
                params.update({"keyboard": buttons.get_keyboard()})

            # Добавляем сообщение, если оно есть
            message = answer.get("message")
            if message is not None:
                params.update({"message": message})

            # TODO сделать поддержку вложений и стикеров
            # Отправляем сообщение пользователю
            files = answer.get('attachments')
            attachments = []
            if files is not None:
                photos = self.upload.photo_messages(photos=files)
                for photo in photos:
                    attachments.append(
                        'photo{}_{}'.format(photo['owner_id'], photo['id'])
                    )
                params.update({'attachment': ','.join(attachments)})

            self.vk.messages.send(**params)
