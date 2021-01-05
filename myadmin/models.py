from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify 
from ckeditor_uploader.fields import RichTextUploadingField


class Contact(models.Model):
    status_choice = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    ]
    contact_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=255)
    mobile = models.CharField(max_length=10)
    message = models.CharField(max_length=5000)
    status = models.CharField(choices = status_choice, max_length=10 ,null = False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    class Meta:
        db_table = "contact"
    def __str__(self):
        return "{0}".format(self.name)

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=100, unique=True)
    category_slug = models.SlugField(unique=True, blank=True, null=True)
    category_title = models.CharField(max_length=255, null = True)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def save(self, *args, **kwargs):
        if not self.category_id:
            self.category_slug = slugify(self.category_name)

        super(Category, self).save(*args, **kwargs)

    class Meta:
        db_table = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return "{0}".format(self.category_name)

class Product_type(models.Model):
    product_type_id = models.AutoField(primary_key=True)
    product_type_name = models.CharField(max_length=255, null = False, unique=True)
    product_type_title = models.CharField(max_length=255, null = True)
    product_type_description = models.TextField(null = False)
    product_type_slug = models.SlugField(unique=True, blank=True, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='product_types')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def save(self, *args, **kwargs):
        if not self.product_type_id:
            self.product_type_slug = slugify(self.product_type_name)

        super(Product_type, self).save(*args, **kwargs)
    class Meta:
        db_table = "product_type"
    def __str__(self):
        return "{0}".format(self.product_type_name)
        
class Country(models.Model):
    country_id = models.AutoField(primary_key=True)
    country_name = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    class Meta:
        db_table = "country"
        verbose_name_plural = "countries"

    def __str__(self): 
        return "{0}".format(self.country_name)

class Currency(models.Model):
    currency_id = models.AutoField(primary_key=True)
    country = models.OneToOneField(Country, on_delete=models.SET_NULL, null=True, related_name='currency')
    currency_symbol = models.CharField(max_length = 15, null = False)
    currency_name = models.CharField(max_length = 50, null = False)
    class Meta:
        db_table = "currency"
        verbose_name_plural = "currencies"
    def __str__(self): 
        return "{0}".format(self.currency_id)


class Brand(models.Model):
    brand_id = models.AutoField(primary_key=True)
    brand_name = models.CharField(max_length=255, null = False, unique=True)
    brand_slug = models.SlugField(unique=True, blank=True, null=True)
    brand_title = models.CharField(max_length = 255)
    brand_logo = models.ImageField(upload_to = 'brand/logo/%Y/%m/')
    brand_logo_alt_text = models.CharField(max_length=255, null = False)
    brand_info = RichTextUploadingField(null = False)
    brand_description = models.CharField(max_length = 255)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    country = models.ForeignKey(Country, default = '1', on_delete=models.SET_DEFAULT, null=True)
    brand_website = models.CharField(max_length = 500, null = True)
    brand_status = models.CharField(max_length = 100, default = "publish")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def save(self, *args, **kwargs):
        if not self.brand_id:
            self.brand_slug = slugify(self.brand_name)
        super(Brand, self).save(*args, **kwargs)
    class Meta:
        db_table = "brand"
    def __str__(self): 
        return "{0}".format(self.brand_name)

class Product(models.Model):
    subscription_choice = [
        ('m', 'Month'),
        ('y', 'Year'),
    ]
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=255, null = False, unique=True)
    product_slug = models.SlugField(unique=True, blank=True, null=True)
    product_title = models.CharField(max_length=255, null = True)
    product_info = models.TextField(null = False)
    product_description = models.CharField(max_length = 255)
    product_price = models.DecimalField(decimal_places = 2, max_digits = 20)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True, related_name = 'products')
    product_subscription = models.CharField(choices = subscription_choice, max_length = 1, null = False)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, related_name = 'products')
    product_type = models.ForeignKey(Product_type, on_delete=models.SET_NULL, null=True)
    product_link = models.CharField(max_length = 500, null = True)
    product_status = models.CharField(max_length = 100, default = "publish")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)

    def save(self, *args, **kwargs):
        if not self.product_id:
            self.product_slug = slugify(self.product_name)

        super(Product, self).save(*args, **kwargs)
    class Meta:
        db_table = "product"
    def __str__(self): 
        return "{0}".format(self.product_name)

