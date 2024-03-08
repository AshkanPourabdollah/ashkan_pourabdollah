from django.db import models

# Create your models here.
"""---------------------------------------------Products------------------------------------"""


# Products
class Category(models.Model):
    category = models.CharField(max_length=30, default='')

    class Meta:
        verbose_name = "طبقه بندی"
        verbose_name_plural = "طبقه بندی ها"

    def __str__(self) -> str:
        return self.category


class Products(models.Model):
    title = models.CharField(max_length=30, default='')
    category = models.ManyToManyField(Category)
    price = models.IntegerField(default=0)
    image = models.ImageField(upload_to='productImages')
    details = models.TextField(default='', max_length=1000)

    class Meta:
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"

    def __str__(self) -> str:
        return self.title + '(' + str(self.category.first()) + ')'


"""----------------------------------------------Card---------------------------------------"""
# order list


"""---------------------------------------------Comments------------------------------------"""


# Comments
class Comment(models.Model):
    person = models.CharField(max_length=50, default='')
    email = models.CharField(max_length=100, default='')
    text = models.TextField(max_length=1500, default='')
    show = models.BooleanField(default=False)

    class Meta:
        verbose_name = "نظر"
        verbose_name_plural = "نظرات"

    def __str__(self) -> str:
        if self.show == True:
            return "درحال نمایش"
        else:
            return "در انتظار تایید"


"""---------------------------------------------Clients------------------------------------"""


# Users
class Client(models.Model):
    name = models.CharField(max_length=50, default='')
    phone = models.CharField(max_length=11, default='')
    password = models.CharField(max_length=30, default='')

    class Meta:
        verbose_name = "مشتری"
        verbose_name_plural = "مشتریان"

    def __str__(self) -> str:
        return self.name


"""-----------------------------------------------Cart--------------------------------------"""


# Cart
class Cart(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)


"""-----------------------------------------------Invoice--------------------------------------"""

class Invoice(models.Model):
    date = models.DateField()
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    total_amount = models.IntegerField(default=0)
    total_price = models.IntegerField(default = 0)

    def __str__(self):
        return self.client.name

class InvoiceItem(models.Model):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.IntegerField(default = 0)

    def __str__(self):
        return f'{self.invoice.client} - {self.product.title}'


