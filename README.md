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

    {'timestamp': '2013-11-07 22:35:56.993394', 'amount': 7019989, 'account_from': 350, 'transaction_id': 72378, 'account_to': 158}
    {'timestamp': '2013-11-07 22:35:56.993494', 'amount': 3227337, 'account_from': 234, 'transaction_id': 88702, 'account_to': 757}
    {'timestamp': '2013-11-07 22:35:56.993590', 'amount': 1800320, 'account_from': 427, 'transaction_id': 22251, 'account_to': 945}
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
APL2