# afb-notifier

Repo for Code@LTH's intro lecture and code along: https://docs.google.com/presentation/d/1rV5IPzBiFoe-DPaGTZztfFuZ4lO70y6T5YRnIyjii4k/edit?usp=sharing




Supervise AFBostäder programmatically to find your dream student housing.

### Setup

* Install Python

Then in the terminal run:

```
$ pip3 install virtualenv
$ virtualvenv venv
$ ./venv/bin/activate
(venv) $ pip3 install -r requirements.txt
```

If you are on Windows I suggest setting up Linux-subsystem. Then check this for the cronjob: https://scottiestech.info/2018/08/07/run-cron-jobs-in-windows-subsystem-for-linux/


### Run

```
(venv) $ python3 -i notifier.py # interpreter for development and debugging
(venv) $ python3 notifier.py    # run script
```

### Setup mailer

1. Go to: https://console.cloud.google.com/
2. Go to "Marketplace"
3. Search for "GMail API"
4. Enable "GMail API"
5. Go to "Gmail API" -> "Credentials"
6. Create a "OAuth Client ID" credential, make sure to select "Desktop App"
8. Download the credential and save in the project directory, for example as "credentials.json".

### Setup cron-job

1. Modify `run.sh` to include your path, hint use `pwd` in the terminal.
2. Run `crontab -e` and paste the following in, again with correct path:

```
*/30 * * * * <your_path>/run.sh > /tmp/afb-notifier-log.txt 2> /tmp/afb-notifier-errors.txt
```

### Links

* Intro to Python 1: https://learnxinyminutes.com/docs/python/
* Intro to Python 2: https://erik.bjareholt.com/python-talk-slides/#1
* Use the GMail API: https://blog.macuyiko.com/post/2016/how-to-send-html-mails-with-oauth2-and-gmail-in-python.html
* Help making cron jobs: https://crontab.guru/
* The Python Paradox: http://www.paulgraham.com/pypar.html
* Free VPS credits and more: https://education.github.com/pack
