class RateLimitError(Exception):
    def __init__(self, message="Rate limit exceeded", retry_after=None):
        super().__init__(message)
        self.retry_after = retry_after
