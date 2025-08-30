import grpc
import jwt

SECRET_KEY = "mysecret"

class AuthInterceptor(grpc.ServerInterceptor):
    def intercept_service(self, continuation, handler_call_details):
        def new_behavior(request, context):
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
            new_behavior,
            request_deserializer=continuation(handler_call_details).request_deserializer,
            response_serializer=continuation(handler_call_details).response_serializer,
        )
