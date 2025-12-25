
        
        
# model_loader.py

import time
import requests
from config import MODEL_NAME, OLLAMA_URL


def wait_for_model_ready(timeout=600, update_interval=5):
    start_time = time.time()
    last_update = 0

    print("🔄 Loading model into memory (this may take a while)...")

    while True:
        elapsed = int(time.time() - start_time)

        if elapsed > timeout:
            raise RuntimeError("❌ Model failed to load within timeout.")

        if elapsed - last_update >= update_interval:
            print(f"⏳ Still loading... elapsed time: {elapsed}s")
            last_update = elapsed

        try:
            response = requests.post(
                OLLAMA_URL,
                json={
                    "model": MODEL_NAME,
                    "prompt": "Initialization check.",
                    "stream": False,
                    "keep_alive": "30m",
                    "options": {"num_predict": 1},
                },
                timeout=120,
            )

            if response.status_code == 200:
                print(f"✅ Model loaded successfully in {elapsed}s.")
                return True

        except Exception:
            pass

        time.sleep(1)

