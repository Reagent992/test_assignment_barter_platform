from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Post(models.Model):
    class CATEGORY_CHOICES(models.TextChoices):
        BOOKS = "books", "Книги"
        ELECTRONICS = "electronics", "Электроника"
        CLOTH = "cloth", "Одежда"
        FURNITURE = "furniture", "Мебель"
        OTHER = "other", "Другое"

    class CONDITION_CHOICES(models.TextChoices):
        NEW = "new", "Новое"
        LIKE_NEW = "like new", "Как новое"
        USED = "used", "Б/У"
        FOR_PARTS = "for parts", "На запчасти"

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="posts",
    )
    title = models.CharField(
        "Название",
        max_length=255,
    )
    description = models.TextField(
        "Описание",
        blank=True,
    )
    image = models.ImageField(
        "Картинка",
        upload_to="images/",
        blank=True,
        help_text="Загрузите картинку",
    )
    category = models.CharField(
        "Категория",
        max_length=50,
        choices=CATEGORY_CHOICES,
    )
    condition = models.CharField(
        "Состояние",
        max_length=50,
        choices=CONDITION_CHOICES,
    )
    created_at = models.DateTimeField(
        "Дата создания",
        auto_now_add=True,
    )

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"


class STATUS_CHOICES(models.TextChoices):
    PENDING = "pending", "На рассмотрении"
    ACCEPTED = "accepted", "Принято"
    REJECTED = "rejected", "Отклонено"


class ExchangeProposal(models.Model):
    sender = models.ForeignKey(
        "Post", on_delete=models.CASCADE, related_name="sent_proposals"
    )
    receiver = models.ForeignKey(
        "Post", on_delete=models.CASCADE, related_name="received_proposals"
    )
    comment = models.TextField("Комментарий")
    status = models.CharField(
        "Статус",
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_CHOICES.PENDING,
    )
    created_at = models.DateTimeField(
        "Дата создания",
        auto_now_add=True,
    )

    def __str__(self) -> str:
        return f"Обмен от {self.sender} на {self.receiver} ({self.status})"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Предложение обмена"
        verbose_name_plural = "Предложения обмена"