class Feature(models.Model):
    has_value_choice = [
        ('y', 'Yes'),
        ('n', 'No'),
    ]
    feature_id = models.AutoField(primary_key=True)
    feature_name = models.CharField(max_length=255, null = False)
    product_type = models.ForeignKey(Product_type, on_delete=models.SET_NULL, null=True)
    feature_has_value = models.CharField(choices=has_value_choice, max_length = 1, null = False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    class Meta:
        db_table = "feature"
    def __str__(self): 
        return "{0}".format(self.feature_name)

class Product_feature(models.Model):
    product_feature_id = models.AutoField(primary_key=True)
    feature = models.ForeignKey(Feature, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, related_name='product_features')
    product_feature_value = models.CharField(max_length=255, null = False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    class Meta:
        db_table = "product_feature"
    def __str__(self): 
        return "{0}".format(self.product_feature_id)

class Review(models.Model):
    status_choice = [
        ('pending', 'Pending'),
        ('published', 'Published'),
        ('rejected', 'Rejected'),
    ]
    brand_choice = [
        ('brand', 'Brand'),
        ('product', 'Product'),
    ]
    review_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, related_name='reviews')
    features_rating = models.DecimalField(max_digits=5, decimal_places=1, null=False)
    value_for_money_rating = models.DecimalField(max_digits=5, decimal_places=1, null=False)
    ease_of_use_rating = models.DecimalField(max_digits=5, decimal_places=1, null=False)
    customer_support_rating = models.DecimalField(max_digits=5, decimal_places=1, null=False)
    overall_rating = models.DecimalField(max_digits=5, decimal_places=1, null=False)
    review_title = models.CharField(max_length=70 ,null = False)
    review = models.CharField(max_length=50000 ,null = False)
    review_status = models.CharField(choices = status_choice, max_length=10 ,null = False, default = "pending")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    class Meta:
        db_table = "review"
    def __str__(self): 
        return "{0}".format(self.review_id)


class ExpertHelp(models.Model):
    status_choice = [
        ('pending', 'Pending'),
        ('seen', 'Seen'),
        ('replied', 'Replied'),
        ('completed', 'Completed'),
    ]
    def ticket_number():
        try:
            no = ExpertHelp.objects.latest('help_id')
            if no == None:
                return SPEH-1
            else:
                prev_ticket_code_number = no.ticket_code.split('-')[-1]
                current_ticket_code_number = int(prev_ticket_code_number) + 1
                final_ticket = "SPEH-" + str(current_ticket_code_number)
                return final_ticket
        except:
            return null

    help_id = models.AutoField(primary_key=True)
    customer_name = models.CharField(max_length=50)
    customer_email = models.EmailField(max_length=255)
    customer_mobile = models.CharField(max_length=10)
    customer_coutry = models.ForeignKey(Country, default = '1', on_delete=models.SET_DEFAULT, null=True)
    customer_note = models.CharField(max_length=5000)
    status = models.CharField(choices = status_choice, max_length=10 ,null = False, default = 'pending')
    customer_inquiry_page_url = models.CharField(max_length=200)
    customer_help_category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='categories')
    ticket_code = models.CharField(unique=True,max_length=15, default=ticket_number)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    class Meta:
        db_table = "expert_help"

    def __str__(self):
        return "{0}".format(self.customer_name)

class WishList(models.Model):
    wishlist_id = models.AutoField(primary_key=True)
    brand = models.ForeignKey(Brand, on_delete=models.SET_NULL, null=True, related_name='wishlists')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='wishlists')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    class Meta:
        db_table = "wishlist"
    def __str__(self): 
        return "{0}".format(self.wishlist_id)


