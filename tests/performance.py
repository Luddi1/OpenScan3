import requests
import time

# lights on
for pin in (24,):
    requests.put(f"http://127.0.0.1:8000/io/{pin}", params={"status": True})

requests.delete("http://127.0.0.1:8000/projects/openscan_test")
requests.post("http://127.0.0.1:8000/projects/openscan_test")

# Set camera values
requests.get("http://127.0.0.1:8000/cameras/0/photo")
requests.post("http://127.0.0.1:8000/cameras/0/exposure", params={"exposure_value": 45})

tic = time.perf_counter()
n = 5
m = 10
for i in range(n):
    requests.put(
        "http://127.0.0.1:8000/projects/openscan_test/focus_stack",
        params={"camera_id": 0, "focus_min": 4, "focus_max": 4+m-1},
    )

toc = time.perf_counter()
print(f"Captured {n} focus stacks with {m} focus steps in {toc - tic:0.4f} s.")

# lights off
for pin in (24,):
    requests.put(f"http://127.0.0.1:8000/io/{pin}", params={"status": False})
