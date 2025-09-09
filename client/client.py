import grpc
from generated import helloworld_pb2 as pb2
from generated import helloworld_pb2_grpc as pb2_grpc
def run():
    with grpc.insecure_channel("localhost:50051") as channel:
        stub = pb2_grpc.GreeterStub(channel)
        response = stub.SayHello(pb2.HelloRequest(name="World"))
        print("Client received:", response.message)

if __name__ == "__main__":
    run()
