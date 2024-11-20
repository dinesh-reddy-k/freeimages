import os
import requests

def download_image(url: str):
    folder_path = 'output'
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an error if the request failed
        filename = url.split("/")[-1].split("?")[0]
        full_path = os.path.join(folder_path, filename)
        os.makedirs(folder_path, exist_ok=True)
        with open(full_path, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)
    except requests.exceptions.RequestException as e:
        print(filename)

# testing
# download_image("https://img.freepik.com/premium-photo/cheerful-confident-happy-smiling-girl-have-everything-control-assuring-all-okay-show-ok-excellent-gesture-give-approval-accepting-like-awesome-product-recommend-something_176420-50953.jpg?uid=P172620103&ga=GA1.1.1069123660.1727916211&semt=ais_hybrid", "output")
