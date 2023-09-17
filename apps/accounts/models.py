from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

from apps.accounts.managers import MyUserManager


class MyUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=255,
        unique=True,
    )
    username = models.CharField(
        max_length=50,
        verbose_name='Имя пользователя',
        unique=True,
    )
    first_name = models.CharField(
        max_length=155,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=155,
        verbose_name='Фамилия'
    )
    created_date = models.DateField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Активен'
    )
    is_staff = models.BooleanField(
        default=True,
        verbose_name='Сотрудник'
    )
    is_admin = models.BooleanField(
        default=False,
        verbose_name='Админ'
    )
    is_caretaker = models.BooleanField(
        default=False,
        verbose_name='Волонтер'
    )
    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']

    def str(self):
        return self.username

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app app_label?"""
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        # Simplest possible answer: All admins are staff
        return self.is_admin

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Category(models.Model):
    name = models.CharField(max_length=125)
    is_active = models.BooleanField(default=True)

    def str(self):
        return self.name


class UserImage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='user_images/')


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    status = models.CharField(max_length=100, blank=True, null=True)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    user_image = models.ForeignKey(UserImage, on_delete=models.SET_NULL, blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def str(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Community(models.Model):
    name = models.CharField(max_length=125, unique=True)
    description = models.TextField()
    members = models.ManyToManyField(UserProfile, related_name='communities_joined')
    moderators = models.ManyToManyField(UserProfile, related_name='communities_moderated')

    def str(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=125)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    count_of_views = models.PositiveIntegerField(default=0)
    count_of_likes = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    author = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)
    community = models.ForeignKey(Community, on_delete=models.CASCADE, related_name='posts')

    def str(self):
        return self.title


class Comment(models.Model):
    body = models.TextField(max_length=1000)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def str(self):
        return f"{self.post.title} {self.body[:20]}"






