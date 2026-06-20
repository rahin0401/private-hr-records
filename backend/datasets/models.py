from django.db import models
# Create your models here.


class DatasetField(models.Model):

    FIELD_TYPE_CHOICES = [
    ('string', 'String'),
    ('number', 'Number'),  
    ('date', 'Date'),  
    ('email', 'Email'),  
    ('boolean', 'Boolean'),  
    ('choice', 'Choice'),]

    project = models.ForeignKey('projects.Project', on_delete=models.CASCADE, related_name='dataset_fields')
    field_name = models.CharField(max_length=100)
    field_type = models.CharField(max_length=20, choices=FIELD_TYPE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.field_name




