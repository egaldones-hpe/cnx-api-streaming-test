from typing import Type
from websocket import create_connection
import ssl
import websocket
from typing import TypedDict
from websocket._exceptions import WebSocketBadStatusException

# Load the Protobuf message definition
from protobuf import event_pb2
from protobuf import location_pb2
from protobuf import wids_pb2

class EventTypeDecoder(TypedDict):
    top_level_decoder: Type
    sub_msg_field: str

event_type_decoders: dict[str, EventTypeDecoder] = {
    "com.hpe.greenlake.network-services.v1alpha1.wids-rules.detection.created": {"top_level_decoder": wids_pb2.WidsStreamMessage, "sub_msg_field": "widsRulesEvent"},
    "com.hpe.greenlake.network-services.v1alpha1.wids-signatures.detection.created": {"top_level_decoder": wids_pb2.WidsStreamMessage, "sub_msg_field": "widsSignaturesEvent"},
    "com.hpe.greenlake.network-services.v1alpha1.wifi-client-locations.created": {"top_level_decoder": location_pb2.StreamLocationMessage, "sub_msg_field": "wifi_client_location"},
    "com.hpe.greenlake.network-services.v1alpha1.asset-tags.last-known-location.created": {"top_level_decoder": location_pb2.StreamLocationMessage, "sub_msg_field": "asset_tag_location"},
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
        decoder_info = event_type_decoders.get(event.type)
        if decoder_info is None:
            decoded_event = f"Unhandled event type: {event.type} via {proto}"
        else:
            message_class = decoder_info["top_level_decoder"]
            try:
                top_level_message = message_class()
                top_level_message.ParseFromString(event.proto_data.value)
                decoded_event = getattr(top_level_message, decoder_info["sub_msg_field"])
            except Exception as e:
                print(f"Error decoding event: {e}")
                decoded_event = f"Error decoding event: {e}"

        print("Decoded Event:")
        print("==============")
        print(decoded_event)

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
