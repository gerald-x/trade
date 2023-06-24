from django.apps import AppConfig


class AdmindashboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'adminDashboard'

    def ready(self):
        # Start the background task when the server starts
        from trade.tasks import generate_profit_loss
        generate_profit_loss()