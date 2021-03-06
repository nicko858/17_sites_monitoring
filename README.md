# Sites Monitoring Utility
The program checks sites health. At the input - a text file with URLs for verification. At the output, the status of each site, based on the following checks:
- the server responds to the request with the status of HTTP 200;
- the domain name of the site is paid for at least 1 month in advance.

# How in works


- The program reads a text file with URLs  
- Reads content line by line
- For every url checks server HTTP-status, domain name of the site is paid
- Prints result check to the console output 

# How to Install
First, you should make a text file with URLs in such format:
```http://youtube.com
http://facebook.com
http://baidu.com
http://wikipedia.org
http://reddit.com
http://yahoo.com
https://www.kinopoisk.ru/top/lists/
https://coderoncode.com/tools/2017/04/16/vim-the-perfect-ide.html
```

Python 3 should be already installed. Then use pip (or pip3 if there is a conflict with old Python 2 setup) to install dependencies:

```bash
pip install -r requirements.txt # alternatively try pip3
```

Remember, it is recommended to use [virtualenv/venv](https://devman.org/encyclopedia/pip/pip_virtualenv/) for better isolation.


# How to run
- Activate virtualenv
``` bash
source <path_to_virtualenv>/bin/activate
```
- Run script with virtualenv-interpreter
```bash
<path_to_virtualenv>/bin/python3.5 check_sites_health.py site_list.txt
```
If everything is fine, you'll see such output:
```text
****************************************
Site - https://www.kinopoisk.ru/top/lists/
Server is ok - True
Domain paid till next month - True
****************************************
****************************************
Site - https://coderoncode.com/tools/2017/04/16/vim-the-perfect-ide.html
Server is ok - True
Domain paid till next month - False
****************************************
****************************************
Site - http://youtube.com
Server is ok - True
Domain payed till next month - True
****************************************
****************************************
Site - http://facebook.com
Server is ok - False
Domain payed till next month - True
****************************************
****************************************
Site - http://baidu.com
Server is ok - True
Domain payed till next month - False
****************************************
```


# Project Goals

The code is written for educational purposes. Training course for web-developers - [DEVMAN.org](https://devman.org)
