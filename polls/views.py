from django.db.models import F
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from .models import Question, Choice
from django.utils import timezone

# def index(request):
#   # return HttpResponse("Hello) 기존코드
    
#   latest_question_list = Question.objects.order_by("-pub_date")[:5]
#   context = {"latest_question_list": latest_question_list}
#   return render(request, "polls/index.html", context)

# 메인 페이지 (질문 목록)
class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """
        발행일이 현재 시각보다 작거나 같은(과거인) 질문만 
        최신순으로 5개 가져오기
        """
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by("-pub_date")[:5]

# def detail(request, question_id):
#   question = get_object_or_404(Question, pk=question_id)
#   return render(request, "polls/detail.html", {"question": question})

# 질문 상세 페이지
class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"
    context_object_name = "question"
    
    
    def get_queryset(self):
        """
        미래 질문의 상세 페이지는 접근 시 404 에러가 나도록 
        조회 대상 자체를 과거 질문으로 한정
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(request, "polls/results.html", {"question": question})

# 결과 페이지
class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"
    context_object_name = "question"


# def vote(request, question_id):
#     return HttpResponse(f"You're voting on question {question_id}.")

# 투표 처리 로직 (함수형 뷰)
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        # 예외 처리: 항목을 선택하지 않고 투표를 눌렀을 때
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "You didn't select a choice.",
            },
        )
    else:
        # 성공 시: 투표수 증가 및 결과 페이지로 이동
        selected_choice.votes = F("votes") + 1
        selected_choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))


# CRUD - Create
class QuestionCreateView(generic.CreateView):
    model = Question
    fields = ["question_text" , "pub_date"]
    template_name = "polls/question_form.html"
    success_url = reverse_lazy("polls:index")

# CRUD - Update
class QuestionUpdateView(generic.UpdateView):
    model = Question
    fields = ["question_text" , "pub_date"]
    template_name = "polls/question_form.html"
    success_url = reverse_lazy("polls:index")

# CRUD - Delete
class QuestionDeleteView(generic.DeleteView):
    model = Question
    template_name = "polls/question_confirm_delete.html"
    success_url = reverse_lazy("polls:index")

# def aa(request):
#   latest_question_list = Choice.objects.order_by("-id")[:5]
#   context = {"latest_question_list": latest_question_list}
#   return render(request, "polls/aa.html", context)