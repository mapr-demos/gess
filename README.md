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
      'lat': '36.7220096',
      'lon': '-4.4186772',
      'amount': 100, 
      'account_id': 'a335', 
      'transaction_id': '636adacc-49d2-11e3-a3d1-a820664821e3'
    }
    ...

Note 1: The average size of one transaction (interpreted as a string) 
is around 200 Bytes. This means `gess` is typically able to emit some 2MB/sec 
resulting in some 7GB/h of transaction data. 

Note 2: that in the above example,
showing a withdrawal in [Spain](https://maps.google.com/maps?q=36.7220096+-4.4186772&hl=en&sll=37.0625,-95.677068&sspn=43.037246,79.013672&t=m&z=16&iwloc=A),
the data has been re-formatted for readability reasons. In fact, each 
transaction spans a single line and is terminated by a `\n`.

Note 3: that `dummy_gess_sink.sh` both echoes the received values on screen
and logs them in a file with the name  `dummy_gess_sink.log`.

## Dependencies

* Python 2.7+
* For the data extraction part only (adding own ATM locations via OSM dumps): [imposm.parser](https://pypi.python.org/pypi/imposm.parser) which in turn depends on [ProtoBuf](https://code.google.com/p/protobuf/) installed.

## Data

### Default setting (Spanish ATM locations  )

We aim for quality synthetic data. To this end, the default data used for the
ATM locations is that of Spain obtained from the [OpenStreetMap](http://openstreetmap.org) project.
To be more precise, the default data are the [geo-coordinates](data/osm-atm-garmin.csv) 
of 822 ATMs in Spain which have been downloaded via the [POI export](http://poi-osm.tucristal.es/) service.

The withdrawal amounts are stacked (20, 50, 100, 200, 300, 400) and the rest
of the data (transaction ID/timestamp) is arbitrary. 

Note that the fraudulent transactions (consecutive withdrawals in different
location in a short time frame) will be marked in that they have a 
`transaction_id` that reads `xxx` and then the `transaction_id` of the original
transaction. This is for convenience reasons to enable a simpler 
CLI-level debugging but can otherwise be ignored.

### Extending ATM locations

If you want to add new ATM locations, then you need to do the following:

1. Choose a geographic area and download the respective `.osm` dump from sites such as [Metro Extracts](http://metro.teczno.com/).
1. Then, run `data/extract_atms.py`, which uses the ATM-tagged nodes in [OSM/XML](http://wiki.openstreetmap.org/wiki/OSM_XML) format and extracts/converts it into the [CSV format](data/osm-atm-garmin.csv) used internally, by gess.
1. Add the so generated ATM location data file in CSV format to `gess.conf` so that gess picks it up on startup time.


To give you an idea in terms of performance: on my laptop (MBP with 16 GB RAM)
it takes approximately 3 min to extract the 416 ATM locations from the 
[San Francisco Bay Area](http://osm-extracted-metros.s3.amazonaws.com/sf-bay-area.osm.bz2)
OSM file. This OSM file contains some 198,000 nodes with a raw, unzipped file size of 1.45 GB.

## Understanding the runtime statistics

In parallel to the data streaming, `gess` will output runtime statistics every
10 sec into the log file `gess.tsv` by using a TSV format that looks as 
following (slightly re-formatted for readability):

    timestamp            num_fintrans tp_fintrans num_bytes tp_bytes
    2013-12-05T16:03:17  112          11          23        2
    2013-12-05T16:03:37  110          11          22        2
    2013-12-05T16:03:47  112          11          23        2
    ...

With the following semantics for the columns:

*  `num_fintrans` … financial transactions emitted in sample interval (in thousands)
*  `tp_fintrans` … throughput of financial transactions (in thousands/second) in sample interval
*  `num_bytes` … number of bytes emitted (in MB) in sample interval
*  `tp_bytes` … throughput of bytes (in MB/sec) in sample interval

So, for example, the first non-header line states that:

* Some 112,000 financial transactions were emitted, in the sample interval ...
* ... with a throughput of 11,000 transactions per sec.
* And further, that 23MB have been emitted ... 
* ... with a throughput of 2MB/sec in the sample interval.

## License
[Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0.html).