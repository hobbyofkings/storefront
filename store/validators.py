from django.core.exceptions import ValidationError

def validate_file_size(file):
    max_size_kb = 10240
    if file.size > max_size_kb * 10240:
        raise ValidationError(f'File size should not exceed {max_size_kb} KB.')

    # if less than 50kb then raise validation error
    min_size_kb = 50
    if file.size < min_size_kb * 1024:
        raise ValidationError(f'File size should not be less than {min_size_kb} KB.')










