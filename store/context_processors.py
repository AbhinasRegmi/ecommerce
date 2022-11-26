from .models import Category

def category_context(request):
    return {
        'category_list' : Category.objects.filter(level=0).order_by('name')
    }