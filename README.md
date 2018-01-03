***A crawler-based search engine using improved Pagerank Algorithm***
------
Tech Stack: Python 2.7, MongoDB, Javascript, HTML, CSS, Bootstrap CSS, AWS, JQuery  

Important libraries used: Beautifulsoup(web cralwer),   Bottle(server), Beaker(AWS deployment)

_To run the search engine:_
1) run the crawler to load the data.
i) start your mongoDB server using this command "sudo mongod".
ii) run your crawler "python crawler.py".
2) run the search engine "python fronend.py".
*Note*: please check the console log to see what the url is.

_To run the one click deployment script:_
1) put your AWS credential.csv file in the project directory.
2) choose names for your key pair and security group by assigning names to key_pair_name and sec_group_name.
3) run the script by "python one_click_deploy.py"

*Note*: the instance url and port number will be displayed shortly in the console, then the console will show environment setup logs.

*Note*: the ip and port is shown at the top of the console when running the script. The default port is 8085.

*NOTE*: PLEASE BE PATIENT WHEN RUNING THE ONE CLICK DEPLOYMENT, IT MIGHT TAKE AROUND 10 MINS DUE TO INSTALLING 
                NUMPY PACKAGE IS REALLY REALLY TIME CONSUMMING!!!

Benchmark Result:

[ec2-user@ip-172-31-86-242 ~]$ ab -n 1000 -c 45 http://ec2-34-227-172-22.compute-1.amazonaws.com/?keywords=helloworld+foo+bar

This is ApacheBench, Version 2.3

Server Software:        WSGIServer/0.1
Server Hostname:        ec2-34-227-172-22.compute-1.amazonaws.com
Server Port:            80

Document Path:          /?keywords=helloworld+foo+bar
Document Length:        0 bytes

Concurrency Level:      45
Time taken for tests:   6.642 seconds
Complete requests:      1000
Failed requests:        0
Write errors:           0
Non-2xx responses:      1000
Total transferred:      359000 bytes
HTML transferred:       0 bytes
Requests per second:    150.56 [#/sec] (mean)
Time per request:       298.875 [ms] (mean)
Time per request:       6.642 [ms] (mean, across all concurrent requests)
Transfer rate:          52.79 [Kbytes/sec] received

Connection Times (ms)
min  mean[+/-sd] median   max
Connect:        0    6  71.8      0    1024
Processing:     1   84 516.7      6    6639
Waiting:        1   84 516.7      6    6639
Total:          4   89 521.0      6    6641

Percentage of the requests served within a certain time (ms)
50%      6
66%      6
75%      6
80%      6
90%      6
95%     15
98%   1653
99%   3344
100%   6641 (longest request)
