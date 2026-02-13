# model_api_helper.py
# Wrapper for accessing AI model metadata APIs
import requests
from typing import Optional

# Note: Current implementation uses AI model platform (civitai.com) as the API provider
API_MODEL_URL = "https://api.civitai.com/v1/models/{}"
API_TIMEOUT = 30


def get_model_metadata(model_id: int) -> dict:
    """
    Ruft Modell-Metadaten vom API ab.
    
    Returns:
        Dict with keys: name, image, versions (list), full_data (dict)
    
    Raises:
        RuntimeError: On API error
    """
    try:
        r = requests.get(API_MODEL_URL.format(model_id), timeout=API_TIMEOUT)
        r.raise_for_status()
        data = r.json()
        
        versions = [
            v.get("name", "")
            for v in data.get("modelVersions", [])
            if v.get("name")
        ]
        
        return {
            "name": data.get("name", ""),
            "image": data.get("image", ""),
            "type": data.get("type", ""),
            "baseModel": data.get("baseModel", ""),
            "description": data.get("description", ""),
            "versions": versions,
            "modelVersions": data.get("modelVersions", []),
            "full_data": data
        }
    except requests.exceptions.Timeout:
        raise RuntimeError(f"API Timeout beim Abrufen von Model {model_id}")
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"API error: {e}")
    except Exception as e:
        raise RuntimeError(f"Error fetching model metadata: {e}")


def get_model_versions(model_id: int) -> list[str]:
    """
    Returns the names of all versions of a model.
    (Wrapper for backward compatibility)
    """
    metadata = get_model_metadata(model_id)
    return metadata["versions"]

