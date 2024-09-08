import requests


def fetch_user_info(msg: str) -> str:
    """
    自定义函数
    Returns:

    """
    url = 'http://127.0.0.1:5000/get_user_data'
    params = {'msg': msg}

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error: {response.status_code}")


def fetch_map_info(msg: str) -> str:
    """
    自定义函数
    Returns:

    """
    url = 'http://127.0.0.1:5000/get_map_data'
    params = {'msg': msg}

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error: {response.status_code}")