from django.contrib.auth.models import BaseUserManager,AbstractUser
from django.core import validators
from django.db import models

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    email = models.EmailField(verbose_name='Почта', unique=True)
    phone = models.CharField(verbose_name='Телефон',max_length=30,
                                                          null=True,blank=True)
    first_last_name = models.CharField(verbose_name='Имя и Фамилия',
                                                                max_length=250)
    total_payment = models.FloatField(verbose_name='Общее вознаграждение',
                                                                    default=0)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        if self.first_last_name:
            return self.first_last_name
        return self.email

class Payment(models.Model):
    author = models.ForeignKey(User,verbose_name="Автор",
                               related_name="authors",
                               on_delete=models.CASCADE)
    payment = models.FloatField(verbose_name='Сумма платежа',
                                validators=[validators.MinValueValidator(0)])
    date = models.DateTimeField(verbose_name="Дата платежа",auto_now_add=True)

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"

    def __str__(self):
        return f"Платеж для: {self.author}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.author.total_payment += self.payment * 0.3
        self.author.save()


class Pay(models.Model):
    user = models.ForeignKey(User, verbose_name="Пользователь",
                               related_name="users",
                               on_delete=models.CASCADE)
    pay = models.FloatField(verbose_name='Сумма выплаты',
                                validators=[validators.MinValueValidator(0)])
    date_create =models.DateTimeField(verbose_name="Дата создания заявки ",
                                                            auto_now_add=True)
    date_processing = models.DateTimeField(verbose_name="Дата обработки заявки",
                                           null=True,blank=True)
    paid_out = models.BooleanField(verbose_name="Выплачено",default=False)

    invoice = models.TextField(verbose_name="Номер счёта",blank=True,null=True)

    class Meta:
        verbose_name= "Выплата"
        verbose_name_plural = "Выплаты"

    def __str__(self):
        return f"Выплата для: {self.user}"