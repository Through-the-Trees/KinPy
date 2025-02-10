# KinPy
A python package for managing a kintone database using the kintone REST API.


## Installation (TODO, For reference only)
```bash
pip install kinpy
```

## Usage (TODO, For reference only)

### Initialize Connection
```python
>>> from kinpy import Kintone, KintoneAuth
...
>>> auth = KintoneAuth('your_domain', 'your_app_id', 'your_api_token')
>>> kintone = Kintone(auth)
```
### Get Apps
```python
>>> Kintone.apps
[App('appId'= '1', 'code'= 'app_code', 'name'= 'app_name', ...), ...]
```

### Get Records
```python
>>> app = kintone.apps['app_code']
>>> app.records
[Record('recordId'= '1', 'record'= {'field_code': {'value': 'value'}, ...}), ...]
```

## License
[GPLv3](LICENSE)


## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.