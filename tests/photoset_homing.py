import requests
import time

# lights on
for pin in (24,):
    requests.put(f"http://127.0.0.1:8000/io/{pin}", params={"status": True})

requests.delete("http://127.0.0.1:8000/projects/openscan_test")
requests.post("http://127.0.0.1:8000/projects/openscan_test")

requests.post("http://piscan3d:8000/motors/rotor/home")

# Set camera values
requests.get("http://127.0.0.1:8000/cameras/0/photo")
requests.post("http://127.0.0.1:8000/cameras/0/exposure", params={"exposure_value": 85})

# Run through absolute values and take focus stacks
for i in range(55, -90, -10):
    requests.post("http://127.0.0.1:8000/motors/rotor/move_to", params={"degrees": i})
    time.sleep(0.5)
    for j in range(0, 360, 15):
        requests.post("http://127.0.0.1:8000/motors/turntable/move_to", params={"degrees": j})
        time.sleep(0.5)
        print("Moved to {0}, {1}".format(i, j))
        requests.put(
            "http://127.0.0.1:8000/projects/openscan_test/focus_stack",
            params={"camera_id": 0, "focus_min": 7, "focus_max": 12},
        )

requests.post("http://127.0.0.1:8000/motors/rotor/move", params={"degrees": 60})

# lights off
for pin in (24,):
    requests.put(f"http://127.0.0.1:8000/io/{pin}", params={"status": False})
