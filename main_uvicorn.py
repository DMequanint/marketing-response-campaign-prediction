import sys
from pathlib import Path

# Add project root to sys.path so Python can find the package
PROJECT_ROOT = Path(__file__).parent.resolve()
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from marketing_campaign_response.main import app
import uvicorn

if __name__ == "__main__":
    uvicorn.run("marketing_campaing_response.main:app", host="127.0.0.1", port=8000, reload=True)

