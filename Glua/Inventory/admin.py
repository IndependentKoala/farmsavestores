from django.contrib import admin
from django.core.exceptions import PermissionDenied
from .models import Drug, Sale, Stocked, Measurement, LockedProduct, MarketingItem, IssuedItem, PickingList, Cannister, IssuedCannister, Client


class LockedProductAdmin(admin.ModelAdmin):
    # Optionally, add fields to the admin panel
    list_display = ('drug', 'locked_by', 'date_locked', 'quantity', 'client')
    search_fields = ('drug__name', 'client__name', 'locked_by__username')

    def save_model(self, request, obj, form, change):
        # Check if the object is being updated (change == True)
        if change:
            original = LockedProduct.objects.get(pk=obj.pk)
            # If the product is locked, prevent any changes to it
            if original.date_locked and obj.drug != original.drug:
                raise PermissionDenied("Cannot update locked drugs.")

        # Call the parent method to save the object
        super().save_model(request, obj, form, change)


class DrugAdmin(admin.ModelAdmin):
    list_display = ('name', 'batch_no', 'stock', 'dose_pack', 'expiry_date', 'reorder_level')
    search_fields = ('name', 'batch_no')


class ClientAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'country_code', 'date_created')
    search_fields = ('name', 'phone', 'email')


class CannisterAdmin(admin.ModelAdmin):
    list_display = ('name', 'batch_no', 'stock', 'litres')
    search_fields = ('name', 'batch_no')


class SaleAdmin(admin.ModelAdmin):
    list_display = ('drug_sold', 'client', 'date_sold', 'quantity', 'remaining_quantity')
    search_fields = ('drug_sold', 'batch_no', 'client__name')


class PickingListAdmin(admin.ModelAdmin):
    list_display = ('date', 'client', 'product', 'batch_no', 'quantity')
    search_fields = ('product', 'batch_no', 'client__name')


class IssuedItemAdmin(admin.ModelAdmin):
    list_display = ('item', 'issued_to', 'quantity_issued', 'date_issued', 'issued_by')
    search_fields = ('item', 'issued_to', 'issued_by__username')


class IssuedCannisterAdmin(admin.ModelAdmin):
    list_display = ('name', 'batch_no', 'client', 'date_issued', 'date_returned', 'quantity')
    search_fields = ('name', 'batch_no', 'client__name')


class MarketingItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'stock')
    search_fields = ('name',)


# Register models with their ModelAdmin classes
admin.site.register(Drug, DrugAdmin)
admin.site.register(Sale, SaleAdmin)
admin.site.register(Client, ClientAdmin)
admin.site.register(MarketingItem, MarketingItemAdmin)
admin.site.register(IssuedItem, IssuedItemAdmin)
admin.site.register(LockedProduct, LockedProductAdmin)
admin.site.register(PickingList, PickingListAdmin)
admin.site.register(Cannister, CannisterAdmin)
admin.site.register(IssuedCannister, IssuedCannisterAdmin)