from typing import Any
from dataclasses import dataclass

import json

import urllib3
from urllib3 import BaseHTTPResponse

http = urllib3.PoolManager()

@dataclass
class App:

    url: str
    api_token: str
    app_id: int

    def __repr__(self):
        return f"<Kintone App ID {self.app_id}>"

    """Runs multiple get requests to get more than 500 records (limeted to 500 per request)"""
    def get_records(self, fields: list[str], query: str='', _last_record_id: int = None) -> list[ dict[str, Any ] ]:

        chunk_size = 500

        # Recursive query that adds to itself each iteration of this function
        bulk_query = f'$id > {_last_record_id}' if _last_record_id else ''
        query = f'({query}) and ' + bulk_query if query and bulk_query else query + bulk_query

        response: BaseHTTPResponse = http.request(
            "GET", self.url + "records.json",
            headers={"X-Cybozu-API-Token": self.api_token},
            fields= \
            {
                "app": self.app_id,
                "fields": ','.join(fields+['$id']),
                "query": query + f' order by $id asc limit {chunk_size}',
                "totalCount": True
            }
        )

        # Convert JSON to python objects
        response_dict = json.loads( response.data.decode('utf-8') )


        print(response_dict)
        # Return none if no records found
        if 'records' not in response_dict:
            return None
        
        # Get records from HTTP response
        records: list[ dict[ str, dict[str, Any] ] ] = response_dict['records']

        # Convert records to less convoluted data structure
        records: list[ dict[str, Any] ] = \
        [
            {
                key: value['value']
                for key, value in record.items()
            }
            for record in records
        ]

        total_count = int(response_dict['totalCount'])
        if total_count > chunk_size:
            last_record_id = max(int(record['$id']) for record in records)
            return records + self.get_records(fields, query, last_record_id)
        else:
            return records
        
    """Intended to update one field value of one record, returns false unless only one record is found"""
    def update_record(self, query: str, field: str, new_value: Any) -> bool:

        records_to_update: list[ dict[str, Any] ] = self.get_records([field], query)

        if not records_to_update or len(records_to_update) != 1:
            return False

        update_ids: list[str] = \
        [
            record['$id']
            for record in records_to_update
            if record[field] != new_value
        ]

        record_updates: list[ dict[str, dict[str, Any] ] ] = \
        [
            {
                'id': id,
                'record': {field: {'value': new_value}}
            }
            for id in update_ids
        ]

        update_count = 0

        payload = \
        {
            "app": self.app_id,
            "records": record_updates
        }

        response: BaseHTTPResponse = http.request \
        (
            "PUT", self.url + "records.json",
            headers={"X-Cybozu-API-Token": self.api_token,
                "Content-Type": "application/json"},
            body=json.dumps(payload).encode('utf-8')
        )
        response_dict = json.loads( response.data.decode('utf-8') )
    
        if 'records' in response_dict:
            update_count += len(response_dict['records'])
        else:
            print(response.data)
            print('No records updated!')
            return False
        
        if update_count < 1:
            return False

        print('Record updated')
        return True

    """Updates one field to a specified value for all records that match the given query"""
    def update_records(self, field: str, new_value: Any, query: str='', _last_record_id: int = None) -> bool:

        records_to_update: list[ dict[str, dict[str, Any] ] ] = self.get_records([field], query)

        if not records_to_update:
            print('No records match query!')
            return False

        update_ids: list[str] = \
        [
            record['$id']['value']
            for record in records_to_update
            if record[field]['value'] != new_value
        ]

        record_updates: list[ dict[str, dict[str, Any] ] ] = \
        [
            {
                'id': id,
                'record': {field: {'value': new_value}}
            }
            for id in update_ids
        ]

        bulk_query = f'$id > {_last_record_id}' if _last_record_id else ''
        query = f'({query}) and ' + bulk_query if query and bulk_query else query + bulk_query

        chunk_size = 100
        update_count = 0
        for i in range(0, len(record_updates), chunk_size):
            chunk = record_updates[i:i+chunk_size]

            payload = \
            {
                "app": self.app_id,
                "records": chunk
            }

            response: BaseHTTPResponse = http.request \
            (
                "PUT", self.url + "records.json",
                headers={"X-Cybozu-API-Token": self.api_token,
                    "Content-Type": "application/json"},
                body=json.dumps(payload).encode('utf-8')
            )
            response_dict = json.loads( response.data.decode('utf-8') )
        
            if 'records' in response_dict:
                update_count += len(response_dict['records'])
            else:
                print(response.data)
                print('No records updated!')
                return False
        print(f'{update_count} records updated')
        return True