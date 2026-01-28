import datetime
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from django.views import generic

from .models import Question

#공통함수
def parse_yyyy_mm_dd(value : str):
    try : 
        return datetime.date.fromisoformat(value)
    except (TypeError, ValueError):
        return None

def practice_1(request):
    q = request.GET.get("q")  # "q" 값을 꺼내기
    return HttpResponse(f"q는 지금: {q}")


def practice_api_1(request):
    q = request.GET.get("q")
    return JsonResponse({"q": q})


def practice_2(request):
    qs = Question.objects.all()
    q = request.GET.get("q")

    if q:
        qs = qs.filter(question_text__icontains=q)

    return HttpResponse(f"검색어: {q} / 결과 개수: {qs.count()}")

def practice_api_2(request):
    qs = Question.objects.all()
    q = request.GET.get("q")

    if q:
        qs = qs.filter(question_text__icontains=q)

    return JsonResponse({
        "q": q,
        "count": qs.count(),
        "results": [{"id": x.id, "text": x.question_text} for x in qs[:10]]
    })


def practice_3(request):
    qs = Question.objects.all()
    show = request.GET.get("show")

    if show != "future" :
        qs = qs.filter(pub_date__lte=timezone.now())
    
    return HttpResponse(f"show= {show} / 결과 :{qs.count()}" )

def practice_api_3(request):
    qs = Question.objects.all()
    show = request.GET.get("show")

    if show != "future" :
        qs = qs.filter(pub_date__lte=timezone.now())
    
    return JsonResponse({
        "show" : show,
        "count" : qs.count(),
        "results": [{"id": x.id, "text": x.question_text} for x in qs[:10]]
    })


def practice_5(request):
    qs = Question.objects.all()

    start_raw = request.GET.get("start")
    end_raw = request.GET.get("end")

    start = parse_yyyy_mm_dd(start_raw)
    end = parse_yyyy_mm_dd(end_raw)

    if start:
        qs = qs.filter(pub_date__date__gte=start)

    if end:
        qs = qs.filter(pub_date__date__lte=end)

    return HttpResponse(f"start={start} end={end} / 결과:{qs.count()}")

def practice_api_5(request):
    qs = Question.objects.all()
    start_raw = request.GET.get("start")
    end_raw = request.GET.get("end")

    start = parse_yyyy_mm_dd(start_raw)
    end = parse_yyyy_mm_dd(end_raw)

    if start:
        qs = qs.filter(pub_date__date__gte=start)
    if end:
        qs = qs.filter(pub_date__date__lte=end)

    return JsonResponse({
        "start_raw": start_raw,
        "end_raw": end_raw,
        "start": start.isoformat() if start else None,
        "end": end.isoformat() if end else None,
        "count": qs.count(),
    })


def practice_6(request):
    qs = Question.objects.all()
    order = request.GET.get("order")

    if order == "oldest":
        qs = qs.order_by("pub_date")
    else:
        qs = qs.order_by("-pub_date")

    first = qs.first()
    return HttpResponse(f"order={order} / 첫 데이터: {first.pub_date if first else None}")

def practice_api_6(request):
    qs = Question.objects.all()
    order = request.GET.get("order")

    if order == oldest:
        qs = qs.order_by("pub_date")
    else:
        qs = qs.order_by("-pub_date")

    return JsonResponse({
        "order": order,
        "first_pub_date": qs.first().pub_date.isoformat() if qs.exists() else None,
        "results": [{"id": x.id, "pub_date": x.pub_date.isoformat()} for x in qs[:5]]
    })