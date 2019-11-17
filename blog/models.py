from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse


# Create your models here.

class Post(models.Model):
	
	STATUS_CHOICES = (
		('draft', 'Удален'),
		('published', 'Опубликован'),
	)

	title = models.CharField(max_length=250, verbose_name='Заголовок')
	slug = models.SlugField(max_length=250, unique_for_date='publish', verbose_name='Идентификатор')
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts', verbose_name='Автор')
	body = models.TextField(verbose_name='Текст')
	publish = models.DateTimeField(default=timezone.now, editable=False, verbose_name='Опубликован')
	created = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
	updated = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
	status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft', verbose_name='Статус')

	class Meta:
		verbose_name = 'Пост'
		verbose_name_plural = 'Посты'
		ordering = ('-publish',)	

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('blog:post-detail', kwargs={
			'year': self.publish.year, 
			'month': self.publish.month, 
			'day': self.publish.day, 
			'post': self.slug})


class Comment(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
	name = models.CharField(max_length=80, verbose_name='Написал')
	email = models.EmailField(verbose_name='Электронная почта')
	body = models.TextField(verbose_name='Текст')
	created = models.DateTimeField(auto_now_add=True,verbose_name='Размещен')
	updated = models.DateTimeField(auto_now=True, verbose_name='Изменен')
	active = models.BooleanField(default=True,verbose_name='Активный')

	class Meta:
			verbose_name = 'Комментарий'
			verbose_name_plural = 'Комментарии'
			ordering = ('-created',)

	def __str__(self):
		return 'Comment by {} on {}'.format(self.name, self.post)