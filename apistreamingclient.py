from websocket import create_connection
import ssl
import websocket
from websocket._exceptions import WebSocketBadStatusException

# Load the Protobuf message definition
from protobuf import event_pb2
from protobuf import location_pb2
from protobuf import wids_pb2

event_type_decoders = {
    "com.hpe.greenlake.network-services.v1alpha1.wids-rules": wids_pb2.WidsRulesEvent,
    "com.hpe.greenlake.network-services.v1alpha1.wids-signatures": wids_pb2.WidsSignaturesEvent,
    "com.hpe.greenlake.network-services.v1alpha1.wifi-client-locations.created": location_pb2.WifiClientLocation,
}

class ApiStreamingClient:
    def __init__(self, cnx_ws_url, access_token):
        self.cnx_ws_url = cnx_ws_url
        self.access_token = access_token

    def decode_stream_event(self, event, proto):
        """Decode the stream event."""
        print(f"Event type: {event.type}")
        subject_customer_id = event.attributes['subject'].ce_string
        print(event)
        decoder = event_type_decoders.get(event.type)
        if decoder is None:
            decoded_event = f"Unhandled event type: {event.type} via {proto}"
        else:
            decoded_event = decoder()
            decoded_event.ParseFromString(event.proto_data.value)
        print(f"Decoded Event:\n{decoded_event}")

    def create_ws_connection(self, access_token, end_point, header_param=None):
        if header_param is None:
            headers = {"Authorization": "Bearer {}".format(access_token)}
        else:
            headers = header_param
        url = self.cnx_ws_url + end_point
        res = create_connection(url, header=headers, sslopt={"cert_reqs": ssl.CERT_NONE})
        return res

    def create_ws_connection_with_client_decoding(self, access_token, end_point, header_param=None):
        if header_param is None:
            headers = {"Authorization": "Bearer {}".format(access_token)}
        else:
            headers = header_param
        url = self.cnx_ws_url + end_point
        ws = create_connection(url, header=headers, sslopt={"cert_reqs": ssl.CERT_NONE}, timeout=30)
        print("ws connected")
        total = 6
        try:
            while True:
                message = ws.recv()
                print("Message recvd")
                event = event_pb2.CloudEvent()
                event.ParseFromString(message)
                event_kb_size = event.ByteSize() / 1024
                if event_kb_size < 32:
                    event_proto = 'UDP'
                else:
                    event_proto = "GRPC"
                print(f"{event_proto} Event and size is {event_kb_size} KB")
                self.decode_stream_event(event, event_proto)
        except KeyboardInterrupt:
            print("\nReceived Ctrl-C, shutting down gracefully...")
        except websocket.WebSocketException as e:
            print(f"WebSocketException Error occurred: {e}")
            raise
        except Exception as e:
            print(f"Exception : {e}")
            raise
        ws.close()
