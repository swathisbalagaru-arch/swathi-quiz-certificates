from django.db.models import Avg, Count
from django.http import Http404, JsonResponse
from django.shortcuts import redirect, render

from .models import PASS_PERCENT, Result
from .questions import QUIZZES


def _student(request):
    return request.session.get("student_name")


def entry(request):
    if request.method == "POST":
        name = request.POST.get("name", "").strip()[:100]
        if not name:
            return render(request, "quiz/login.html", {"error": "Please enter your name."})
        request.session["student_name"] = name
        return redirect("home")
    return render(request, "quiz/login.html")


def logout_view(request):
    request.session.flush()
    return redirect("entry")


def home(request):
    name = _student(request)
    if not name:
        return redirect("entry")
    cats = [{"name": c, "count": len(qs)} for c, qs in QUIZZES.items()]
    mine = Result.objects.filter(student_name=name)[:10]
    return render(request, "quiz/home.html", {"name": name, "categories": cats, "mine": mine, "pass_percent": PASS_PERCENT})


def take_quiz(request, category):
    name = _student(request)
    if not name:
        return redirect("entry")
    questions = QUIZZES.get(category)
    if questions is None:
        raise Http404("Unknown quiz category")

    if request.method == "POST":
        score = 0
        for i, item in enumerate(questions):
            if request.POST.get(f"q{i}") == str(item["answer"]):
                score += 1
        result = Result.objects.create(
            student_name=name, category=category, score=score, total=len(questions)
        )
        return redirect("result", code=result.certificate_id)

    return render(request, "quiz/quiz.html", {"category": category, "questions": list(enumerate(questions))})


def result_page(request, code):
    try:
        result = Result.objects.get(certificate_id=code)
    except Result.DoesNotExist:
        raise Http404("Result not found")
    return render(request, "quiz/result.html", {"r": result, "pass_percent": PASS_PERCENT})


def certificate(request, code):
    try:
        result = Result.objects.get(certificate_id=code)
    except Result.DoesNotExist:
        raise Http404("Certificate not found")
    if not result.passed:
        raise Http404("No certificate for a failed attempt")
    return render(request, "quiz/certificate.html", {"r": result})


def verify(request):
    code = request.GET.get("code", "").strip().upper()
    result = None
    searched = bool(code)
    if code:
        result = Result.objects.filter(certificate_id=code).first()
        if result and not result.passed:
            result = None
    return render(request, "quiz/verify.html", {"code": code, "r": result, "searched": searched})


def _as_dict(r):
    return {
        "student_name": r.student_name,
        "category": r.category,
        "score": r.score,
        "total": r.total,
        "percent": r.percent,
        "passed": r.passed,
        "certificate_id": r.certificate_id,
        "date": r.created_at.isoformat(),
    }


def results_json(request):
    return JsonResponse({"results": [_as_dict(r) for r in Result.objects.all()]})


def student_results_json(request, student_name):
    rows = Result.objects.filter(student_name__iexact=student_name)
    return JsonResponse({"student": student_name, "results": [_as_dict(r) for r in rows]})


def summary_json(request):
    agg = Result.objects.aggregate(attempts=Count("id"), avg=Avg("score"))
    return JsonResponse({
        "total_attempts": agg["attempts"],
        "average_score": round(agg["avg"], 2) if agg["avg"] is not None else 0,
    })
