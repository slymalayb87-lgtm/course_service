from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.forms.models import model_to_dict
from .models import Course
import json

@csrf_exempt
@require_http_methods(["GET", "POST"])
def course_list(request):
    if request.method == "GET":
        q = request.GET.get("q", "")
        courses = Course.objects.filter(name__icontains=q) | Course.objects.filter(category__icontains=q)
        data = [model_to_dict(c) for c in courses]
        return JsonResponse(data, safe=False)

    if request.method == "POST":
        body = json.loads(request.body.decode("utf-8"))
        course = Course.objects.create(
            name=body.get("name", ""),
            category=body.get("category", ""),
            description=body.get("description", ""),
            schedule=body.get("schedule", "")
        )
        return JsonResponse(model_to_dict(course), status=201)


@csrf_exempt
@require_http_methods(["GET", "PUT", "DELETE"])
def course_detail(request, id):
    try:
        course = Course.objects.get(pk=id)
    except Course.DoesNotExist:
        return JsonResponse({"error": "Course not found"}, status=404)

    if request.method == "GET":
        return JsonResponse(model_to_dict(course))

    if request.method == "PUT":
        body = json.loads(request.body.decode("utf-8"))
        for field in ["name", "category", "description", "schedule"]:
            if field in body:
                setattr(course, field, body[field])
        course.save()
        return JsonResponse(model_to_dict(course))

    if request.method == "DELETE":
        course.delete()
        return JsonResponse({"message": "Deleted successfully"})
