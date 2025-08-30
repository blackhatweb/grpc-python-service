import grpc
import time

class RetryInterceptor(grpc.UnaryUnaryClientInterceptor):
    def __init__(self, max_retries=3, delay=1):
        self.max_retries = max_retries
        self.delay = delay

    def intercept_unary_unary(self, continuation, client_call_details, request):
        retries = 0
        while True:
            try:
                return continuation(client_call_details, request)
            except grpc.RpcError as e:
                if retries < self.max_retries and e.code() in (grpc.StatusCode.UNAVAILABLE, grpc.StatusCode.DEADLINE_EXCEEDED):
                    retries += 1
                    time.sleep(self.delay)
                else:
                    raise
