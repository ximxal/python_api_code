
__error_count = 0

def decorator(func):
    def log_func(*arg, **kvargs):
        global __error_count
        try:
            return func(*arg, **kvargs)
        except:
            if(__error_count < 10):
                __error_count = __error_count + 1
                print(func, "<error>")
            #pass
    return log_func