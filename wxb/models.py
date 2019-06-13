from django.db import models

# Create your models here.
class Wx_wxb(models.Model):
    wx_name = models.CharField('公众号名称',max_length=20)
    read = models.CharField('阅读数',max_length=20)
    wx_url = models.CharField('原文链接',max_length=1000)
    title = models.CharField('标题',max_length=100)
    content = models.TextField('内容',max_length=100000)
    ctime = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return "{}-{}-{}".format(self.wx_name,self.title, self.read)

    class Meta:
        verbose_name = "公众号文章"