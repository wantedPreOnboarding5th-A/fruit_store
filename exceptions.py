class CustomBaseExecption(Exception):
    is_custom_execption = True


class NotFoundError(CustomBaseExecption):
    def __init__(self):
        self.msg = "Data Not Found. Please Check ID"
