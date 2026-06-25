from django.db import models
from projects.models import Project
# Create your models here.
class SyntheticDataset(models.Model):
    project = models.ForeignKey(Project,on_delete=models.CASCADE, related_name="synthetic_datasets")
    file = models.FileField(upload_to="synthetic/")
    rows_generated = models.BigIntegerField()
    quality_score = models.FloatField(default=0)
    privacy_score = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.project.name}-{self.created_at}"