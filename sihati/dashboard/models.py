from django.db import models
from django.conf import settings


class Report(models.Model):
    class ReportType(models.TextChoices):
        APPOINTMENTS = 'appointments', 'Rendez-vous'
        ORDERS = 'orders', 'Commandes'
        USERS = 'users', 'Utilisateurs'
        REVENUE = 'revenue', 'Chiffre d\'affaires'
        STOCK = 'stock', 'Stock'
        REVIEWS = 'reviews', 'Avis'

    class Period(models.TextChoices):
        DAILY = 'daily', 'Journalier'
        WEEKLY = 'weekly', 'Hebdomadaire'
        MONTHLY = 'monthly', 'Mensuel'
        CUSTOM = 'custom', 'Personnalisé'

    generated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='reports'
    )
    report_type = models.CharField(max_length=30, choices=ReportType.choices)
    period = models.CharField(max_length=20, choices=Period.choices)
    date_from = models.DateField()
    date_to = models.DateField()
    data = models.JSONField(default=dict)
    file = models.FileField(upload_to='reports/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Rapport {self.report_type} ({self.date_from} → {self.date_to})"


class DashboardWidget(models.Model):
    """Permet à chaque utilisateur de personnaliser son tableau de bord."""

    class WidgetType(models.TextChoices):
        STAT_CARD = 'stat_card', 'Carte statistique'
        BAR_CHART = 'bar_chart', 'Graphique barres'
        LINE_CHART = 'line_chart', 'Graphique lignes'
        PIE_CHART = 'pie_chart', 'Graphique camembert'
        TABLE = 'table', 'Tableau'

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='dashboard_widgets'
    )
    widget_type = models.CharField(max_length=20, choices=WidgetType.choices)
    title = models.CharField(max_length=100)
    config = models.JSONField(default=dict)    # data source, filters, time range, etc.
    position_x = models.PositiveSmallIntegerField(default=0)
    position_y = models.PositiveSmallIntegerField(default=0)
    width = models.PositiveSmallIntegerField(default=1)
    height = models.PositiveSmallIntegerField(default=1)
    is_visible = models.BooleanField(default=True)

    class Meta:
        ordering = ['position_y', 'position_x']

    def __str__(self):
        return f"Widget '{self.title}' – {self.user}"