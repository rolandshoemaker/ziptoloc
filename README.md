ziptoloc
========

ziptoloc is the underlying infrastructure that runs [www.ziptoloc.net](http://www.ziptoloc.net), a service that provides a simple way to get a [LOC](http://en.wikipedia.org/wiki/LOC_record) DNS record from a United States Zip Code.

Using the service
-----------------

    [rolands@kamaji:~]$ dig +noall +answer loc 97402.ziptoloc.net
    97402.ziptoloc.net.	86400	IN	LOC	44 2 24.000 N 123 13 12.000 W 0.00m 0.00m 0.00m 0.00m
    
    [rolands@kamaji:~]$ dig +noall +answer loc 10200.ziptoloc.net
    10200.ziptoloc.net.	86400	IN	LOC	40 46 12.000 N 73 57 0.000 E 0.00m 0.00m 0.00m 0.00m
    
    [rolands@kamaji:~]$ dig +noall +answer loc 51630.ziptoloc.net
    51630.ziptoloc.net.	86400	IN	LOC	40 34 48.000 N 95 13 12.000 W 0.00m 0.00m 0.00m 0.00m
