from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Client)

admin.site.register(Category)
admin.site.register(Products)

admin.site.register(Comment)

admin.site.register(Cart)

admin.site.register(Invoice)
admin.site.register(InvoiceItem)

################################################################### admin settings ##################################
admin.site.site_header = 'مدیریت سایت هگزا'
admin.site.site_title = 'مدیریت فروشگاه هگزا'
admin.site.index_title = 'فروشگاه هگزا'
admin.site.site_url = None