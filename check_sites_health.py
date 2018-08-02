import whois
import requests
from os.path import isfile
import argparse
from requests import HTTPError
from requests import ConnectionError
from datetime import datetime
from dateutil import relativedelta
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
        "site_list",
        type=check_file,
        help="Specify the path to url_list file"
    )
    args = parser.parse_args()
    return args


def load_urls4check(path_to_site_list):
    urls4check = []
    with open(path_to_site_list) as urls_list:
        for line in urls_list:
            urls4check.append(line.splitlines())
    return urls4check


def is_server_respond_with_200(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return True
    except (ConnectionError, HTTPError, timeout, ReadTimeout):
        return False


def get_domain_expiration_date(url):
    try:
        domain_whois = whois.whois(url)
        return domain_whois.expiration_date
    except timeout:
        return None


def is_domain_name_payed(expiration_date, months):
    today = datetime.today()
    nextmonth = today + relativedelta.relativedelta(months=months)
    if isinstance(expiration_date, list):
        return expiration_date[0] >= nextmonth
    return expiration_date >= nextmonth


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
    path_to_site_list = args.site_list
    urls4check = load_urls4check(path_to_site_list)
    for site in urls4check:
        url = "".join(site)
        domain_expiration_date = get_domain_expiration_date(url)
        is_server_ok = is_server_respond_with_200(url)
        if not domain_expiration_date:
            is_domain_payed = False
        else:
            is_domain_payed = is_domain_name_payed(
                domain_expiration_date,
                months=1
            )
            print_site_status(url, is_server_ok, is_domain_payed)