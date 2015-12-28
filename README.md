## Overview
Work in progress fork of ColdSauce's repo.  Will currently only get one page of search results.

## Setting Up
Start by installing the dependencies by running the command `pip install -r requirements` in the root folder.  
Note that you must be running Python 2.7.9 and pip.  Running versions lower than 2.7.9 will result in warnings.

## Using
To use, run `download_subreddit.py`

### options
`-s`, `--start` specify the time to start searching in a `mm/dd/yy` format.  Defaults to `01/01/00`

`-e`, `--end`  specify the time to stop searching in a `mm/dd/yy` format.  Defaults to current date

`-r`, `--reddit` specify the subreddit to search, e.g. `gabe_k`.  Defaults to `all`

## License
Licensed under MIT. Please check out LICENSE for more info.
