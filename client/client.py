# import grpc
# import helloworld_pb2
# import helloworld_pb2_grpc

# def run():
#     with grpc.insecure_channel("localhost:50051") as channel:
#         stub = helloworld_pb2_grpc.GreeterStub(channel)
#         response = stub.SayHello(helloworld_pb2.HelloRequest(name="World"))
#     print("Greeter client received: " + response.message)

# if __name__ == "__main__":
#     run()

import grpc
import helloworld_pb2
import helloworld_pb2_grpc
import jwt
import time

# ========================
# Retry Interceptor
# ========================
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
                if retries < self.max_retries and e.code() in (
                    grpc.StatusCode.UNAVAILABLE,
                    grpc.StatusCode.DEADLINE_EXCEEDED,
                ):
                    retries += 1
                    print(f"[Retry] Attempt {retries} failed, retrying in {self.delay}s...")
                    time.sleep(self.delay)
                else:
                    raise

# ========================
# Client logic
# ========================
def run():
    # Generate JWT token
    token = jwt.encode({"user": "alice"}, "mysecret", algorithm="HS256")

    channel = grpc.insecure_channel("localhost:50051")
    intercept_channel = grpc.intercept_channel(channel, RetryInterceptor(max_retries=5, delay=2))
    stub = helloworld_pb2_grpc.GreeterStub(intercept_channel)

    metadata = [("authorization", token)]
    response = stub.SayHello(helloworld_pb2.HelloRequest(name="World"), metadata=metadata)
    print("✅ Greeter client received:", response.message)

if __name__ == "__main__":
    run()
