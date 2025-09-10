import grpc, time, logging

logging.basicConfig(level=logging.INFO)

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
