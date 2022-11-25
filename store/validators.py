from django.core.exceptions import ValidationError

def validate_max_image_size(file):
    max_size_kb = 1000

    if not file.size < max_size_kb * 1024:
        raise ValidationError(f'Image size should be less than {max_size_kb}Kb.')