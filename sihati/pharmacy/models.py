from django.db import models
from django.conf import settings


class MedicineCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Medicine categories'

    def __str__(self):
        return self.name


class Medicine(models.Model):
    name = models.CharField(max_length=200)
    generic_name = models.CharField(max_length=200, blank=True)
    category = models.ForeignKey(MedicineCategory, on_delete=models.SET_NULL, null=True, related_name='medicines')
    description = models.TextField(blank=True)
    dosage_form = models.CharField(max_length=100, blank=True)   # comprimé, sirop, injection...
    strength = models.CharField(max_length=100, blank=True)      # ex: 500mg
    requires_prescription = models.BooleanField(default=False)
    image = models.ImageField(upload_to='medicines/', null=True, blank=True)
    barcode = models.CharField(max_length=100, blank=True, unique=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} {self.strength}"


class PharmacyStock(models.Model):
    seller = models.ForeignKey(
        'accounts.SellerProfile', on_delete=models.CASCADE, related_name='pharmacy_stocks'
    )
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name='stocks')
    quantity = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_available = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('seller', 'medicine')

    def __str__(self):
        return f"{self.medicine} @ {self.seller.business_name} (qté: {self.quantity})"


class MedicineReservation(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'En attente'
        READY = 'ready', 'Prête'
        COLLECTED = 'collected', 'Récupérée'
        CANCELLED = 'cancelled', 'Annulée'
        EXPIRED = 'expired', 'Expirée'

    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='medicine_reservations'
    )
    stock = models.ForeignKey(PharmacyStock, on_delete=models.CASCADE, related_name='reservations')
    quantity = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Réservation {self.patient} – {self.stock.medicine}"


class MedicineDelivery(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'En attente'
        CONFIRMED = 'confirmed', 'Confirmée'
        IN_TRANSIT = 'in_transit', 'En livraison'
        DELIVERED = 'delivered', 'Livrée'
        CANCELLED = 'cancelled', 'Annulée'

    reservation = models.OneToOneField(
        MedicineReservation, on_delete=models.CASCADE, related_name='delivery'
    )
    delivery_address = models.TextField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    delivery_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    estimated_delivery_time = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Livraison – {self.reservation}"