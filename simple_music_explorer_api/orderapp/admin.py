from django.contrib import admin

from .models import Orders, OrderItem, Address, ProductOrAlbumToOrder, PurchasedTrack

admin.site.register(OrderItem)
admin.site.register(Orders)
admin.site.register(Address)
admin.site.register(ProductOrAlbumToOrder)
admin.site.register(PurchasedTrack)

