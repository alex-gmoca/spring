from django.db import models
from django.db.models import aggregates

class leaderboard_user(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    address = models.TextField(blank=True)
    points = models.IntegerField(default=0)

    def point_up(self):
        self.points += 1
        self.save()

    def point_down(self):
        self.points -= 1
        self.save()
    
    def save(self, *args, **kwargs):
        if not self.pk or self.points < 0:
            self.points = 0
        super(leaderboard_user, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-points']
