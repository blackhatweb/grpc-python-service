# import grpc
# from concurrent import futures
# import time

# import helloworld_pb2
# import helloworld_pb2_grpc

# from opentelemetry import trace
# from opentelemetry.sdk.trace import TracerProvider
# from opentelemetry.sdk.trace.export import BatchSpanProcessor
# from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
# from opentelemetry.instrumentation.grpc import GrpcInstrumentorServer

# # Setup Tracer
# trace.set_tracer_provider(TracerProvider())
# tracer = trace.get_tracer(__name__)
# otlp_exporter = OTLPSpanExporter()
# trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(otlp_exporter))

# # Instrument gRPC server
# GrpcInstrumentorServer().instrument()

# # Implement service
# class GreeterServicer(helloworld_pb2_grpc.GreeterServicer):
#     def SayHello(self, request, context):
#         return helloworld_pb2.HelloReply(message=f"Hello, {request.name}!")

# def serve():
#     server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
#     helloworld_pb2_grpc.add_GreeterServicer_to_server(GreeterServicer(), server)
#     server.add_insecure_port("[::]:50051")
#     server.start()
#     print("Server started at port 50051...")
#     try:
#         while True:
#             time.sleep(86400)
#     except KeyboardInterrupt:
#         server.stop(0)

# if __name__ == "__main__":
#     serve()

import grpc
from concurrent import futures
import time
import logging

import helloworld_pb2
import helloworld_pb2_grpc

# ========================
# Logging Interceptor
# ========================
class LoggingInterceptor(grpc.ServerInterceptor):
    def intercept_service(self, continuation, handler_call_details):
        method = handler_call_details.method
        def wrapper(request, context):
            start = time.time()
            response = continuation(handler_call_details).unary_unary(request, context)
            duration = (time.time() - start) * 1000
            logging.info(f"[gRPC] {method} took {duration:.2f} ms")
            return response

        return grpc.unary_unary_rpc_method_handler(
            wrapper,
            request_deserializer=continuation(handler_call_details).request_deserializer,
            response_serializer=continuation(handler_call_details).response_serializer,
        )

# ========================
# Auth Interceptor (JWT)
# ========================
import jwt
SECRET_KEY = "mysecret"

class AuthInterceptor(grpc.ServerInterceptor):
    def intercept_service(self, continuation, handler_call_details):
        def wrapper(request, context):
            metadata = dict(context.invocation_metadata())
            token = metadata.get("authorization")
            if not token:
                context.abort(grpc.StatusCode.UNAUTHENTICATED, "Missing token")
            try:
                jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            except jwt.InvalidTokenError:
                context.abort(grpc.StatusCode.UNAUTHENTICATED, "Invalid token")
            return continuation(handler_call_details).unary_unary(request, context)

        return grpc.unary_unary_rpc_method_handler(
            wrapper,
            request_deserializer=continuation(handler_call_details).request_deserializer,
            response_serializer=continuation(handler_call_details).response_serializer,
        )

# ========================
# gRPC Service
# ========================
class GreeterServicer(helloworld_pb2_grpc.GreeterServicer):
    def SayHello(self, request, context):
        return helloworld_pb2.HelloReply(message=f"Hello, {request.name}!")

# ========================
# Main
# ========================
def serve():
    logging.basicConfig(level=logging.INFO)

    interceptors = [
        LoggingInterceptor(),
        AuthInterceptor()
    ]

    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10),
        interceptors=interceptors
    )
    helloworld_pb2_grpc.add_GreeterServicer_to_server(GreeterServicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    print("🚀 gRPC Server started at port 50051...")
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        print("Stopping server...")
        server.stop(0)

if __name__ == "__main__":
    serve()
