from django.db import models


def directory_path(instance, filename):
    return 'csv/{0}'.format(filename)


class DatasetCSV(models.Model):
    """
    Model representing one Dataset
    Attributes:
        path, created_date
    """
    filename = models.CharField(
        max_length=300,
        unique=True,
        blank=False,
        verbose_name="File name"
    )
    path = models.FileField(upload_to='csv/', max_length=300, verbose_name="Path")

    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Created date")

    def __str__(self):
        return str(self.created_date)
