# no_dev_fee

This is Crypto coin no dev fee tool, support eth, etc, zec, xmr protocol.
 
We use [pydivert](https://pypi.python.org/pypi/pydivert/2.0.1) capture and replace network packet  with user Crypto coin address replacing devfee address.

### usage

```bash
python no_dev_fee.py {coin_adress} {port} {worker_name.delemiter} {debug_level}

# eg:
python no_dev_fee.py 0xe9473918c1122276203677860fad70ef2b4522af 3333 . 0
```
