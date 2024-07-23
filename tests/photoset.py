import requests
import time

# lights on
for pin in (24,):
    requests.put(f"http://127.0.0.1:8000/io/{pin}", params={"status": True})

requests.delete("http://127.0.0.1:8000/projects/openscan_test")
requests.post("http://127.0.0.1:8000/projects/openscan_test")

# Set camera values
requests.post("http://127.0.0.1:8000/cameras/0/exposure", params={"exposure_value": 45})

# rotor has to stand level, in middle of range
for i in (60, -20, -20, -20, -20, -20, -20):
    requests.post("http://127.0.0.1:8000/motors/rotor/move", params={"degrees": i})
    for j in range(0, 360, 30):
        requests.post("http://127.0.0.1:8000/motors/turntable/move", params={"degrees": 30})
        time.sleep(0.5)
        print("Moved to {0}, {1}".format(i, j))
        requests.put(
            "http://127.0.0.1:8000/projects/openscan_test/photo_stack",
            params={"camera_id": 0, "focus_min": 6, "focus_max": 13},
        )

requests.post("http://127.0.0.1:8000/motors/rotor/move", params={"degrees": 60})

# lights off
for pin in (24,):
    requests.put(f"http://127.0.0.1:8000/io/{pin}", params={"status": False})
