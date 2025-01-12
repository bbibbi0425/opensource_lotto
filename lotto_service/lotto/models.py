from django.db import models

# Create your models here.

class Draw(models.Model):
    id = models.AutoField(primary_key=True)  # Django 기본 ID 필드 (자동 생성됨)
    round_number = models.IntegerField()
    winning_numbers = models.CharField(max_length=50, blank=True, null=True, default="")
    bonus_number = models.IntegerField(blank=True, null=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_winner_statistics(self):
        """
        회차별 당첨자 수를 반환하는 메서드.
        """
        winners = Ticket.objects.filter(
            draw=self,
            numbers__in=self.winning_numbers.split(",")
        ).count()
        return winners

class Ticket(models.Model):
    draw = models.ForeignKey(Draw, on_delete=models.CASCADE)  # 회차와 연결
    user = models.CharField(max_length=100)
    numbers = models.CharField(max_length=17)  # 로또 번호
    created_at = models.DateTimeField(auto_now_add=True)
