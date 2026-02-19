from datetime import datetime, timezone
import uuid

from app.model_loader import get_model_version

def build_audit_block():
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "model_version": get_model_version(),
        "request_id": str(uuid.uuid4()),
        "api_version": "1.0.0"
    }