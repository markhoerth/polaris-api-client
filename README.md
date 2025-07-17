# Polaris Catalog Client

A simple Python script to interact with Apache Polaris catalog API.

## Setup

1. Install dependencies:
```bash
pip install requests
```

2. Set environment variables (optional):
```bash
export POLARIS_HOST="your-host:port"
export POLARIS_CLIENT_ID="your-client-id"  
export POLARIS_CLIENT_SECRET="your-client-secret"
```

If not set, defaults to:
- Host: `localhost:8183`
- Client ID: `admin`
- Client Secret: `admin`

## Usage

```bash
python polaris_api_client.py
```

## What it does

1. Gets an authentication token
2. Lists catalogs
3. Lists namespaces in the specified catalog
4. Lists tables in the specified namespace
5. Shows table metadata and snapshots

## Configuration

Edit these variables in the script:
```python
catalog_name = "polaris4"
namespace_name = "polaris4_namespace" 
table_name = "customers"
```

## Output

The script prints raw API responses so you can see exactly what the server returns. This helps debug any issues with listing namespaces or tables.
