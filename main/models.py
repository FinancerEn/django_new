from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    name: models.CharField = models.CharField(max_length=255, verbose_name="Название продукта")
    price: models.DecimalField = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    description: models.TextField = models.TextField(blank=True, verbose_name="Описание")
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self) -> str:
        return self.name


class Customer(models.Model):
    user: models.OneToOneField = models.OneToOneField(User, on_delete=models.CASCADE)
    phone: models.CharField = models.CharField(max_length=15, verbose_name="Телефон")
    address: models.TextField = models.TextField(verbose_name="Адрес")
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")

    def __str__(self) -> str:
        return self.user.username


class Loader(models.Model):
    name: models.CharField = models.CharField(max_length=100, verbose_name="Имя")
    phone: models.CharField = models.CharField(max_length=15, verbose_name="Телефон")
    is_available: models.BooleanField = models.BooleanField(default=True, verbose_name="Доступен")
    hourly_rate: models.DecimalField = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Стоимость за час")

    def __str__(self) -> str:
        return self.name


class Vehicle(models.Model):
    VEHICLE_TYPES = [
        ('small', 'Маленькая'),
        ('medium', 'Средняя'),
        ('large', 'Большая'),
    ]

    license_plate: models.CharField = models.CharField(max_length=15, unique=True, verbose_name="Номерной знак")
    vehicle_type: models.CharField = models.CharField(max_length=10, choices=VEHICLE_TYPES, verbose_name="Тип машины")
    capacity: models.DecimalField = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Грузоподъемность (тонн)")
    hourly_rate: models.DecimalField = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Стоимость за час")
    is_available: models.BooleanField = models.BooleanField(default=True, verbose_name="Доступна")

    def __str__(self) -> str:
        return f"{self.get_vehicle_type_display()} ({self.license_plate})"


class Order(models.Model):
    customer: models.ForeignKey = models.ForeignKey(Customer, on_delete=models.CASCADE, verbose_name="Клиент")
    loaders: models.ManyToManyField = models.ManyToManyField(Loader, blank=True, verbose_name="Грузчики")
    vehicle: models.ForeignKey = models.ForeignKey(Vehicle, on_delete=models.CASCADE, verbose_name="Машина")
    pickup_address: models.TextField = models.TextField(verbose_name="Адрес загрузки")
    delivery_address: models.TextField = models.TextField(verbose_name="Адрес доставки")
    scheduled_time: models.DateTimeField = models.DateTimeField(verbose_name="Время заказа")
    total_cost: models.DecimalField = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Итоговая стоимость")
    is_paid: models.BooleanField = models.BooleanField(default=False, verbose_name="Оплачен")
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self) -> str:
        return f"Заказ #{self.id} - {self.customer.user.username}"


class Cart(models.Model):
    customer: models.OneToOneField = models.OneToOneField(Customer, on_delete=models.CASCADE, verbose_name="Клиент")
    orders: models.ManyToManyField = models.ManyToManyField(Order, blank=True, verbose_name="Заказы")
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self) -> str:
        return f"Корзина {self.customer.user.username}"


class ChatMessage(models.Model):
    sender: models.ForeignKey = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Отправитель")
    message: models.TextField = models.TextField(verbose_name="Сообщение")
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True, verbose_name="Дата отправки")

    def __str__(self) -> str:
        return f"Сообщение от {self.sender.username} в {self.created_at}"


class Payment(models.Model):
    order: models.OneToOneField = models.OneToOneField(Order, on_delete=models.CASCADE, verbose_name="Заказ")
    payment_method: models.CharField = models.CharField(max_length=50, verbose_name="Способ оплаты")
    transaction_id: models.CharField = models.CharField(max_length=100, unique=True, verbose_name="ID транзакции")
    paid_at: models.DateTimeField = models.DateTimeField(auto_now_add=True, verbose_name="Дата оплаты")

    def __str__(self) -> str:
        return f"Платеж для заказа #{self.order.id}"
