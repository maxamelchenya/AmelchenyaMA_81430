from django.contrib import admin

from .models import BidHistory, Category, Coin, Country, User

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Country)
admin.site.register(Coin)
admin.site.register(BidHistory)
