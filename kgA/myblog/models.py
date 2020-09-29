from django.db import models

# Create your models here.
class Category(models.Model):
    """
    问题分类
    """
    name = models.CharField(verbose_name='问题类别', max_length=20)

    class Meta:
        verbose_name = '问题类别'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
class Tag(models.Model):
    """
    问题标签
    """
    name = models.CharField(verbose_name='问题标签', max_length=20)

    class Meta:
        verbose_name = '问题标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

from django.utils import timezone

class Blog(models.Model):

    title = models.CharField(verbose_name='标题', max_length=100)
    content = models.TextField(verbose_name='正文', default='')
    create_time = models.DateTimeField(verbose_name='创建时间', default=timezone.now)
    modify_time = models.DateTimeField(verbose_name='修改时间', auto_now=True)
    click_nums = models.IntegerField(verbose_name='点击量', default=0)
    category = models.ForeignKey(Category, verbose_name='问题类别', on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag, verbose_name='问题标签')

    class Meta:
        verbose_name = '我的问题'
        verbose_name_plural = verbose_name

    def __str__(self):

        return self.title