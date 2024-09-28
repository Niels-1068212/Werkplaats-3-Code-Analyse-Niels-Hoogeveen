from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from datetime import date


class Toezichthouders(models.Model):
    ervaringsdeskundige = models.IntegerField(blank=True, null=True)
    voornaam_1 = models.TextField()
    achternaam_1 = models.TextField()
    telefoonnummer_1 = models.TextField()
    voornaam_2 = models.TextField(blank=True, null=True)
    achternaam_2 = models.TextField(blank=True, null=True)
    telefoonnummer_2 = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = "Toezichthouders"


class User(AbstractUser):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    postcode = models.CharField(max_length=10)
    geslacht = models.CharField(
        max_length=10, choices=[("M", "Man"), ("V", "Vrouw"), ("0", "Anders")]
    )
    email = models.EmailField()
    telefoonnummer = models.CharField(max_length=100)
    geboortedatum = models.DateField()
    gebruikte_hulpmiddelen = models.TextField(max_length=200)
    bijzonderheden = models.TextField(max_length=100, default="", blank=True)
    beschikbaar_vanaf = models.DateTimeField()
    beschikbaar_tot = models.DateTimeField()
    bijzonderheden_beschikbaarheid = models.TextField(
        max_length=100, blank=True
        )
    username = models.CharField(max_length=100, unique=True)
    voorkeur_benadering = models.CharField(max_length=20)
    status = models.CharField(max_length=10, default=1)
    opmerking_verwijderd = models.TextField(blank=True, null=True)
    datum_goedgekeurd = models.DateTimeField(blank=True, null=True)
    goedegekeurd_door = models.CharField(max_length=100, null=True)
    # userpermission
    groups = models.ManyToManyField(
        Group,
        verbose_name="groups",
        related_name="user_groups",
        blank=True,
        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name="user permissions",
        related_name="user_user_permissions",
        blank=True,
        help_text="Specific permissions for this user.",
        related_query_name="user",
    )

    def age(self):
        date_today = date.today()
        leeftijd = (
            date_today.year
            - self.geboortedatum.year
            - (
                (date_today.month, date_today.day)
                < (self.geboortedatum.month, self.geboortedatum.day)
            )
        )
        return leeftijd


class BeperkingenErvaringsdeskundigen(models.Model):
    beperking_id = models.IntegerField()
    ervaringsdeskundigen_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = "Beperkingen_ervaringsdeskundigen"


class BeperkingenOnderzoeken(models.Model):
    onderzoeks_id = models.IntegerField()
    beperking_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = "Beperkingen_onderzoeken"
