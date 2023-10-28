import boto3
from boto3.dynamodb.types import TypeSerializer, TypeDeserializer


class ddbTable:

    def __init__(self, table_name, **kwargs):
        self.session = boto3.Session(**kwargs)
        self.resource = self.session.resource('dynamodb')
        self.table = self.resource.Table(TableName=table_name)
        return self
        
        
    # Redundant due to using dynamodb resource rather than client
    def _convert_python_to_ddb_obj(obj: dict) -> dict:
        serializer = TypeSerializer()
        return {
            k: serializer.serialize(v) for k, v in obj.items()
        }
        
    # Redundant due to using dynamodb resource rather than client
    def _convert_ddb_to_python_obj(obj:dict) -> dict:
        deserializer = TypeDeserializer()
        return {
            k: deserializer.deserialize(v) for k, v in obj.items()
        }
    
    # Might have to rename this function in the future to match Django's ORM
    def save(self, payload:dict, **kwargs):
        return self.table.put_item(
            Items=payload
        )
        
    # Might have to rename this function in the future to match Django's ORM
    def get(self, payload:dict, **kwargs):
        values = {f':{k}': v for k, v in payload.items()}
        expression = ' AND '.join(map(lambda x: f'{x} = :{x}', payload.keys()))
        return self.table.query(
            ExpressionAttributeValues=values,
            KeyConditionExpression=expression
        )
        
        
        