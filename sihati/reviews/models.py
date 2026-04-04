from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings


class DoctorReview(models.Model):
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='doctor_reviews'
    )
    doctor = models.ForeignKey(
        'accounts.DoctorProfile', on_delete=models.CASCADE, related_name='reviews'
    )
    appointment = models.OneToOneField(
        'doctors.Appointment', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='review'
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(blank=True)
    is_anonymous = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('patient', 'doctor', 'appointment')

    def __str__(self):
        return f"Avis {self.patient} → Dr.{self.doctor} ({self.rating}/5)"


class SellerReview(models.Model):
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='seller_reviews'
    )
    seller = models.ForeignKey(
        'accounts.SellerProfile', on_delete=models.CASCADE, related_name='reviews'
    )
    order = models.OneToOneField(
        'marketplace.Order', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='review'
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('patient', 'seller', 'order')

    def __str__(self):
        return f"Avis {self.patient} → {self.seller.business_name} ({self.rating}/5)"


class ReviewReply(models.Model):
    """Réponse d'un vendeur/médecin à un avis."""

    doctor_review = models.OneToOneField(
        DoctorReview, on_delete=models.CASCADE, null=True, blank=True, related_name='reply'
    )
    seller_review = models.OneToOneField(
        SellerReview, on_delete=models.CASCADE, null=True, blank=True, related_name='reply'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='review_replies'
    )
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Réponse de {self.author}"