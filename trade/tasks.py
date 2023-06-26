from userDashboard.models import User, Records
import random
from background_task import background
from datetime import timedelta
from django.utils import timezone
import atexit
from background_task.models import Task
import logging

# Configure logging
logging.basicConfig(level=logging.INFO) 


@background(schedule=timedelta(seconds=45))
def generate_profit_loss():
    users = User.objects.all()
    logging.warning(users.count())
    for user in users:
        profit_loss = round(random.uniform(-10, 10), 2)
        all_records = Records.objects.filter(user=user).order_by('-time')
        current_record = all_records.first()

        if not current_record:
            record = Records(
                initial_value = user.initial_deposit,
                profit_loss = 0.00,
                current_value = user.initial_deposit,
                user = user
            )
            record.save()
            logging.warning("saved")
        else:
            new_value = round((current_record.current_value + (current_record.current_value * profit_loss / 100)), 2)
            present_value = current_record.current_value
            record = Records(
                initial_value = current_record.current_value,
                profit_loss = profit_loss,
                current_value = present_value if not new_value > 0.00 else new_value,
                user = user,
                time=timezone.now()
            )
            if record.time >= (current_record.time + timedelta(minutes=1)):
                record.save()
                logging.warning("saved")
            
        logging.debug(f"updated user value {timezone.now()}")

generate_profit_loss()
