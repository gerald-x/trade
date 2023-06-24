from django.apps import AppConfig


class UserdashboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'userDashboard'

    def ready(self):
        # Start the background task when the server starts
        from trade.tasks import generate_profit_loss
        generate_profit_loss()