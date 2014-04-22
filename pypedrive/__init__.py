import logging
from urlparse import urljoin
import requests

__author__ = 'gautam'

BASE_URL = "http://api.pipedrive.com/v1/"

logging.basicConfig(level=logging.INFO)


class ResponseError(Exception):
    pass


def add_base_info(fn):
    def wrapper_method(self, url, params=None, **kwargs):
        if not params: params = {}
        params["api_token"] = self.api_token
        final_url = urljoin(self.base_url, url)
        logging.info(final_url)
        return fn(self, final_url, params, **kwargs)

    return wrapper_method


def jsonify(fn):
    def wrapper(*args, **kwargs):
        result = fn(*args, **kwargs)
        json = result.json()
        if result.status_code not in [200, 201] or not json.get("success"):
            raise ResponseError(json.get("error", "Unknown Error"))
        return json["data"]

    return wrapper


class Pypedrive:
    def __init__(self, api_token, base_url=BASE_URL):
        self.api_token = api_token
        self.base_url = base_url


    @jsonify
    @add_base_info
    def get(self, url, params):
        return requests.get(url, params=params)

    @jsonify
    @add_base_info
    def post(self, url, params, data=None):
        return requests.post(url, params=params, data=data)

    @jsonify
    @add_base_info
    def put(self, url, params,data=None):
        return requests.put(url, params=params,data=data)

    @jsonify
    @add_base_info
    def delete(self, url, params):
        return requests.delete(url, params=params)


class Deals(Pypedrive):
    def deals(self, id=None):
        return self.get("deals") if not id else self.get("deals/{}".format(id))

    def update_deals(self,id,params):
        return self.put("deals/{}".format(id),data=params)