import datetime
import dateutil.parser
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.contrib.gis.db.models import Q
from rest_framework import serializers


class UserManager(BaseUserManager):

    def create_user(self, clientcode, password=None, **extra_fields):
        """Creates and save a new user"""

        user = self.model(clientcode=clientcode, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, clientcode, password):
        """
        Creates a superuser
        """
        user = self.create_user(clientcode, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self.db)

        return user


class User(AbstractBaseUser, PermissionsMixin):

    """Custom user model"""

    clientcode = models.CharField(
        _ ('Code client'), max_length=255, unique=True)
    societe = models.CharField(
        _('Société'), max_length=255, null=True, blank=True)
    email = models.EmailField(
        _('adresse mail'),
        max_length=255, unique=True, null=True,)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    canOrder = models.BooleanField(default=False)
    last_name = models.CharField(_('Nom'), max_length=255, blank=True)
    first_name = models.CharField(_('Prénom'), max_length=255, blank=True)
    objects = UserManager()

    USERNAME_FIELD = 'clientcode'
    _original_canOrder = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._original_canOrder = self.canOrder

    def __str__(self):
        return f" {self.clientcode} {self.last_name} {self.societe}"


AVICOLE = 'AVICOL'
BOVIN = 'BOVIN'
CAPRIN = 'CAPRIN'
EQUIN = 'EQUIN'
HELICICOLE = "HELICI"
OVIN = 'OVIN'
PALMIDE = 'PALMID'
PORCIN = 'PORCIN'
DIVERS = 'DIVERS'

TYP_CHOICES = (
    (AVICOLE, 'Avicole sauf canard'),
    (BOVIN, 'Bovin'),
    (CAPRIN, 'Caprin'),
    (EQUIN, 'Equin'),
    (HELICICOLE, 'Hélicicole'),
    (OVIN, 'Ovin'),
    (PALMIDE, 'Palmidés'),
    (PORCIN, 'Porcin'),
    (DIVERS, 'Divers')
)


