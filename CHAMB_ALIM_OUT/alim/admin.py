from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
from alim import models
from alim.models import User, Cat, Chef_elev, Product, Elevage, Silo


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ['clientcode', 'societe', 'last_name',
                    'first_name', 'categorie', 'email', 'canOrder']
    list_filter = [
        'canOrder',
        'cat'
    ]
    search_fields = ('last_name', 'societe', 'first_name', 'cat')
    actions = ('set_canOrder',)
    fieldsets = (
        (None, {'fields': ('clientcode', 'password')}),
        (_('Personnal info'), {
         'fields': ('societe', 'last_name', 'first_name', 'email')}),
        (
            _('permissions'),
            {
                'fields': ('canOrder', 'is_active', 'is_staff', 'is_superuser')
            }
        ),
        (_('Important_dates'), {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2',)
        }),
    )

    def set_canOrder(self, request, queryset):
        count = 0
        for user in queryset:
            user.canOrder = True
            user.save()
            count += 1
        self.message_user(
            request, '{} utilisateurs(s) autorisé(s)'.format(count))

    set_canOrder.short_description = "Autoriser les utilisateurs selectionnés"

    def categorie(self, user):
        cat = Cat.objects.get(user=user.id)
        return cat.cat


class ProductAdmin(admin.ModelAdmin):
    ordering = ['produit']
    list_display = [
        'produit',
        'ref'
    ]

    search_fields = ('produit', 'ref')


class OrderAdmin(admin.ModelAdmin):
    ordering = ['-delivery']
    list_display = [
        'id',
        'created_by',
        'elevage',
        'delivery',
        'recorded',
        'delivered',
    ]
    fieldsets = (
        (_('Commande'), {
            "fields": (
                'created_by', 'elevage', 'product'
            ),

        }),
        (_('Déroulement'), {
            "fields": (
                'date_order', 'delivery', 'recorded', 'delivered'
            ),
        })
    )
    list_per_page = 25
    list_filter = [
        'date_order',
        'delivery',
        'recorded',
        'delivered'
    ]

    def set_recorded(self, request, queryset):
        count = 0
        for user in queryset:
            user.canOrder = True
            user.save()
            count += 1
        self.message_user(
            request, '{} commandes(s) enregistrée(s)'.format(count))

    set_recorded.short_description = "enregistrer commande(s) selectionnée(s)"

    def set_delivered(self, request, queryset):
        count = 0
        for user in queryset:
            user.canOrder = True
            user.save()
            count += 1
        self.message_user(
            request, '{} commandes(s) livrée(s)'.format(count))

    set_recorded.short_description = "livrer commande(s) selectionnée(s)"
    actions = ('set_recorded', 'set_delivered')


admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.User, UserAdmin)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.Elevage)
admin.site.register(models.Cat)
admin.site.register(models.Silo)
