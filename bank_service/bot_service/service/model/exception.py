class ConflictException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)