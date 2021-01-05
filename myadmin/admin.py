from django.contrib import admin
from .models import Category,Product_type,Brand, Country, Feature, Product_feature, Product, Contact, Review, ExpertHelp, WishList, Currency

# Register your models here.
admin.site.register(Category)
admin.site.register(Country)
admin.site.register(Product_type)
admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(Feature)
admin.site.register(Product_feature)
admin.site.register(Contact)
admin.site.register(Review)
admin.site.register(ExpertHelp)
admin.site.register(WishList)
admin.site.register(Currency)



