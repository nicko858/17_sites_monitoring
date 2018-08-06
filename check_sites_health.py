import whois
import requests
from os.path import isfile
import argparse
from requests import HTTPError
from requests import ConnectionError
from datetime import datetime
from datetime import timedelta
from requests import ReadTimeout
from socket import timeout


def check_file(file_path):
    if not isfile(file_path):
        message = "'{}' is not a file or doesn't exist".format(file_path)
        raise argparse.ArgumentTypeError(message)
    return file_path


def get_args():
    script_usage = "python check_sites_health.py <path to url_list file>"
    parser = argparse.ArgumentParser(
        description="How to run check_sites_health.py:",
        usage=script_usage
    )
    parser.add_argument(
        "url_list",
        type=check_file,
        help="Specify the path to url_list file"
    )
    args = parser.parse_args()
    return args


def load_urls4check(path_to_url_list):
    with open(path_to_url_list) as file_handler:
        urls4check = file_handler.read().splitlines()
    return urls4check


def is_server_respond_ok(url):
    user_agent = {'User-agent': 'Mozilla/5.0'}
    try:
        response = requests.get(url, headers=user_agent, timeout=10)
        return response.ok
    except (ConnectionError, HTTPError, timeout, ReadTimeout):
        return False


def get_domain_expiration_date(url):
    try:
        domain_whois = whois.whois(url)
        return domain_whois.expiration_date
    except (timeout, BaseException):
        return None


def is_domain_name_payed(expiration_date, days):
    today = datetime.today()
    until_date = today + timedelta(days=days)
    if isinstance(expiration_date, list):
        return expiration_date[0] >= until_date
    return expiration_date >= until_date


def print_site_status(url, is_server_ok, is_domain_payed):
    separator = "*"*40
    print(separator)
    print("Site - {}\nServer is ok - {}\n"
          "Domain paid till next month - {}".format(
           url,
           is_server_ok,
           is_domain_payed
          ))
    print(separator)


if __name__ == "__main__":
    args = get_args()
    path_to_url_list = args.url_list
    urls4check = load_urls4check(path_to_url_list)
    for url in urls4check:
        domain_expiration_date = get_domain_expiration_date(url)
        is_server_ok = is_server_respond_ok(url)
        if not domain_expiration_date:
            is_domain_payed = False
        else:
            is_domain_payed = is_domain_name_payed(
                domain_expiration_date,
                days=31
            )
        print_site_status(url, is_server_ok, is_domain_payed)