[![Imports: isort](https://img.shields.io/badge/%20imports-isort-%231674b1?style=flat&labelColor=ef8336)](https://pycqa.github.io/isort/)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)

![Release](https://github.com/drawjk705/us-congress/workflows/Release/badge.svg)
![CI](https://github.com/drawjk705/us-congress/workflows/CI/badge.svg)

# US Congress

Client for getting information on the US Congress.

## Requirements

For this package to work, you must [get an API key from ProPublica](https://www.propublica.org/datastore/api/propublica-congress-api), whose API this uses, and set the following the environment variable `PROPUBLICA_CONG_KEY` to whatever that key is, either with

```bash
export PROPUBLICA_CONG_KEY=<your key>
```

or in a `.env` file:

```bash
PROPUBLICA_CONG_KEY=<your key>
```

## Getting started

To install with pip, simply run

```bash
pip install us_congress
```

```python
>>> from us_congress import Congress
>>> cong = getCongress(116)
>>> cong
<Congress 116>
```

This will return a client for querying data on a particular congress (in the above example, the 116th Congress).

Right now, this enables only getting lists of Representatives and Senators:

```python
cong.getRepresentatives() # DataFrame with all representatives
cong.getSenators()        # DataFrame with all senators
```
