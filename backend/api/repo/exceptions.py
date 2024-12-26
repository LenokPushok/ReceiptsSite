class BaseRepoError(Exception):
    def __init__(self):
        super().__init__()
        self.detail = ""

    def __str__(self):
        return self.detail


class NotFoundError(BaseRepoError):
    def __init__(self, orm_model_name: str):
        super().__init__()
        self.detail = f"Not found for {orm_model_name}"


class MultipleFoundError(BaseRepoError):
    def __init__(self, orm_model_name: str):
        super().__init__()
        self.detail = f"Multiple result found for {orm_model_name}"
