# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
import polypuppet.polypuppet_pb2 as polypuppet__pb2


class RemoteConnectionStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.login_user = channel.unary_unary(
                '/RemoteConnection/login_user',
                request_serializer=polypuppet__pb2.User.SerializeToString,
                response_deserializer=polypuppet__pb2.Profile.FromString,
                )
        self.login_classroom = channel.unary_unary(
                '/RemoteConnection/login_classroom',
                request_serializer=polypuppet__pb2.Classroom.SerializeToString,
                response_deserializer=polypuppet__pb2.Profile.FromString,
                )


class RemoteConnectionServicer(object):
    """Missing associated documentation comment in .proto file."""

    def login_user(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def login_classroom(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_RemoteConnectionServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'login_user': grpc.unary_unary_rpc_method_handler(
                    servicer.login_user,
                    request_deserializer=polypuppet__pb2.User.FromString,
                    response_serializer=polypuppet__pb2.Profile.SerializeToString,
            ),
            'login_classroom': grpc.unary_unary_rpc_method_handler(
                    servicer.login_classroom,
                    request_deserializer=polypuppet__pb2.Classroom.FromString,
                    response_serializer=polypuppet__pb2.Profile.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'RemoteConnection', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class RemoteConnection(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def login_user(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/RemoteConnection/login_user',
            polypuppet__pb2.User.SerializeToString,
            polypuppet__pb2.Profile.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def login_classroom(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/RemoteConnection/login_classroom',
            polypuppet__pb2.Classroom.SerializeToString,
            polypuppet__pb2.Profile.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)


class LocalConnectionStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.manage_token = channel.unary_unary(
                '/LocalConnection/manage_token',
                request_serializer=polypuppet__pb2.Token.SerializeToString,
                response_deserializer=polypuppet__pb2.Token.FromString,
                )
        self.autosign = channel.unary_unary(
                '/LocalConnection/autosign',
                request_serializer=polypuppet__pb2.Certname.SerializeToString,
                response_deserializer=polypuppet__pb2.Autosign.FromString,
                )
        self.stop = channel.unary_unary(
                '/LocalConnection/stop',
                request_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
                response_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                )


class LocalConnectionServicer(object):
    """Missing associated documentation comment in .proto file."""

    def manage_token(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def autosign(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def stop(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_LocalConnectionServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'manage_token': grpc.unary_unary_rpc_method_handler(
                    servicer.manage_token,
                    request_deserializer=polypuppet__pb2.Token.FromString,
                    response_serializer=polypuppet__pb2.Token.SerializeToString,
            ),
            'autosign': grpc.unary_unary_rpc_method_handler(
                    servicer.autosign,
                    request_deserializer=polypuppet__pb2.Certname.FromString,
                    response_serializer=polypuppet__pb2.Autosign.SerializeToString,
            ),
            'stop': grpc.unary_unary_rpc_method_handler(
                    servicer.stop,
                    request_deserializer=google_dot_protobuf_dot_empty__pb2.Empty.FromString,
                    response_serializer=google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'LocalConnection', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class LocalConnection(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def manage_token(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/LocalConnection/manage_token',
            polypuppet__pb2.Token.SerializeToString,
            polypuppet__pb2.Token.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def autosign(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/LocalConnection/autosign',
            polypuppet__pb2.Certname.SerializeToString,
            polypuppet__pb2.Autosign.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def stop(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/LocalConnection/stop',
            google_dot_protobuf_dot_empty__pb2.Empty.SerializeToString,
            google_dot_protobuf_dot_empty__pb2.Empty.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
