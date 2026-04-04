from django.db import models
from django.conf import settings


class Notification(models.Model):
    class NotifType(models.TextChoices):
        APPOINTMENT_CONFIRMED = 'appt_confirmed', 'RDV confirmé'
        APPOINTMENT_REFUSED = 'appt_refused', 'RDV refusé'
        APPOINTMENT_CANCELLED = 'appt_cancelled', 'RDV annulé'
        APPOINTMENT_REMINDER = 'appt_reminder', 'Rappel RDV'
        ORDER_STATUS = 'order_status', 'Statut commande'
        RESERVATION_READY = 'reservation_ready', 'Réservation prête'
        DELIVERY_UPDATE = 'delivery_update', 'Mise à jour livraison'
        ACCOUNT_VALIDATED = 'account_validated', 'Compte validé'
        NEW_REVIEW = 'new_review', 'Nouvel avis'
        STOCK_LOW = 'stock_low', 'Stock faible'
        SYSTEM = 'system', 'Système'

    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications'
    )
    notif_type = models.CharField(max_length=30, choices=NotifType.choices)
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)

    # Generic link to the related object (optional)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    object_type = models.CharField(max_length=50, blank=True)   # 'appointment', 'order', ...

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Notif → {self.recipient} : {self.title}"


class NotificationPreference(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notif_preferences'
    )
    email_enabled = models.BooleanField(default=True)
    sms_enabled = models.BooleanField(default=False)
    push_enabled = models.BooleanField(default=True)

    # Granular switches per type
    appointment_reminders = models.BooleanField(default=True)
    order_updates = models.BooleanField(default=True)
    new_reviews = models.BooleanField(default=True)
    promotions = models.BooleanField(default=False)

    def __str__(self):
        return f"Préférences notif – {self.user}"