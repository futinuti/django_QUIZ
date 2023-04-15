from datetime import datetime, time, timedelta

from django.core.mail import send_mail
from django.core.management import BaseCommand
from django.utils import timezone
from django.utils.timezone import make_aware

from prettytable import PrettyTable

from quiz.models import Result


class Command(BaseCommand):
    help = "Send email to User reminder of unfinished tests"

    def handle(self, *args, **options):

        start = make_aware(datetime.combine(timezone.now() + timedelta(1), time()))

        results = Result.objects.filter(create_timestamp__lte=start, state=0).order_by('user')

        if results:
            tab = PrettyTable()
            tab.field_names = ['Username', 'Test', 'Correct/Incorrect', 'Points', 'Duration']
            user_current = results.first().user

            for result in results:

                if user_current == result.user:
                    tab.add_row([
                        result.user.username,
                        result.exam.title,
                        f'{result.num_correct_answers}/{result.num_incorrect_answers}',
                        result.points(),
                        f'{round((result.update_timestamp - result.create_timestamp).total_seconds())}s'
                    ])
                else:
                    subj = f"Report from {start.strftime('%Y-%m-%d')}"
                    send_mail(subject=subj, message=tab.get_string(), html_message=tab.get_html_string(),
                              from_email='admin@test.com', recipient_list=[user_current.email, ])
                    tab.clear_rows()
                    user_current = result.user
                    tab.add_row([
                        result.user.username,
                        result.exam.title,
                        f'{result.num_correct_answers}/{result.num_incorrect_answers}',
                        result.points(),
                        f'{round((result.update_timestamp - result.create_timestamp).total_seconds())}s'
                    ])
            subj = f"Report from {start.strftime('%Y-%m-%d')}"
            send_mail(subject=subj, message=tab.get_string(), html_message=tab.get_html_string(),
                      from_email='admin@test.com', recipient_list=[user_current.email, ])
            self.stdout.write("The report was sent by the admin`s email.")
        else:
            self.stdout.write("Nothing to send")
