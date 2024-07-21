import requests
import time

# lights on
for pin in (24,):
    requests.put(f"http://127.0.0.1:8000/io/{pin}", params={"status": True})

requests.delete("http://127.0.0.1:8000/projects/openscan_test")
requests.post("http://127.0.0.1:8000/projects/openscan_test")

# Set camera values
requests.post("http://127.0.0.1:8000/cameras/0/exposure", params={"exposure_value": 45})

for i in (10, -10, -10):
    requests.post("http://127.0.0.1:8000/motors/rotor/move", params={"degrees": i})
    for _ in range(0, 360, 20):
        requests.post("http://127.0.0.1:8000/motors/turntable/move", params={"degrees": 20})
        time.sleep(0.5)
        requests.put(
            "http://127.0.0.1:8000/projects/openscan_test/photo_stack",
            params={"camera_id": 0, "focus_min": 6, "focus_max": 13},
        )

requests.post("http://127.0.0.1:8000/motors/rotor/move", params={"degrees": 10})


# lights off
for pin in (24,):
    requests.put(f"http://127.0.0.1:8000/io/{pin}", params={"status": False})
