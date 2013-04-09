# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime


class Supplier(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование')
    address = models.CharField(max_length=255, verbose_name='Адрес', blank=True)
    phone = models.CharField(max_length=255, verbose_name='Телефон', blank=True)
    contact = models.CharField(max_length=255, verbose_name='Контактное лицо, ФИО', blank=True)
    contact_phone = models.CharField(max_length=255, verbose_name='Контактное лицо, телефон', blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'store_supplier'
        ordering = ['name']
        verbose_name_plural = u'Поставщики'
        verbose_name = u'Поставщик'

class CategoryOfProduct(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    parent = models.ForeignKey('self', verbose_name='Родитель', blank=True, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'store_product_categories'
        ordering = ['name']
        verbose_name_plural = u'Категории товара'
        verbose_name = u'Категория товара'

class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    category = models.ForeignKey(CategoryOfProduct, verbose_name='Категория')
    measure_unit = models.CharField(max_length=255, verbose_name='Единица измерения')
    price = models.PositiveIntegerField(verbose_name='Закупочная цена')
    supplier = models.ForeignKey(Supplier, blank=True, null=True, verbose_name='Поставщик')
    description = models.TextField(verbose_name='Описание', blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'store_products'
        ordering = ['name']
        verbose_name_plural = u'Товары'
        verbose_name = u'Товар'

class Warehouse(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    address = models.CharField(max_length=255, verbose_name='Адрес', blank=True)
    comment = models.TextField(verbose_name='Комментарий', blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'store_warehouses'
        ordering = ['name']
        verbose_name_plural = u'Склады'
        verbose_name = u'Склад'

class CategoryOfDish(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    parent = models.ForeignKey('self', verbose_name='Категория')

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'store_dish_categories'
        ordering = ['name']
        verbose_name_plural = u'Категории калькуляционных карт'
        verbose_name = u'Категория калькуляционных карт'

class Dish(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    category = models.ForeignKey(CategoryOfDish, verbose_name='Категория')
    date_start = models.DateField(verbose_name='Действует с')
    date_end = models.DateField(verbose_name='Действует по', blank=True, null=True)
    portion = models.PositiveIntegerField(verbose_name='Порция')
    created = models.DateField(verbose_name='Дата создания')
    author = models.ForeignKey(User, verbose_name='Автор', related_name='dish_author')
    modified_date = models.DateField(verbose_name='Дата изменения')
    modified_author = models.ForeignKey(User, verbose_name='Последний сотрудник внесший изменения ', related_name='dish_modified_author')
    comment = models.TextField(verbose_name='Комментарий', blank=True)
    master = models.BooleanField(verbose_name='выдан мастером или нет')

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'store_dishes'
        ordering = ['name']
        verbose_name_plural = u'Калькуляционные карты'
        verbose_name = u'Калькуляционная карта'

class ProductOfDish(models.Model):
    dish = models.ForeignKey(Dish, verbose_name='КК')
    product = models.ForeignKey(Product, verbose_name='Товар')
    measure_unit = models.CharField(max_length=255, verbose_name='Единица измерения')

    def __unicode__(self):
        return self.product

    class Meta:
        db_table = 'store_dish_products'
        ordering = ['product']
        verbose_name_plural = u'Товары КК'
        verbose_name = u'Товар КК'


class SalePoint(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название')
    warehouse = models.ForeignKey(Warehouse, verbose_name='Склад')
    address = models.CharField(max_length=255, verbose_name='Адрес', blank=True)
    comment = models.TextField(verbose_name='Комментарий', blank=True)
    created = models.DateField(verbose_name='Дата создания')
    author = models.ForeignKey(User, verbose_name='Автор', related_name='point_author')
    modified_date = models.DateField(verbose_name='Дата изменения')
    modified_author = models.ForeignKey(User, verbose_name='Автор изменений', related_name='point_modified_author')

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'sale_salepoints'
        ordering = ['name']
        verbose_name_plural = u'Точки продаж'
        verbose_name = u'Точка продаж'

class Change(models.Model):
    point = models.ForeignKey(SalePoint, verbose_name='Точка продаж')
    cashier = models.ForeignKey(User, verbose_name='Кассир')
    start = models.DateField(verbose_name='Дата открытия')
    end = models.DateField(verbose_name='Дата закрытия', blank=True, null=True)

    def __unicode__(self):
        return self.point

    class Meta:
        db_table = 'sale_changes'
        ordering = ['point']
        verbose_name_plural = u'Смены'
        verbose_name = u'Смена'

class Sale(models.Model):
    point = models.ForeignKey(SalePoint, verbose_name='Точка продаж')
    cashier = models.ForeignKey(User, verbose_name='Кассир')
    change = models.ForeignKey(Change, verbose_name='Смена')
    discount = models.PositiveIntegerField(verbose_name='Скидка', blank=True, null=True)

    def __unicode__(self):
        return self.point

    class Meta:
        db_table = 'sale_sales'
        ordering = ['point']
        verbose_name_plural = u'Смены'
        verbose_name = u'Смена'

class DishOfSale(models.Model):
    sale = models.ForeignKey(Sale, verbose_name='Продажи')
    dish = models.ForeignKey(Dish, verbose_name='Блюда')
    amount = models.PositiveIntegerField(verbose_name='Количество')
    price = models.PositiveIntegerField(verbose_name='Цена')

    def __unicode__(self):
        return self.dish

    class Meta:
        db_table = 'sale_sale_dishes'
        ordering = ['dish']
        verbose_name_plural = u'Блюда для продажи'
        verbose_name = u'Блюдо для продажи'

class Purchase(models.Model):
    purchaser = models.ForeignKey(User, verbose_name='Закупщик', related_name='purchaser')
    supplier = models.ForeignKey(Supplier, verbose_name='Контрагент', blank=True, null=True)
    warehouse = models.ForeignKey(Warehouse, verbose_name='Склад')
    date_purchase = models.DateField(verbose_name='Дата закупа')
    comment = models.TextField(verbose_name='Комментарий', blank=True)
    created = models.DateField(verbose_name='Время создания')
    author = models.ForeignKey(User, verbose_name='Автор', related_name='purchase_author')
    modified_date = models.DateField(verbose_name='Дата изменения')
    modified_author = models.ForeignKey(User, verbose_name='Автор изменения', related_name='purchase_modified_author')
    issued = models.PositiveIntegerField(verbose_name='Выдано', blank=True, null=True)

    def __unicode__(self):
        return str(self.pk)

    class Meta:
        db_table = 'wr_purchases'
        ordering = ['pk']
        verbose_name_plural = u'Закупы'
        verbose_name = u'Закуп'

class ProductOfPurchase(models.Model):
    purchase = models.ForeignKey(Purchase, verbose_name='Закуп')
    product = models.ForeignKey(Product, verbose_name='Товары')
    purchase_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Количество, закуп')
    acceptance_amount = models.DecimalField(max_digits=10, decimal_places=2,verbose_name='Количество, приемка', blank=True, null=True)
    return_amount = models.DecimalField(max_digits=10, decimal_places=2,verbose_name='Количество, возврат', blank=True, null=True)
    purchase_price = models.PositiveIntegerField(verbose_name='Цена закупа')
    acceptance_price = models.PositiveIntegerField(verbose_name='Цена закупа', blank=True, null=True)
    return_price = models.PositiveIntegerField(verbose_name='Цена закупа', blank=True, null=True)

    def __unicode__(self):
        return self.product.name

    class Meta:
        db_table = 'wr_purchase_products'
        ordering = ['product']
        verbose_name_plural = u'Товары закупа'
        verbose_name = u'Товар закупа'

class Acceptance(models.Model):
    purchase = models.OneToOneField(Purchase, verbose_name='Закуп')
    date = models.DateField(verbose_name='Дата приемки')
    costs = models.PositiveIntegerField(verbose_name='Расходы', blank=True, null=True)
    cash = models.PositiveIntegerField(verbose_name='В кассу')
    comment = models.TextField(verbose_name='Комментарий', blank=True)
    created = models.DateField(verbose_name='Время создания')
    author = models.ForeignKey(User, verbose_name='Автор', related_name='acceptance_author')
    modified_date = models.DateField(verbose_name='Дата изменения')
    modified_author = models.ForeignKey(User, verbose_name='Автор изменения', related_name='acceptance_modified_author')

    def sum(self):
        products = ProductOfPurchase.objects.filter(purchase=self.purchase)
        sum = 0
        for product in products:
            sum += product.acceptance_price * product.acceptance_amount
        return sum

    def debt(self):
        debt = self.cash -(self.purchase.issued-self.sum()-self.costs)
        return debt

    def __unicode__(self):
        return str(self.pk)

    class Meta:
        db_table = 'wr_acceptances'
        ordering = ['pk']
        verbose_name_plural = u'Приемки'
        verbose_name = u'Приемка'

class ReturnModel(models.Model):
    acceptance = models.OneToOneField(Acceptance, verbose_name='Приемка')
    date = models.DateField(verbose_name='Дата возврата', blank=True, null=True)
    comment = models.TextField(verbose_name='Комментарий', blank=True)
    created = models.DateField(verbose_name='Время создания')
    author = models.ForeignKey(User, verbose_name='Автор', related_name='return_author')
    modified_date = models.DateField(verbose_name='Дата изменения')
    modified_author = models.ForeignKey(User, verbose_name='Автор изменения', related_name='return_modified_author')

    def sum(self):
        products = ProductOfPurchase.objects.filter(purchase=self.acceptance.purchase)
        sum = 0
        for product in products:
            sum += (product.acceptance_price * product.return_amount)
        return sum

    def __unicode__(self):
        return str(self.pk)

    class Meta:
        db_table = 'wr_returns'
        ordering = ['pk']
        verbose_name_plural = u'Возвраты'
        verbose_name = u'Возврат'

class WriteOff(models.Model):
    warehouse = models.ForeignKey(Warehouse, verbose_name='Склад')
    date = models.DateField(verbose_name='Дата')
    comment = models.TextField(verbose_name='Комментарий', blank=True)
    reason = models.CharField(max_length=100, verbose_name='Причина', choices=((u'Обеды сотрудников',u'Обеды сотрудников'),(u'Порча',u'Порча'),(u'Прочее',u'Прочее')))
    created = models.DateField(verbose_name='Время создания')
    author = models.ForeignKey(User, verbose_name='Автор', related_name='writeoff_author')
    modified_date = models.DateField(verbose_name='Дата изменения')
    modified_author = models.ForeignKey(User, verbose_name='Автор изменения', related_name='writeoff_modified_author')

    def __unicode__(self):
        return str(self.pk)

    class Meta:
        db_table = 'wr_writeoffs'
        ordering = ['pk']
        verbose_name_plural = u'Списания'
        verbose_name = u'Списание'

class ProductOfWriteOff(models.Model):
    writeoff = models.ForeignKey(WriteOff, verbose_name='Списание')
    product = models.ForeignKey(Product, verbose_name='Товары', blank=True, null=True)
    dish = models.ForeignKey(Dish, verbose_name='Товары', blank=True, null=True)
    amount = models.PositiveIntegerField(verbose_name='Количество')
    price = models.PositiveIntegerField(verbose_name='Цена')

    def __unicode__(self):
        return self.product

    class Meta:
        db_table = 'wr_writeoff_products'
        ordering = ['product']
        verbose_name_plural = u'Товары списания'
        verbose_name = u'Товар списанияы'

class Inventory(models.Model):
    warehouse = models.ForeignKey(Warehouse, verbose_name='Склад')
    date = models.DateField(verbose_name='Дата')
    comment = models.TextField(verbose_name='Комментарий', blank=True)
    created = models.DateTimeField(verbose_name='Время создания')
    author = models.ForeignKey(User, verbose_name='Автор', related_name='inventory_author')
    modified_date = models.DateField(verbose_name='Дата изменения')
    modified_author = models.ForeignKey(User, verbose_name='Автор изменения', related_name='inventory_modified_author')

    def __unicode__(self):
        return self.pk

    class Meta:
        db_table = 'wr_inventories'
        ordering = ['pk']
        verbose_name_plural = u'Инвентаризация'
        verbose_name = u'Инвентаризация'

class ProductOfInventory(models.Model):
    inventory = models.ForeignKey(Inventory, verbose_name='Инвентаризация')
    product = models.ForeignKey(Product, verbose_name='Товары')
    estimated_balance = models.PositiveIntegerField(verbose_name='Расчетный остаток')
    actual_balance = models.PositiveIntegerField(verbose_name='Фактический остаток')
    price = models.PositiveIntegerField(verbose_name='Цена')

    def __unicode__(self):
        return self.product

    class Meta:
        db_table = 'wr_inventory_products'
        ordering = ['product']
        verbose_name_plural = u'Товары инвентаризации'
        verbose_name = u'Товар инвентаризации'

class Movement(models.Model):
    warehouse_from = models.ForeignKey(Warehouse, verbose_name='Склад откуда', related_name='warehouse_from')
    warehouse_to = models.ForeignKey(Warehouse, verbose_name='Склад куда', related_name='warehouse_to')
    date = models.DateField(verbose_name='Дата')
    comment = models.TextField(verbose_name='Комментарий', blank=True)
    created = models.DateTimeField(verbose_name='Время создания')
    author = models.ForeignKey(User, verbose_name='Автор', related_name='movement_author')
    modified_date = models.DateField(verbose_name='Дата изменения')
    modified_author = models.ForeignKey(User, verbose_name='Автор изменения', related_name='movement_modified_author')

    def __unicode__(self):
        return self.pk

    class Meta:
        db_table = 'wr_movements'
        ordering = ['pk']
        verbose_name_plural = u'Перемещения'
        verbose_name = u'Перемещение'

class ProductOfMovement(models.Model):
    movement = models.ForeignKey(Movement, verbose_name='Перемещение')
    product = models.ForeignKey(Product, verbose_name='Товары', blank=True, null=True)
    dish = models.ForeignKey(Dish, verbose_name='Блюдо', blank=True, null=True)
    amount = models.PositiveIntegerField(verbose_name='Количество')
    price = models.PositiveIntegerField(verbose_name='Цена')

    def __unicode__(self):
        return self.product

    class Meta:
        db_table = 'wr_movement_products'
        ordering = ['product']
        verbose_name_plural = u'Товары перемещения'
        verbose_name = u'Товар перемещения'

class Issuance(models.Model):
    warehouse = models.ForeignKey(Warehouse, verbose_name='Склад')
    master = models.ForeignKey(User, verbose_name='Мастер', related_name='master')
    date = models.DateField(verbose_name='Дата')
    comment = models.TextField(verbose_name='Комментарий', blank=True)
    created = models.DateTimeField(verbose_name='Время создания')
    author = models.ForeignKey(User, verbose_name='Автор', related_name='issuance_author')
    modified_date = models.DateField(verbose_name='Дата изменения')
    modified_author = models.ForeignKey(User, verbose_name='Автор изменения', related_name='issuance_modified_author')

    def __unicode__(self):
        return self.pk

    class Meta:
        db_table = 'wr_issuances'
        ordering = ['pk']
        verbose_name_plural = u'Выдачи'
        verbose_name = u'Выдача'

class DishOfIssuance(models.Model):
    issuance = models.ForeignKey(Issuance, verbose_name='Выдача')
    dish = models.ForeignKey(Dish, verbose_name='Блюдо')
    amount = models.PositiveIntegerField(verbose_name='Количество')
    price = models.PositiveIntegerField(verbose_name='Цена')

    def __unicode__(self):
        return self.dish

    class Meta:
        db_table = 'wr_issuance_dishes'
        ordering = ['dish']
        verbose_name_plural = u'Блюда выдачи'
        verbose_name = u'Блюдо выдачи'

class DishOfWarehouse(models.Model):
    warehouse = models.ForeignKey(Warehouse, verbose_name='Склад')
    dish = models.ForeignKey(Dish, verbose_name='Блюдо')
    amount = models.PositiveIntegerField(verbose_name='Количество')
    price = models.PositiveIntegerField(verbose_name='Цена')
    date = models.DateField(verbose_name='Дата')

    def __unicode__(self):
        return self.dish

    class Meta:
        db_table = 'store_warehouse_dishes'
        ordering = ['dish']
        verbose_name_plural = u'Блюда на складе'
        verbose_name = u'Блюдо на складе'

class Costs(models.Model):
    date = models.DateField(verbose_name='Дата')
    sum = models.PositiveIntegerField(verbose_name='Сумма')
    type = models.CharField(max_length=255, verbose_name='Тип расхода')
    comment = models.TextField(verbose_name='Комментарий', blank=True)

    def __unicode__(self):
        return self.pk

    class Meta:
        db_table = 'cst_costs'
        ordering = ['pk']
        verbose_name_plural = u'Расходы'
        verbose_name = u'Расход'


class ProductAtWarehouse(models.Model):
    product = models.ForeignKey(Product, verbose_name='Товар')
    warehouse = models.ForeignKey(Warehouse, verbose_name='Склад')
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Количество')
    price = models.PositiveIntegerField(verbose_name='Цена приемки')
    date = models.DateField(verbose_name='Дата приемки')

    def __unicode__(self):
        return self.product

    class Meta:
        db_table = 'store_warehouse_products'
        ordering = ['product']
        verbose_name_plural = u'Товары на складе'
        verbose_name = u'Товар на складе'


class UserProfile(models.Model):
    user = models.OneToOneField(User, unique=True, verbose_name='Пользователь')
    patronymic = models.CharField(max_length=255, verbose_name='Отчество', blank=True)
    phone = models.CharField(max_length=255, verbose_name='Телефон', blank=True)
    position = models.CharField(max_length=255, blank=True, verbose_name='Должность')
    point = models.ForeignKey(SalePoint, verbose_name='Точка продаж', blank=True, null=True)
    active_from = models.DateField(verbose_name='Активен с')
    active_until = models.DateField(verbose_name='Активен до', blank=True, null=True)
    type = models.CharField(max_length=255, verbose_name='Тип оплаты')

    def __unicode__(self):
        return self.user

    class Meta:
        db_table = 'auth_user_profile'
        ordering = ['pk']
        verbose_name_plural = u'Профили'
        verbose_name = u'Профиль'

@receiver(post_save, sender=User, dispatch_uid="gV3AQD1y3H6laRX5mx94KDWeqYrL9c0V")
def create_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.get_or_create(user=instance, active_from=datetime.date.today())

# еще три таблицы по юзеру