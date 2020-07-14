from django.contrib import admin

from .models import Orders, OrderItem, Address, ProductToOrder, AlbumToOrder, PurchasedTrack

admin.site.register(OrderItem)
admin.site.register(Orders)
admin.site.register(Address)
admin.site.register(ProductToOrder)
admin.site.register(AlbumToOrder)
admin.site.register(PurchasedTrack)

