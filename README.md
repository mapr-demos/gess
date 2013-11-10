# gess

A _ge_nerator for _s_ynthetic _s_treams of financial transactions (ATM withdrawals).

## Usage

First, start `gess` like so:

    $ ./gess.sh start 
  
Then, check if `gess` is working fine:

    $ ./dummy_gess_sink.sh


Once active, `gess` will stream synthetic data about ATM withdrawals, 
in a line-oriented, JSON-formatted fashion on default port `6900` via UDP 
(which you can observe as the output of `dummy_gess_sink.sh`):

    ...
    {
      'timestamp': '2013-11-08T10:58:19.668225', 
      'lat': '37,3896661',
      'lon': '-5.9742199',
      'amount': 100, 
      'account_id': 'a335', 
      'transaction_id': '636adacc-49d2-11e3-a3d1-a820664821e3'
    }
    ...

Note that in the above example,
showing a withdrawal in [Spain](https://www.google.com/maps/preview#!q=37%C2%B0+39.850'%2C+-5%C2%B0+58.477'),
the data has been re-formatted for readability reasons. In fact, each 
transaction spans a single line and is terminated by a `\n`.

## Data

We aim for quality synthetic data. To this end, we have obtained the geolocation
of ATMs in Europe, serving as the basis for the withdrawals, from the 
[OpenStreetMap](http://openstreetmap.org) project. 

To be more precise, we have extracted the 
[geo-coordinates](data/osm-atm-garmin.csv) of 822 ATMs via
[POI export](http://poi-osm.tucristal.es/) for the following countries:

* Spain
* France
* Portugal
* Belgium
* Switzerland
* Germany
* Italy

The withdrawal amounts are stacked (20, 50, 100, 200, 300, 400) and the rest
of the data is random. 

Note that the fraudulent transactions (consecutive withdrawals in different
location in a short time frame) will be marked in that they have a 
`transaction_id` that starts with `xxx`. This is for convinience reasons to
enable a simpler CLI-level debugging but can otherwise be ignored.


## Understanding the runtime statistics

In parallel to the data streaming, `gess` will output runtime statistics into
the log file `gess.log`, using a TSV format that looks like following (slightly
re-formatted for readability):

    sample_interval num_fintrans  tp_fintrans num_bytes tp_bytes
    10	            77828         7           16        1642
    10	            78547         7           16        1657
    10	            72895         7           15        1537
    10	            69906         6           14        1474
    10	            69748         6           14        1471
    10	            70618         7           14        1489
    ...

With the following semantics for the columns:

* `sample_interval` … the sample interval (in seconds)
*  `num_fintrans` … financial transactions emitted in sample interval 
*  `tp_fintrans` … throughput of financial transactions (in thousands/second) in sample interval
*  `num_bytes` … number of bytes emitted (in MB) in sample interval
*  `tp_bytes` … throughput of bytes (in kB/sec) in sample interval

So, for example, the first non-header line states that:

* in the sample interval of 10 sec, 
* 77,828 financial transactions were emitted,
* with a throughput of  7000 transactions per sec,
* and further, that 16MB have been emitted, 
* with a throughput of 1642kB per second.

Note: in terms of throughput, a single `gess` instance should be able to produce
some 5GB of transaction data, per hour.

## To Do

* Implement multi-gess through [threading](http://stackoverflow.com/questions/2846653/python-multithreading-for-dummies) over range of ports 
* Implement throttling (2x, 5x, 10x)

## License
[Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0.html).