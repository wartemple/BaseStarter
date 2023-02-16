

class HttpUtils:
    @classmethod
    def has_http_only(cookie):
        extra_args = cookie.__dict__.get('_rest')
        if extra_args:
            for key in extra_args.keys():
                if key.lower() == 'httponly':
                    return True
        return False