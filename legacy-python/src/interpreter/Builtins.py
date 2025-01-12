class Builtins:
    def __init__(self, interpreter):
        self.interpreter = interpreter

    def builtin_print(self, *args):
        print(*args)
        return None

    def builtin_printf(self, format_string: str, *args):
        print(self.builtin_sprintf(format_string, *args))
        return None

    def builtin_sprintf(self, format_string: str, *args):
        if not isinstance(format_string, str):
            raise Exception("First argument to sprintf must be a string.")

        try:
            formatted_output = format_string % args
        except TypeError as e:
            raise Exception(f"Error in sprintf formatting: {e}")

        return formatted_output
