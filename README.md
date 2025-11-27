# CNX API Streaming Test

A Python client for streaming API events from HPE GreenLake Network Services. This project provides real-time streaming of network events including WiFi client locations, WIDS (Wireless Intrusion Detection System) rules, and signatures through WebSocket connections.

## Features

- **Real-time Event Streaming**: Connect to HPE GreenLake Network Services via WebSocket
- **OAuth2 Authentication**: Secure authentication using client credentials flow
- **Protocol Buffer Support**: Efficient binary serialization for network events
- **Multiple Event Types**: Support for WIDS rules, WIDS signatures, and WiFi client location events
- **Configurable**: Command-line arguments and environment variable support

## Supported Event Types

- `com.hpe.greenlake.network-services.v1alpha1.wids-rules`
- `com.hpe.greenlake.network-services.v1alpha1.wids-signatures` 
- `com.hpe.greenlake.network-services.v1alpha1.wifi-client-locations.created`
- `com.hpe.greenlake.network-services.v1alpha1.asset-tags.last-known-location.created`

## Requirements

- Python 3.8+
- Poetry (for dependency management)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd cnx-api-streaming-test
```

2. Install dependencies using Poetry:
```bash
poetry install
```

3. Activate the virtual environment:
```bash
poetry shell
```

## Configuration

The application can be configured using command-line arguments or environment variables:

### Environment Variables

```bash
export CNX_CLIENT_ID="your-client-id"
export CNX_CLIENT_SECRET="your-client-secret"
export CNX_TOKEN_URL="https://sso.common.cloud.hpe.com/as/token.oauth2"
export CNX_WEBSOCKET_URL="wss://cnx-apigw-aqua.arubadev.cloud.hpe.com"
```

### Command Line Arguments

```bash
python apistreamingtest.py \
  --client-id <your-client-id> \
  --client-secret <your-client-secret> \
  --token-url <your-token-url> \
  --websocket-url <your-websocket-url> \
  --endpoint <websocket-endpoint-path>
```

## Usage

### Basic Usage

With environment variables configured:
```bash
python apistreamingtest.py --endpoint "/network-services/v1alpha1/wids-events"
```

### Full Command Line Usage

```bash
python apistreamingtest.py \
  --client-id "your-client-id" \
  --client-secret "your-client-secret" \
  --token-url ""https://sso.common.cloud.hpe.com/as/token.oauth2" \
  --websocket-url "wss://cnx-apigw-aqua.arubadev.cloud.hpe.com" \
  --endpoint "/network-services/v1alpha1/wids-events"
```

### Using the Client Library

```python
from apistreamingclient import ApiStreamingClient

# Initialize the client
client = ApiStreamingClient(websocket_url, access_token)

# Create WebSocket connection and start streaming
client.create_ws_connection_with_client_decoding(access_token, endpoint)
```

## Project Structure

```
├── apistreamingclient.py     # Main streaming client class
├── apistreamingtest.py       # CLI application and example usage
├── protobuf/                 # Protocol Buffer generated files
│   ├── __init__.py          # Package initialization
│   ├── event_pb2.py         # Generated Protocol Buffer classes for events
│   ├── location_pb2.py      # Generated Protocol Buffer classes for locations
│   └── wids_pb2.py          # Generated Protocol Buffer classes for WIDS events
├── pyproject.toml           # Poetry configuration and dependencies
└── README.md                # This file
```

## Dependencies

- `websocket-client`: WebSocket client library
- `requests-oauthlib`: OAuth2 authentication
- `oauthlib`: OAuth2 protocol implementation
- `protobuf`: Protocol Buffer support

## Event Processing

The client automatically:

1. **Authenticates** using OAuth2 client credentials flow
2. **Connects** to the WebSocket endpoint
3. **Receives** binary Protocol Buffer messages
4. **Decodes** events based on their type
5. **Displays** event information and decoded data

Events are classified as UDP (< 32KB) or GRPC (≥ 32KB) based on their size.

## Error Handling

The client handles:
- WebSocket connection errors
- Authentication failures
- Protocol Buffer parsing errors
- Graceful shutdown on Ctrl-C

## Development

### Prerequisites

- Python 3.8+
- Poetry

### Setup Development Environment

```bash
# Install Poetry if not already installed
curl -sSL https://install.python-poetry.org | python3 -

# Install dependencies
poetry install

# Activate virtual environment
poetry shell
```

### Protocol Buffer Files

The Protocol Buffer files (`*_pb2.py`) are located in the `protobuf/` directory and are generated from `.proto` definitions. If you need to regenerate them:

```bash
# Install protoc compiler
# On macOS: brew install protobuf
# On Ubuntu: apt-get install protobuf-compiler

# Generate Python classes (example)
protoc --python_out=protobuf/ event.proto location.proto wids.proto
```

## License

This project is part of HPE GreenLake Network Services development and testing.

## Support

For issues and questions related to HPE GreenLake Network Services API, please refer to the official HPE documentation or contact support.
