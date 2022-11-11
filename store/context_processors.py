from .models import Category

def category_context(request):
    return {
        'category_list' : Category.objects.all().order_by('name')
    }