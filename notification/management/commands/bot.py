from django.core.management.base import BaseCommand
from django.conf import settings
from django.urls import reverse_lazy
from django.utils import timezone
from telegram import Bot
from telegram.ext import Updater, CommandHandler
from tasks.models import Task
from user.models import Volunteer, User, Employer


class Command(BaseCommand):
    help = "Телеграм бот"

    def handle(self, *args, **options):
        updater = Updater(
            token=settings.TELEGRAM_BOT_TOKEN,
            use_context=True
        )
        updater.dispatcher.add_handler(CommandHandler('start', self.connect_user))

        self.bot = Bot(
            token=settings.TELEGRAM_BOT_TOKEN
        )
        job_queue = updater.job_queue
        job_queue.run_repeating(callback=self.send_notifications, interval=3600 * 12, first=1)

        updater.start_polling()
        updater.idle()

    def send_notifications(self, job):
        users = User.objects.all()
        for user in users:
            volunteer = Volunteer.objects.filter(user_id=user.id)
            output_msg = f"Добрый день, {user.username}!\n" \
                         f"Сегодня у вас следующие события: \n\n"
            self.send_message(user.telegram_chat_id, output_msg)

            if volunteer:
                tasks = Task.objects.filter(volunteers=volunteer[0].id)
            else:
                employer = Employer.objects.filter(user_id=user.id)[0]
                tasks = employer.my_tasks.all()

            for task in tasks:
                if timezone.now().date() != task.datetime.date():
                    new_msg = f"{task.name} в {task.datetime.astimezone().time()}" \
                               f" (http://127.0.0.1:8000" \
                               f"{reverse_lazy('task_view', kwargs={'pk': task.id})})"
                    lon, lat = task.point_on_map.split()
                    self.send_message(user.telegram_chat_id, new_msg)
                    self.send_location(user.telegram_chat_id, lon, lat)

    def send_message(self, chat_id, msg):
        try:
            self.bot.send_message(chat_id, msg)
        except:
            print(f"Chat not found for {chat_id} {msg}")

    def send_location(self, chat_id, lon, lat):
        try:
            self.bot.send_location(chat_id=chat_id, longitude=lon, latitude=lat)
        except:
            print(f"Chat not found for {chat_id} or incorrect lonLat ({lon}, {lat})")

    def connect_user(self, update, context):
        chat = update.message.chat
        user = User.objects.filter(telegram_id=chat.username)
        if user:
            user = user[0]
            user.telegram_chat_id = chat.id
            user.save()
            self.bot.send_message(chat.id, "Аккаунт успешно привязан к рассылке")
        else:
            self.bot.send_message(chat.id, "Аккаунт не зарегистрирован в системе")
