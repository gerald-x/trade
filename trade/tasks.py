from userDashboard.models import User, Records
import random
from background_task import background
from datetime import timedelta
from django.utils import timezone
import atexit
from background_task.models import Task

@background(schedule=timedelta(seconds=75))
def generate_profit_loss():
    users = User.objects.all()
    print(users.count())
    for user in users:
        profit_loss = round(random.uniform(-10, 10), 2)
        last_value = Records.objects.filter(user=user).order_by('-time').first()

        if not last_value:
            record = Records(
                initial_value = user.initial_deposit,
                profit_loss = 0.00,
                current_value = user.initial_deposit,
                user = user
            )
            record.save()
        else:
            new_value = round((last_value.current_value + (last_value.current_value * profit_loss / 100)), 2)
            present_value = last_value.current_value
            record = Records(
                initial_value = last_value.current_value,
                profit_loss = profit_loss,
                current_value = present_value if not new_value > 0.00 else new_value,
                user = user
            )
            record.save()
        print(f"updated user value {timezone.now()}")

import signal

def stop_background_task(signal, frame):
    Task.objects.filter(task_name='trade.task.generate_profit_loss').delete()


signal.signal(signal.SIGTERM, stop_background_task)
