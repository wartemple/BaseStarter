import datetime


class TimeUtils:
    @classmethod
    def get_now_date_str(cls):
        return datetime.datetime.now().strftime('%Y-%m-%d')

    @classmethod
    def get_now_datetime_str(cls):
        return datetime.datetime.now().strftime('%Y-%m-%d_%H%M%S')
