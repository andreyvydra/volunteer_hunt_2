from django.core.management.base import BaseCommand
from django.conf import settings
from django.urls import reverse_lazy
from django.utils import timezone
from telegram import Bot, Update
from telegram.ext import CallbackQueryHandler, Updater, CommandHandler
from telegram.utils.request import Request

from hackaton_test.settings import DATE_INPUT_FORMATS
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

            if volunteer:
                tasks = Task.objects.filter(volunteers=volunteer[0].id)
            else:
                employer = Employer.objects.filter(user_id=user.id)[0]
                tasks = employer.my_tasks.all()

            is_having_task_for_today = False
            for task in tasks:
                if timezone.now().date() == task.datetime.date():
                    is_having_task_for_today = True
                    output_msg += f"{task.name} в {task.datetime.astimezone().time()}" \
                                  f" (http://127.0.0.1:8000" \
                                  f"{reverse_lazy('task_view', kwargs={'pk': task.id})}) \n\n"

            if is_having_task_for_today:
                self.send_message(user.telegram_chat_id, output_msg)
            else:
                self.send_message(user.telegram_chat_id, 'Сегоня у вас нет никаких задач')

    def send_message(self, chat_id, msg):
        try:
            self.bot.send_message(chat_id, msg)
        except:
            print(f"Chat not found for {chat_id} {msg}")

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
