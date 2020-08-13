from django.contrib import admin

from orderapp.models import UserOrder, OrderItem, Address, FrozenOrderItem, FrozenTrack

admin.site.register(OrderItem)
admin.site.register(UserOrder)
admin.site.register(Address)
admin.site.register(FrozenOrderItem)
admin.site.register(FrozenTrack)

