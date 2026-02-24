from django.db import models

class AskModel(models.Model):
    question = models.CharField(max_length = 255)
    prediction = models.CharField(max_length = 255)    
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.question

class ComplimentModel(models.Model):
    CHOICES = (
        ('him', 'him'),
        ('her', 'her'),
    )
    name = models.CharField(max_length=255)
    for_how = models.CharField(max_length=255, choices = CHOICES)



class QuestionModel(models.Model):
    text = models.TextField(verbose_name="Текст вопроса")
    answer1 = models.CharField(max_length=255, verbose_name="Ответ 1")
    answer2 = models.CharField(max_length=255, verbose_name="Ответ 2")
    answer3 = models.CharField(max_length=255, verbose_name="Ответ 3")
    answer4 = models.CharField(max_length=255, verbose_name="Ответ 4")

    level = models.PositiveSmallIntegerField(
        choices=[(1, "Лёгкий"), (2, "Средний"), (3, "Сложный")],
        verbose_name="Уровень сложности"
    )

    correct_answer = models.PositiveSmallIntegerField(
        choices=[(1, "Ответ 1"), (2, "Ответ 2"), (3, "Ответ 3"), (4, "Ответ 4")],
        verbose_name="Правильный ответ"
    )


class TicketStat(models.Model):
    count = models.PositiveBigIntegerField(default=0)    
    lucky = models.PositiveBigIntegerField(default=0)   

class FactModel(models.Model):
    text = models.TextField()
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)

class SayingModel(models.Model):
    text = models.TextField()
    author = models.TextField()
    likes = models.PositiveIntegerField(default=0)
    dislikes = models.PositiveIntegerField(default=0)


class Number(models.Model):
    value = models.IntegerField()
    order = models.PositiveIntegerField(default=0, editable=False, db_index=True)
    used = models.BooleanField(default=False) 

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return str(self.value)