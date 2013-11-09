# gess

A _ge_nerator for _s_ynthetic _s_treams of financial transactions.

## Usage

First, start `gess` like so:

    $ ./gess.sh start 
  
Then, check if `gess` is working fine:

    $ ./dummy_gess_sink.sh


Once active, `gess` will stream financial transactions in a line-oriented,
JSON-formatted fashion on default port `6900` via UDP 
(which you can observe as the output of `dummy_gess_sink.sh`):

    {'timestamp': '2013-11-08T10:58:19.668225', 'amount': 1315372, 'account_from': 335, 'transaction_id': '0888199f-b65c-49b8-a816-719b90308c62', 'account_to': 979}
    {'timestamp': '2013-11-08T10:58:19.668396', 'amount': 7141834, 'account_from': 84, 'transaction_id': '8102c772-48e9-4a2f-9b0a-7ab78d8875c0', 'account_to': 218}
    {'timestamp': '2013-11-08T10:58:19.668565', 'amount': 7609895, 'account_from': 259, 'transaction_id': '5ca91f40-3714-41b3-bdc2-4bb528c196ec', 'account_to': 926}
    {'timestamp': '2013-11-08T10:58:19.668733', 'amount': 3258696, 'account_from': 1, 'transaction_id': '82e130c0-57c9-44d4-8575-d7cc620ccd41', 'account_to': 280}
    {'timestamp': '2013-11-08T10:58:19.668900', 'amount': 5678310, 'account_from': 524, 'transaction_id': 'd3355a52-2c56-4855-9499-81ff4a67eb1e', 'account_to': 588}
    ...
    
## Understanding the runtime statistics

In parallel to the data streaming, `gess` will output runtime statistics into
the log file `gess.log`, using a TSV format that looks like following:

    sample_interval	num_fintrans	tp_fintrans	num_bytes	tp_bytes
    5	89835	17	14	2869
    5	92572	18	14	2957
    5	91259	18	14	2915
    5	91980	18	14	2938
    5	92069	18	14	2941
    ...

With the following semantics for the columns:

* `sample_interval` … the sample interval (in seconds)
*  `num_fintrans` … financial transactions emitted in sample interval 
*  `tp_fintrans` … throughput of financial transactions (in thousands/second) in sample interval
*  `num_bytes` … number of bytes emitted (in MB) in sample interval
*  `tp_bytes` … throughput of bytes (in kB/sec) in sample interval

So, for example, the first non-header line states that:

* in the sample interval of 5 sec
* 89,835 financial transactions were emitted
* with a throughput of  17 thousand transactions per sec
* and further 14MB have been emitted 
* with a throughput of 2869kB per second.


## To Do

* Implement multi-gess (launch X instances of gess-main in range of ports) 
* Implement throttling

## Architecture
TBD.

## License
[Apache License, Version 2.0](http://www.apache.org/licenses/LICENSE-2.0.html).