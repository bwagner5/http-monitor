# http-monitor
An HTTP Traffic Monitor Command Line Utility


## Problem Statement

*********************************** 
HTTP log monitoring console program 
***********************************

Create a simple console program that monitors HTTP traffic on your machine:

* Consume an actively written-to w3c-formatted HTTP access log (https://en.wikipedia.org/wiki/Common_Log_Format) 
* Every 10s, display in the console the sections of the web site with the most hits (a section is defined as being what's before the second '/' in a URL. i.e. the section for "http://my.site.com/pages/create' is "http://my.site.com/pages"), as well as interesting summary statistics on the traffic as a whole. 
* Make sure a user can keep the console app running and monitor traffic on their machine 
* Whenever total traffic for the past 2 minutes exceeds a certain number on average, add a message saying that “High traffic generated an alert - hits = {value}, triggered at {time}” 
* Whenever the total traffic drops again below that value on average for the past 2 minutes, add another message detailing when the alert recovered

* Make sure all messages showing when alerting thresholds are crossed remain visible on the page for historical reasons. 
* Write a test for the alerting logic 
* Explain how you’d improve on this application design

Please submit here: https://app.greenhouse.io/tests/c56c91edafa7365224a7610e3d9ec22b


## About

This python application monitors HTTP traffic from a Commons Log Format access log. Statistics are gathered about the overall traffic, section counts, and other useful information. Alerts are also generated based off a variable threshold provided as an argument. 

## Usage

```
> ./http_monitor.py -h

  usage: http_monitor.py [-h] [-a ALERT] [-f FILE] [-w WINDOW]
                       [-t TEST_WINDOW_END]

HTTP Monitor

optional arguments:
  -h, --help            show this help message and exit
  -a ALERT, --alert ALERT
                        Alert threshold
  -f FILE, --file FILE  HTTP Access Log to read from
  -w WINDOW, --window WINDOW
                        Time window in seconds
  -t TEST_WINDOW_END, --test_window_end TEST_WINDOW_END
                        Test window upper bound in UTC for testing (ie.
                        "2017-08-24 17:55:59")
```


## Simple Test of Burst Traffic

A simple test can be ran using the provided log file `requests_at_same_time.log.txt` with the following CLI parameters:

`./http_monitor.py -t "2017-08-08 23:03:20"`

This will start the time window upper bound at 23:03:20 on August 8th 2017. The log file has 1258 requests to http://google.com/list at 2017-08-08 23:01:27. So the first window will be [23:01:20 to 23:03:20], which will alarm immediately and then exit the window with the burst of requests and recover after about 8 seconds.



