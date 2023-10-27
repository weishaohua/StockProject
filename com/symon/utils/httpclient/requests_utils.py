import requests


def get(url, params=None, headers=None, timeout=None):
    """
    get请求

    :param url: url
    :param params: 参数
    :param headers: 请求头信息
    :param timeout: 超时时间，单位秒
    :return: 返回内容
    """
    session = requests.Session()
    try:
        response = session.get(url, params=params, headers=headers, timeout=timeout)
        if response.status_code == 200:
            return response.text
        else:
            raise Exception(f"请求url: {url} 返回失败status_code: {response.status_code}")
    except requests.RequestException as e:
        print(f"请求url: {url} 发生了异常:", str(e))
        raise
    finally:
        session.close()


def post(url, data=None, headers=None, timeout=None):
    """
    post请求

    :param url: url
    :param data: 请求数据
    :param headers: 请求头信息
    :param timeout: 超时时间，单位秒
    :return: 返回内容
    """
    session = requests.Session()
    try:
        response = session.post(url, data=data, headers=headers, timeout=timeout)
        if response.status_code == 200:
            return response.text
        else:
            raise Exception(f"请求url: {url} 返回失败status_code: {response.status_code}")
    except requests.RequestException as e:
        print(f"请求url: {url} 发生了异常:", str(e))
        raise
    finally:
        session.close()