class Cat(models.Model):

    """
    catégories d'utilisateur
    FABRICANT  crée, modifie, autorise, fabricant, client, élévage, commande, valide la commande pour le compte d'un client
    COMMERCIAL crée, modifie, commercial, client, élevage, commande,
    CLIENT modifie client, crée modifie commande si pas validée par fabricant, crée, supprime chef d'élevage
    CHEF-ELEV crée modifie commande pour un élevage donné si pas validée par fabricant,
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        verbose_name="Utilisateur",
        on_delete=models.CASCADE)
    FABRICANT = 'FABRIC'
    COMMERCIAL = 'COMMER'
    CLIENT = 'CLIENT'
    CHEF_ELEVAGE = 'CH_ELE'
    CHAUFFEUR = 'CHAUFF'

    CAT_CHOICES = (
        (FABRICANT, 'Fabricant'),
        (COMMERCIAL, 'Commercial'),
        (CLIENT, 'Client'),
        (CHEF_ELEVAGE, "Chef d'élevage"),
        (CHAUFFEUR, 'Chauffeur')
    )
    cat = models.CharField("catégorie", max_length=6,
                           choices=CAT_CHOICES, default="CLIENT")

    def __str__(self):
        return self.cat


class Chef_elev(User):
    """
    Creates a user associated with a Client, this Chef_elev will
    only be allowed to place orders for one Elevage,
    """
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   verbose_name='créateur',
                                   related_name='créateur',
                                   on_delete=models.CASCADE,
                                   null=True,
                                   blank=True
                                   )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def elevage(self):
        elev = Elevage.objects.get(Chef_elev=self.id)
        return elev.nom


class Product(models.Model):
    """Defines products"""
    produit = models.CharField(
        _('Nom du produit'), max_length=255
    )
    ref = models.CharField(
        _('Référence'), max_length=255
    )

    cat = models.CharField("Type d'élevage", max_length=6,
                           choices=TYP_CHOICES, default=None)

    def __str__(self):
        return f"{self.ref} {self.produit}"


class Elevage(models.Model):
    """Defines Elevage associated with Client"""
    nom = models.CharField(_('Nom ou localisation élévage'), max_length=255)
    typ_elevage = models.CharField("Type d'élevage", max_length=6,
                                   choices=TYP_CHOICES, default=None)
    chef_elev = models.ManyToManyField(User,
                                       verbose_name='Chef élevage',
                                       related_name='chef_elevage',
                                       blank=True
                                       )
    client = models.ForeignKey(settings.AUTH_USER_MODEL,
                               verbose_name='client',
                               related_name='elev_client',
                               on_delete=models.CASCADE
                               )
    valide = models.BooleanField("Validé", default=False)
    created = models.DateTimeField(_('Crée le'), auto_now_add=True)
    updated = models.DateTimeField(_('Modifié le'), auto_now=True)
    _original_valide = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._original_valide = self.valide

    def __str__(self):
        return f"{self.nom} {self.client}"

    def chef_elev_list(self):
        """returns list of chef_elev list created by elevage client"""
        chefs = Chef_elev.objects.all().filter(created_by=self.client)
        chefslist = []
        for chef in chefs:
            chefslist.append(chef.id)
        return chefslist

    def silo_list(self):
        """call all silos from on elevage"""
        silos = Silo.objects.all().filter(elevage=self.nom)
        silo_list = []
        for silo in silos:
            silo_list.append(silo.id)
        return silo_list

    def product_list(self):
        """
        call all products for one elevage
        """
        prods = Silo.objects.all().filter(elevage=self.nom)
        prod_list = []
        for prod in prods:
            prod_list.append(prod.contient.produit)
        return prod_list

    class Meta:
        ordering = ['nom']

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):

        context = {
            'elev': self.nom,
            'chef_elev': self.client.last_name
        }
        # pour envoi de mail ou sms lors de la validation

        if self.valide == self._original_valide and self.valide:
            # mail_elevage_valid(context, self.client.email)
            print('premier test ok élevage UPDATED')
        else:
            # mail_elevage_created(context, self.client.email)
            print('premier test KO élevage CREATED')

        return super().save(
            force_insert=force_insert,
            force_update=force_update,
            using=using, update_fields=update_fields
        )


class Silo(models.Model):
    """Defines silo/boisseau for an Elevage if necessary"""
    number = models.SmallIntegerField(_('Silo N°'))
    elevage = models.ForeignKey(
        Elevage,
        verbose_name="Elevage",
        related_name='elevage',
        on_delete=models.CASCADE
    )
    contient = models.ForeignKey(
        Product,
        verbose_name='Produit',
        related_name='produit_silo',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    class Meta:
        unique_together = ('number', 'elevage')

    def __str__(self):
        return f" {self.elevage} {self.number} {self.contient}"


class Order(models.Model):
    """
    Defines order placed by a user that can be of all types except CHAUF
    """
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   verbose_name="Client",
                                   related_name="order_createur",
                                   blank=True,
                                   null=True,
                                   on_delete=models.SET_NULL)
    elevage = models.ForeignKey(
        Elevage,
        verbose_name="Elevage",
        related_name="order_elevage",
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    product = models.ManyToManyField(
        Product,
        verbose_name="Produit",
        related_name="order_product"
    )
    created = models.DateTimeField(_('Crée le'), auto_now_add=True)
    updated = models.DateTimeField(_('Modifié le'), auto_now=True)
    date_order = models.DateField(_('date de commande'),
                                  blank=False,
                                  null=False)
    delivery = models.DateField(_('Livraison le: '))
    recorded = models.BooleanField(default=False)
    delivered = models.BooleanField(default=False)

    class Meta:
        ordering = ['date_order']

    def elevage_list(self):
        """
        Returns elevage list attached to client or chef_elev
        if user is Fabric or Commerc returns list of Client and then returns elevage list
        """
        if self.created_by.cat not in ['CLIENT', 'CH_ELE']:
            elevages = Elevage.objects.all()
        else:
            elevages = Elevage.objects.all().filter(
                Q(client=self.created_by) |
                Q(chef_elev=self.created_by)
            )
            elevage_list = []
            for el in elevages:
                if el.id not in elevage_list:
                    elevage_list.append(el.id)
            return elevage_list

    def product_list(self):
        return self.elevage.product_list

    def save(self, *args, **kwargs):

        date_o = dateutil.parser.parse(str(self.date_order)).date()
        date_d = dateutil.parser.parse(str(self.delivery)).date()

        if not self.created_by.canOrder:
            msg = _("utilisateur non autorisé, contactez l'admin")
            raise serializers.ValidationError(msg, code='authorization')
        if not self.elevage.valide:
            msg = _("l'élevage est non validé, contactez l'admin")
            raise serializers.ValidationError(msg, code='authorization')
        if self.recorded:
            msg = _('la commande ne peut pas être modifiée, car déja validée')
            raise serializers.ValidationError(msg, code='authorization')
        if self.updated:
            datetime_u = dateutil.parser.parse(str(self.updated))
            datetime_o = dateutil.parser.parse(str(self.date_order))
            delta = datetime_o - datetime_u
        if date_d <= datetime.date.today():
            msg = _('la commande ne peut pas être livrée dans un délai inférieur à {} '
                    .format(settings.MIN_FAB_DELAY)
                    )
            raise serializers.ValidationError(msg, code='authorization')

        super(Order, self).save(*args, **kwargs)

    def delete(self, using=None, keep_parents=False):
        if self.recorded:
            msg = _('la commande ne peut pas être supprimée, car déja validée')
            raise serializers.ValidationError(msg, code='authorization')
        if self.delivered:
            msg = _('la commande ne peut pas être supprimée, car déja livrée')
            raise serializers.ValidationError(msg, code='authorization')
        else:
            return super().delete(using=using, keep_parents=keep_parents)


# table produits to user pour simplifier la liste lors de la commande

# créer la commande (utilisateur --> choix de l'élevage si plusieurs --> choix du produit --> choix du silo si plusieurs si rien remorque ou BB)

# créer table address to elevage

# créer table address to client

# option créer table address to user (facturation)
