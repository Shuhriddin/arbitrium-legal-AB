from django.db import models

class Application(models.Model):
    CATEGORY_CHOICES = (
        ('criminal', 'Jinoiy / Уголовное'),
        ('administrative', 'Ma\'muriy / Административное'),
        ('civil', 'Fuqarolik / Гражданское'),
        ('business', 'Tadbirkorlik va MChJ / Бизнес и ООО'),
    )
    STATUS_CHOICES = (
        ('new', 'Yangi / Новое'),
        ('in_progress', 'Jarayonda / В процессе'),
        ('completed', 'Yakunlangan / Завершено'),
    )
    
    name = models.CharField(max_length=255, verbose_name="F.I.Sh. / Ф.И.О.")
    phone = models.CharField(max_length=20, verbose_name="Telefon / Телефон")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, verbose_name="Yo'nalish / Направление")
    description = models.TextField(blank=True, null=True, verbose_name="Muammo tavsifi / Описание проблемы")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yuborilgan vaqti / Время отправки")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name="Holat / Статус")
    notes = models.TextField(blank=True, null=True, verbose_name="Eslatma / Заметки (Faqat admin ko'radi)")

    class Meta:
        verbose_name = "Ariza"
        verbose_name_plural = "Barcha Arizalar"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.get_category_display()} ({self.phone})"


# Managers to filter proxy models
class CriminalApplicationManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(category='criminal')

class AdministrativeApplicationManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(category='administrative')

class CivilApplicationManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(category='civil')

class BusinessApplicationManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(category='business')


# Proxy models
class CriminalApplication(Application):
    objects = CriminalApplicationManager()
    class Meta:
        proxy = True
        verbose_name = "Jinoiy yo'nalish arizasi"
        verbose_name_plural = "1. Jinoiy Bo'lim"

class AdministrativeApplication(Application):
    objects = AdministrativeApplicationManager()
    class Meta:
        proxy = True
        verbose_name = "Ma'muriy yo'nalish arizasi"
        verbose_name_plural = "2. Ma'muriy Bo'lim"

class CivilApplication(Application):
    objects = CivilApplicationManager()
    class Meta:
        proxy = True
        verbose_name = "Fuqarolik yo'nalish arizasi"
        verbose_name_plural = "3. Fuqarolik Bo'lim"

class BusinessApplication(Application):
    objects = BusinessApplicationManager()
    class Meta:
        proxy = True
        verbose_name = "Tadbirkorlik yo'nalish arizasi"
        verbose_name_plural = "4. Tadbirkorlik Bo'lim"


# Blog Post Model (For SEO and articles)
class BlogPost(models.Model):
    CATEGORY_CHOICES = (
        ('criminal', 'Jinoiy / Уголовное'),
        ('administrative', 'Ma\'muriy / Административное'),
        ('civil', 'Fuqarolik / Гражданское'),
        ('business', 'Tadbirkorlik / Предпринимательство'),
    )
    title = models.CharField(max_length=255, verbose_name="Sarlavha (UZ) / Заголовок (UZ)")
    title_ru = models.CharField(max_length=255, blank=True, default='', verbose_name="Sarlavha (RU) / Заголовок (RU)")
    slug = models.SlugField(max_length=255, unique=True, verbose_name="Slug (URL uchun)")
    content = models.TextField(verbose_name="Matn (UZ) / Содержание (UZ)")
    content_ru = models.TextField(blank=True, default='', verbose_name="Matn (RU) / Содержание (RU)")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, verbose_name="Kategoriya / Категория")
    law_code = models.CharField(max_length=255, blank=True, default='', verbose_name="Kodeks (UZ) / Кодекс (UZ)")
    law_code_ru = models.CharField(max_length=255, blank=True, default='', verbose_name="Kodeks (RU) / Кодекс (RU)")
    law_article = models.CharField(max_length=100, blank=True, default='', verbose_name="Modda (UZ) / Статья (UZ)")
    law_article_ru = models.CharField(max_length=100, blank=True, default='', verbose_name="Modda (RU) / Статья (RU)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Yaratilgan vaqti / Время создания")
    is_published = models.BooleanField(default=True, verbose_name="Chop etilganmi / Опубликовано")

    class Meta:
        verbose_name = "Maqola"
        verbose_name_plural = "Blog (Maqolalar)"
        ordering = ['-created_at']

    def __str__(self):
        return self.title


# Court Case Model (For successful results and building trust)
class CourtCase(models.Model):
    RESULT_CHOICES = (
        ('acquitted', 'Oqlov / Оправдательный приговор'),
        ('cancelled', 'Jarima bekor qilindi / Штраф отменен'),
        ('satisfied', 'Da\'vo qanoatlantirildi / Иск удовлетворен'),
    )
    CATEGORY_CHOICES = (
        ('criminal', 'Jinoiy / Уголовное'),
        ('administrative', 'Ma\'muriy / Административное'),
        ('civil', 'Fuqarolik / Гражданское'),
        ('business', 'Tadbirkorlik / Предпринимательство'),
    )
    title = models.CharField(max_length=255, verbose_name="Mavzu (UZ) / Тема (UZ)")
    title_ru = models.CharField(max_length=255, blank=True, default='', verbose_name="Mavzu (RU) / Тема (RU)")
    result = models.CharField(max_length=20, choices=RESULT_CHOICES, verbose_name="Natija / Результат")
    description = models.TextField(verbose_name="Tafsilotlar (UZ) / Описание (UZ)")
    description_ru = models.TextField(blank=True, default='', verbose_name="Tafsilotlar (RU) / Описание (RU)")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, verbose_name="Yo'nalish / Направление")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Sana / Дата")

    class Meta:
        verbose_name = "Sud ishi"
        verbose_name_plural = "Sud Amaliyoti (Natijalar)"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_result_display()}: {self.title}"


# Hero Section Settings Model
class HeroSettings(models.Model):
    title_uz = models.CharField(
        max_length=255, 
        default="Murakkab huquqiy muammolarga professional yechim",
        verbose_name="Sarlavha (UZ)"
    )
    title_ru = models.CharField(
        max_length=255, 
        default="Профессиональное решение сложных правовых вопросов",
        verbose_name="Sarlavha (RU)"
    )
    subtitle_uz = models.TextField(
        default="<strong>Solixov Shuxriddin</strong> - 2013-yildan buyon huquq sohasida faoliyat yuritib kelayotgan, Jinoiy va ma'muriy ishlar bo'yicha litsenziyaga ega <span class=\"license-text\">(LITSENZIYA Adliya vazirligining Toshkent viloyati xududiy boshqarmasi №1636252)</span> tajribali advokat. Tergov va sud jarayonlarida kafolatlangan himoya hamda murakkab nizolarga professional yechimlar.",
        verbose_name="Kichik sarlavha (UZ)"
    )
    subtitle_ru = models.TextField(
        default="<strong>Солихов Шухриддин</strong> - опытный адвокат, осуществляющий деятельность в сфере права с 2013 года, имеющий лицензию по уголовным и административным делам <span class=\"license-text\">(ЛИЦЕНЗИЯ Ташкентского областного территориального управления Министерства юстиции №1636252)</span>. Гарантированная защита в ходе следствия и судебных процессов, а также профессиональное решение сложных споров.",
        verbose_name="Kichik sarlavha (RU)"
    )

    class Meta:
        verbose_name = "Hero Bo'limi Sozlamasi"
        verbose_name_plural = "Hero Bo'limi Sozlamalari"

    def __str__(self):
        return "Hero Bo'limi Sozlamalari"

