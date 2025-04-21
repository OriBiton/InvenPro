from django.db import models

class Product(models.Model):
    id = models.AutoField(primary_key=True)  # מזהה ייחודי שמגדיל את עצמו אוטומטית
    model = models.CharField(max_length=100)  # מודל המוצר
    deploying_number = models.CharField(max_length=50)  # מספר פריסה (חייב להיות ייחודי)
    date = models.DateField()  # תאריך יצירת הפריט
    height = models.FloatField()  # גובה
    width = models.FloatField()  # רוחב
    TYPE_CHOICES = [
        ("פלטה", "פלטה"),
        ("חתיכה", "חתיכה")
    ]
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)  # סוג הפריט (רק "פלטה" או "חתיכה")
    count = models.PositiveIntegerField(default=1)  # כמות הפריטים

    def __str__(self):
        return f"{self.model} - {self.deploying_number} ({self.type})"
