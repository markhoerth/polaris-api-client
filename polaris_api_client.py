#!/usr/bin/env python3
"""
Simple Polaris Catalog API Client
"""

import json
import requests
import os

# Configuration
POLARIS_HOST = os.getenv("POLARIS_HOST", "localhost:8183")
CLIENT_ID = os.getenv("POLARIS_CLIENT_ID", "admin")
CLIENT_SECRET = os.getenv("POLARIS_CLIENT_SECRET", "admin")

def get_token():
    """Get authentication token"""
    print("Getting authentication token...")
    
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    form_data = {
        "scope": "PRINCIPAL_ROLE:ALL",
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }
    
    url = f"http://{POLARIS_HOST}/api/catalog/v1/oauth/tokens"
    response = requests.post(url, headers=headers, data=form_data)
    response.raise_for_status()
    
    token = response.json()["access_token"]
    print(f"Token: {token}")
    return token

def get_headers(token):
    """Get request headers with token"""
    return {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

def list_catalogs(token):
    """List all catalogs"""
    print("\nListing catalogs...")
    
    url = f"http://{POLARIS_HOST}/api/management/v1/catalogs"
    response = requests.get(url, headers=get_headers(token))
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Parsed JSON: {data}")
        return data
    return None

def list_namespaces(token, catalog_name):
    """List namespaces in a catalog"""
    print(f"\nListing namespaces in catalog '{catalog_name}'...")
    
    url = f"http://{POLARIS_HOST}/api/catalog/v1/{catalog_name}/namespaces"
    response = requests.get(url, headers=get_headers(token))
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Parsed JSON: {data}")
        return data
    return None

def list_tables(token, catalog_name, namespace_name):
    """List tables in a namespace"""
    print(f"\nListing tables in namespace '{namespace_name}'...")
    
    url = f"http://{POLARIS_HOST}/api/catalog/v1/{catalog_name}/namespaces/{namespace_name}/tables"
    response = requests.get(url, headers=get_headers(token))
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Parsed JSON: {data}")
        return data
    return None

def create_catalog(token, catalog_name, base_location, storage_config):
    """Create a new catalog"""
    print(f"\nCreating catalog '{catalog_name}'...")
    
    url = f"http://{POLARIS_HOST}/api/management/v1/catalogs"
    
    data = {
        "type": "INTERNAL",
        "name": catalog_name,
        "properties": {
            "default-base-location": base_location
        },
        "storageConfigInfo": storage_config
    }
    
    response = requests.post(url, headers=get_headers(token), json=data)
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code in [200, 201]:
        data = response.json()
        print(f"Created catalog successfully: {data}")
        return data
    return None

def create_namespace(token, catalog_name, namespace_name, properties=None):
    """Create a new namespace in a catalog"""
    print(f"\nCreating namespace '{namespace_name}' in catalog '{catalog_name}'...")
    
    url = f"http://{POLARIS_HOST}/api/catalog/v1/{catalog_name}/namespaces"
    
    data = {
        "namespace": [namespace_name],
        "properties": properties or {}
    }
    
    response = requests.post(url, headers=get_headers(token), json=data)
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code in [200, 201]:
        data = response.json()
        print(f"Created namespace successfully: {data}")
        return data
    return None

def create_table(token, catalog_name, namespace_name, table_name, schema, properties=None):
    """Create a new table in a namespace"""
    print(f"\nCreating table '{table_name}' in namespace '{namespace_name}'...")
    
    url = f"http://{POLARIS_HOST}/api/catalog/v1/{catalog_name}/namespaces/{namespace_name}/tables"
    
    data = {
        "name": table_name,
        "schema": schema,
        "properties": properties or {}
    }
    
    response = requests.post(url, headers=get_headers(token), json=data)
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
    
    if response.status_code in [200, 201]:
        data = response.json()
        print(f"Created table successfully: {data}")
        return data
    return None

def get_table_metadata(token, catalog_name, namespace_name, table_name):
    """Get table metadata"""
    print(f"\nGetting metadata for table '{table_name}'...")
    
    url = f"http://{POLARIS_HOST}/api/catalog/v1/{catalog_name}/namespaces/{namespace_name}/tables/{table_name}"
    response = requests.get(url, headers=get_headers(token))
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        metadata = response.json()
        print("Current schema ID:", metadata["metadata"]["current-schema-id"])
        print("Available schemas:", len(metadata["metadata"]["schemas"]))
        
        # Print all schemas
        for i, schema in enumerate(metadata["metadata"]["schemas"]):
            print(f"\nSchema {i} (ID: {schema['schema-id']}):")
            for field in schema["fields"]:
                print(f"  - {field['name']} ({field['type']})")
        
        # Print snapshots
        snapshots = metadata["metadata"]["snapshots"]
        current_snapshot_id = metadata["metadata"]["current-snapshot-id"]
        print(f"\nCurrent snapshot ID: {current_snapshot_id}")
        print(f"Total snapshots: {len(snapshots)}")
        
        for snapshot in snapshots:
            print(f"\nSnapshot ID: {snapshot['snapshot-id']}")
            print(f"  Timestamp: {snapshot['timestamp-ms']}")
            print(f"  Operation: {snapshot.get('operation', 'N/A')}")
            print(f"  Summary: {snapshot.get('summary', {})}")
            if snapshot['snapshot-id'] == current_snapshot_id:
                print("  ^ CURRENT SNAPSHOT")
        
        return metadata
    else:
        print(f"Error: {response.text}")
    return None

def main():
    """Main function"""
    # Your catalog/namespace/table names
    catalog_name = "polaris4"
    namespace_name = "polaris4_namespace"
    table_name = "customers"
    
    try:
        # Get authentication token
        token = get_token()
        
        # Uncomment these to create resources:
        
        # # Create catalog
        # storage_config = {
        #     "storageType": "S3",
        #     "roleArn": "arn:aws:iam::123456789012:role/S3AccessRole",
        #     "region": "us-east-1"
        # }
        # create_catalog(token, catalog_name, "s3://my-data-bucket/warehouse", storage_config)
        
        # # Create namespace
        # create_namespace(token, catalog_name, namespace_name, {"owner": "admin"})
        
        # # Create table
        # schema = {
        #     "type": "struct",
        #     "schema-id": 0,
        #     "fields": [
        #         {"id": 1, "name": "id", "required": True, "type": "long"},
        #         {"id": 2, "name": "created_at", "required": True, "type": "timestamp"},
        #         {"id": 3, "name": "account_balance", "required": True, "type": "long"},
        #         {"id": 4, "name": "renewal_date", "required": True, "type": "date"}
        #     ]
        # }
        # table_properties = {
        #     "write.format.default": "parquet",
        #     "write.parquet.compression-codec": "snappy"
        # }
        # create_table(token, catalog_name, namespace_name, table_name, schema, table_properties)
        
        # List existing resources
        list_catalogs(token)
        list_namespaces(token, catalog_name)
        list_tables(token, catalog_name, namespace_name)
        get_table_metadata(token, catalog_name, namespace_name, table_name)
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
