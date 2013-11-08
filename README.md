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

    {'timestamp': '2013-11-08T10:53:03.242662', 'amount': 6071441, 'account_from': 203, 'transaction_id': 93850, 'account_to': 261}
    {'timestamp': '2013-11-08T10:53:03.242758', 'amount': 256516, 'account_from': 329, 'transaction_id': 8337, 'account_to': 605}
    {'timestamp': '2013-11-08T10:53:03.242851', 'amount': 594838, 'account_from': 138, 'transaction_id': 22413, 'account_to': 376}
    {'timestamp': '2013-11-08T10:53:03.242945', 'amount': 4540650, 'account_from': 698, 'transaction_id': 20910, 'account_to': 885}
    {'timestamp': '2013-11-08T10:53:03.243040', 'amount': 3073270, 'account_from': 534, 'transaction_id': 63642, 'account_to': 947}    ...
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