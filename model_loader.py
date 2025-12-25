# model_loader.py
# REAL model warm-up (forces full load)

import time
import requests
from config import MODEL_NAME, OLLAMA_URL


def wait_for_model_ready(timeout=600, update_interval=5):
    start_time = time.time()
    last_update = 0

    print("🔄 Warming up model (forcing full load)...")

    while True:
        elapsed = int(time.time() - start_time)

        if elapsed > timeout:
            raise RuntimeError("❌ Model failed to warm up within timeout.")

        if elapsed - last_update >= update_interval:
            print(f"⏳ Warming up... elapsed time: {elapsed}s")
            last_update = elapsed

        try:
            # 🔥 REAL inference, not a ping
            response = requests.post(
                OLLAMA_URL,
                json={
                    "model": MODEL_NAME,
                    "prompt": (
                        "This is a warm-up request. "
                        "Generate a short acknowledgement sentence."
                    ),
                    "stream": False,
                    "keep_alive": "30m",
                    "options": {
                        "num_predict": 50,      # 🔑 forces real generation
                        "temperature": 0.0
                    },
                },
                timeout=300,
            )

            if response.status_code == 200:
                print(f"✅ Model fully warmed in {elapsed}s.")
                return True

        except Exception:
            pass

        time.sleep(1)