# Pair-Pipeline

<br>

![My Logo](image/iot.jpeg)

<br>
<br>


Pair-Pipeline is a Flask-based API designed for managing pipelines and securely storing key-value data for IoT devices. This API enables efficient communication and data handling between IoT systems and supports CRUD operations for pipeline IDs and associated data. 

The application is live and accessible at: [https://lolenseu.pythonanywhere.com/](https://lolenseu.pythonanywhere.com/)

---

## Features

- **IoT Integration**: Designed to handle data from IoT devices.
- **Pipeline Management**: Create, confirm, update, and validate pipeline IDs and keys.
- **Data Handling**: Store and retrieve structured data securely.
- **Public IP Retrieval**: Fetch the server's public IP address.
- **Error Handling**: Custom error messages for invalid or malformed requests.
- **RESTful Routes**: API endpoints for interacting with the pipeline and megastream services.

---

## Live Testing

You can test the live application hosted at [https://lolenseu.pythonanywhere.com/pipeline](https://lolenseu.pythonanywhere.com/pipeline). Below are some example requests:

### Example Requests

#### Home Endpoint
- **URL**: [https://lolenseu.pythonanywhere.com/pipeline](https://lolenseu.pythonanywhere.com/pipeline)
- **Method**: `GET`
- **Response**:
    ```json
    {
        "message": "Welcome to Pair-Pipeline!",
        "response": "success!",
        "timestamp": "<current_timestamp>"
    }
    ```

#### Megastream Endpoint
- **URL**: [https://lolenseu.pythonanywhere.com/pipeline/megastream](https://lolenseu.pythonanywhere.com/pipeline/megastream)
- **Method**: `GET`
- **Response**:
    ```json
    {
        "server_ip": "<server_public_ip>",
        "total_id": <total_ids_created>,
        "timestamp": "<current_timestamp>"
    }
    ```

#### Create Pipeline (`cre`)
- **URL**: [https://lolenseu.pythonanywhere.com/pipeline/stream](https://lolenseu.pythonanywhere.com/pipeline/stream)
- **Method**: `POST`
- **Query Parameters**:
    - `opt=cre`
    - `id=12345678` (8-digit pipeline ID)
    - `key=abcdefghijklmnop` (16-character pipeline key)
- **Example Request**:
    ```bash
    https://lolenseu.pythonanywhere.com/pipeline/stream?opt=cre&id=12345678&key=abcdefghijklmnop
    ```

    ```bash
    curl -X POST "https://lolenseu.pythonanywhere.com/pipeline/stream?opt=cre&id=12345678&key=abcdefghijklmnop"
    ```
- **Response**:
    ```json
    {
        "response": "success!",
        "message": "Pipeline created successfully",
        "id": "12345678",
        "timestamp": "<current_timestamp>"
    }
    ```

#### Update Key (`upk`)
- **URL**: [https://lolenseu.pythonanywhere.com/pipeline/stream](https://lolenseu.pythonanywhere.com/pipeline/stream)
- **Method**: `POST`
- **Query Parameters**:
    - `opt=upk`
    - `id=12345678` (8-digit pipeline ID)
    - `key=abcdefghijklmnop` (16-character pipeline key)
    - `nkey=abcdefghijklmnop` (16-character pipeline newkey)
- **Example Request**:
    ```bash
    https://lolenseu.pythonanywhere.com/pipeline/stream?opt=upk&id=12345678&key=abcdefghijklmnop&nkey=abcdefghijklmnop
    ```

    ```bash
    curl -X POST "https://lolenseu.pythonanywhere.com/pipeline/stream?opt=upk&id=12345678&key=abcdefghijklmnop&nkey=abcdefghijklmnop"
    ```
- **Response**:
    ```json
    {
        "response": "success!",
        "message": "Key updated successfully",
        "id": "12345678",
        "timestamp": "<current_timestamp>"
    }
    ```

#### Send Data (`snd`)
- **URL**: [https://lolenseu.pythonanywhere.com/pipeline/stream](https://lolenseu.pythonanywhere.com/pipeline/stream)
- **Method**: `POST`
- **Query Parameters**:
  - `opt=snd` (required): Specifies the operation.
  - `id=12345678` (required): The 8-digit pipeline ID.
  - `key=abcdefghijklmnop` (required): The 16-character pipeline key.
  - `ivp1`, `ivp2`, ..., `ivp8` (optional): Integer virtual pins (1-8, each max 4 digits).
  - `svp1`, `svp2`, ..., `svp4` (optional): String virtual pins (1-4, each max 128 characters).
- **Example Request**:
    ```bash
    https://lolenseu.pythonanywhere.com/pipeline/stream?opt=snd&id=12345678&key=abcdefghijklmnop&ivp1=123&ivp2=456&svp1=hello&svp2=world
    ```
    
    ```bash
    curl -X POST "https://lolenseu.pythonanywhere.com/pipeline/stream?opt=snd&id=12345678&key=abcdefghijklmnop&ivp1=123&ivp2=456&svp1=hello&svp2=world"
    ```
- **Response**:
    ```json
    {
        "response": "success!",
        "message": "Data sent successfully",
        "id": "12345678",
        "timestamp": "2024-12-25T12:00:00Z"
    }
    ```

#### Retrieve Data (`rcv`)
- **URL**: [https://lolenseu.pythonanywhere.com/pipeline/stream](https://lolenseu.pythonanywhere.com/pipeline/stream)
- **Method**: `POST`
- **Query Parameters**:
    - `opt=rcv`
    - `id=12345678`
    - `key=abcdefghijklmnop`
- **Example Request**:
    ```bash
    https://lolenseu.pythonanywhere.com/pipeline/stream?opt=rcv&id=12345678&key=abcdefghijklmnop
    ```

    ```bash
    curl -X POST "https://lolenseu.pythonanywhere.com/pipeline/stream?opt=rcv&id=12345678&key=abcdefghijklmnop"
    ```
- **Response**:
    ```json
    {
        "response": "success!",
        "message": "Data retrieved successfully",
        "id": "12345678",
        "timestamp": "<current_timestamp>",
        "stream": {
        "int_virtual_pin": {
            "ivp1": 123,
            "ivp2": 456
        },
        "str_virtual_pin": {
            "svp1": "hello",
            "svp2": "world"
        }
    }
    ```

## Local Testing

### Prerequisites

- Python 3.8 or later
- Flask (`pip install flask`)
- Requests (`pip install requests`)

---

### Installation

1. Clone this repository:
    ```bash
    git clone https://github.com/your-repo/pair-pipeline.git
    cd pair-pipeline
    ```

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Run the application:
    ```bash
    python app.py
    ```

---

### API Endpoints

#### Home
- **URL**: `http://localhost:5000/`
- **Method**: `GET, POST`
- **Response**:
    ```json
    {
        "message": "Welcome to Pair-Pipeline!"
    }
    ```

#### Megastream
- **URL**: `http://localhost:5000/pipeline/megastream`
- **Method**: `GET, POST`
- **Response**:
    ```json
    {
        "server_ip": "<server_public_ip>",
        "total_id": <total_ids_created>,
        "timestamp": "<current_timestamp>"
    }
    ```

#### Pipeline
- **URL**: `http://localhost:5000/pipeline/stream`
- **Method**: `GET, POST`
- **Query Parameters**:
  - `opt` (required): Operation type (`cre`, `upk`, `snd`, `rcv`)
  - `id` (required): Pipeline ID (8 digits)
  - `key` (required): Pipeline Key (16 characters)
  - `nkey` (optional): New Pipeline Key (16 characters)
  - `ivp1-ivp8` (optional): Integer virtual pins (1-8, max 4 digits)
  - `svp1-svp4` (optional): String virtual pins (1-4, max 128 characters)

---

### Pipeline Operations
Creates a new pipeline ID.
- **Success**:
    ```json
    {
        "response": "success!",
        "message": "Pipeline created successfully",
        "id": "<pipeline_id>",
        "timestamp": "<current_timestamp>"
    }
    ```
- **Error**:
    ```json
    {
        "response": "error!",
        "message": "<error_message>",
        "id": "<pipeline_id>",
        "timestamp": "<current_timestamp>"
    }
    ```

#### Create pipeline (`cre`)
Create new pipeline.

#### Update Key (`upk`)
Updates the key for an existing pipeline ID.

#### Send Data (`snd`)
Stores integer and string data for a pipeline ID.

#### Retrieve Data (`rcv`)
Retrieve stored data for a pipeline ID.

---

### Error Handling

All error responses return a `400` status code with a descriptive message:
```json
{
    "response": "error!",
    "message": "<error_description>",
    "id": "<pipeline_id>",
    "timestamp": "<current_timestamp>"
}
```

## Powered by

This app is running on pythonanywhere.com [PythonAnywhere](https://www.pythonanywhere.com/).

## License

This package is open-sourced software licensed under the [MIT license](https://opensource.org/licenses/MIT).
