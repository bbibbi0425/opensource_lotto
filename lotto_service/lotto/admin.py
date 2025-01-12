from django.contrib import admin
from django import forms
from .models import Draw, Ticket
import random

# Draw 모델에 대한 Form 정의
class DrawForm(forms.ModelForm):
    class Meta:
        model = Draw  # Draw 모델을 기반으로 Form 생성
        fields = '__all__'  # 모든 필드를 포함

    class Media:
        js = ('custom_draw.js',)  # custom_draw.js 파일을 Form에 포함

# Draw 모델에 대한 Admin 커스터마이징
@admin.register(Draw)
class DrawAdmin(admin.ModelAdmin):
    form = DrawForm  # DrawForm을 사용
    list_display = ('round_number', 'winning_numbers', 'bonus_number', 'created_at')  # 리스트에 표시할 필드
    actions = ['generate_random_numbers', 'show_winner_statistics']  # 관리자가 사용할 수 있는 추가 액션 등록

    # 랜덤 번호 생성 액션
    def generate_random_numbers(self, request, queryset):
        for draw in queryset:
            # 1~45 사이의 랜덤한 숫자 6개를 선택하고 정렬
            winning_numbers = sorted(random.sample(range(1, 46), 6))
            # 보너스 번호는 당첨 번호에 포함되지 않은 숫자 중에서 랜덤으로 선택
            bonus_number = random.choice([num for num in range(1, 46) if num not in winning_numbers])
            # 당첨 번호와 보너스 번호를 Draw 객체에 저장
            draw.winning_numbers = ','.join(map(str, winning_numbers))
            draw.bonus_number = bonus_number
            draw.save()  # 변경사항 저장
        # 관리자에게 메시지 표시
        self.message_user(request, "Random numbers generated successfully!")
    generate_random_numbers.short_description = "Generate random winning numbers"  # 액션 설명

    def winner_count(self, obj):

        return Ticket.objects.filter(
            draw=obj,
            numbers__in=obj.winning_numbers.split(",")
        ).count()
    winner_count.short_description = "당첨자 수"  # 관리자 화면에 표시할 이름

    # 당첨자 통계 확인 액션
    def show_winner_statistics(self, request, queryset):
        for draw in queryset:
            winner_count = Ticket.objects.filter(
                draw=draw,
                numbers__in=draw.winning_numbers.split(",")
            ).count()
            self.message_user(request, f"Round {draw.round_number}: {winner_count} winners found.")
    show_winner_statistics.short_description = "Show winner statistics"

# Ticket 모델에 대한 Admin 커스터마이징
@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('draw', 'user', 'numbers', 'created_at')  # 리스트에 표시할 필드
