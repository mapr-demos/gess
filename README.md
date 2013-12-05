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

Further note that `dummy_gess_sink.sh` both echoes the received values on screen
and logs them in a file with the name  `dummy_gess_sink.log`.

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
`transaction_id` that reads `xxx` and then the `transaction_id` of the original
transaction. This is for convenience reasons to enable a simpler 
CLI-level debugging but can otherwise be ignored.


## Understanding the runtime statistics

In parallel to the data streaming, `gess` will output runtime statistics every
5sec into the log file `gess.tsv`. I'm using a TSV format that looks like 
following (slightly re-formatted for readability):

    timestamp            num_fintrans tp_fintrans num_bytes tp_bytes
    2013-12-05T16:03:17  57           11          11        2
    2013-12-05T16:03:22  58           11          12        2
    2013-12-05T16:03:27  57           11          11        2
    ...

With the following semantics for the columns:

*  `num_fintrans` … financial transactions emitted in sample interval (in thousands)
*  `tp_fintrans` … throughput of financial transactions (in thousands/second) in sample interval
*  `num_bytes` … number of bytes emitted (in MB) in sample interval
*  `tp_bytes` … throughput of bytes (in MB/sec) in sample interval

So, for example, the first non-header line states that:

* Some 57,000 financial transactions were emitted, in the sample interval ...
* ... with a throughput of 11,000 transactions per sec.
* And further, that 11MB have been emitted ... 
* ... with a throughput of 2MB/sec in the sample interval.

Note: in terms of throughput, a single `gess` instance should be able to produce
some 4-5GB of transaction data, per hour.

## License
[Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0.html).