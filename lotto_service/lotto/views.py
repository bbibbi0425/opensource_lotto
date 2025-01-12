from django.shortcuts import render
from django.http import JsonResponse
from .models import Ticket, Draw
import random

# 등수 계산 함수
def check_rank(ticket_numbers, winning_numbers, bonus_number):
    match_count = len(set(ticket_numbers) & set(winning_numbers))
    has_bonus = bonus_number in ticket_numbers

    # 등수 계산
    if match_count == 6:  # 모든 숫자 일치
        return "1등"
    elif match_count == 5:
        if has_bonus:  # 5개 일치 + 보너스 번호
            return "2등"
        return "3등"  # 5개 일치 (보너스 번호 없음)
    elif match_count == 4:
        return "4등"  # 4개 일치
    elif match_count == 3:
        return "5등"  # 3개 일치
    else:
        return "꽝"  # 나머지

# 로또 페이지 View
def lotto_page(request):
    if request.method == "POST":
        # 티켓 구매 처리
        user = request.POST.get("user")
        numbers = request.POST.get("numbers")
        draw = Draw.objects.latest('round_number')  # 최신 회차 가져오기

        # 번호 검증
        if numbers:
            try:
                numbers_list = list(map(int, numbers.split(',')))
                if len(numbers_list) != 6 or not all(1 <= num <= 45 for num in numbers_list):
                    return JsonResponse({"error": "Numbers must be 6 integers between 1 and 45!"}, status=400)
            except ValueError:
                return JsonResponse({"error": "Invalid number format. Please enter comma-separated integers."}, status=400)
        else:
            numbers_list = sorted(random.sample(range(1, 46), 6))

        Ticket.objects.create(
            user=user,
            numbers=','.join(map(str, numbers_list)),
            draw=draw
        )
        return JsonResponse({"message": "Ticket purchased successfully!", "numbers": numbers_list})

    if request.method == "GET" and request.GET.get("action") == "check_results":
    # 특정 회차 확인
        round_number = request.GET.get("round")
        if not round_number:
            return JsonResponse({"error": "Please provide a round number."}, status=400)

        try:
            draw = Draw.objects.get(round_number=round_number)
        except Draw.DoesNotExist:
            return JsonResponse({"error": "Round not found."}, status=404)

        tickets = Ticket.objects.filter(draw=draw)
        winning_numbers = list(map(int, draw.winning_numbers.split(',')))
        bonus_number = draw.bonus_number

        results = []
        for ticket in tickets:
            ticket_numbers = list(map(int, ticket.numbers.split(',')))
            rank = check_rank(ticket_numbers, winning_numbers, bonus_number)
            results.append({"user": ticket.user, "numbers": ticket.numbers, "rank": rank})

        return JsonResponse({
            "results": results,
            "round": draw.round_number,
            "winning_numbers": draw.winning_numbers,
            "bonus_number": draw.bonus_number
        })


    # 모든 회차 정보 가져오기
    draws = Draw.objects.all().order_by('-round_number')
    return render(request, "lotto_page.html", {"draws": draws})
