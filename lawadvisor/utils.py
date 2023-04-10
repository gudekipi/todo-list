def get_error_message(serializer):
    for keys, values in serializer.errors.items():
        error = [value[:] for value in values]
        return error[0]