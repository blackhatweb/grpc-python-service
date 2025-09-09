from generated import helloworld_pb2
from generated import helloworld_pb2_grpc


class GreeterService(helloworld_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        return helloworld_pb2.HelloReply(message=f"Hello, {request.name}!")
