from django.core.exceptions import ValidationError


def validate_file_size(file):
    max_size_kb = 900

    if not file.size < max_size_kb * 1024:
        raise ValidationError(f'Image size should be less than {max_size_kb}Kb.')