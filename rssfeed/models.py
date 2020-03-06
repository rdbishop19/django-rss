from django.db import models

# Create your models here.
class Feed(models.Model):
    ''' Feed model '''
    title = models.CharField(max_length=255)
    description = models.TextField()
    link = models.CharField(max_length=255, unique=True)
    pub_date = models.DateTimeField(auto_now=False, auto_now_add=False)

    class Meta:
        ordering = ['-pub_date']