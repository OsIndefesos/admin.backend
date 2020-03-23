import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    adotantes_table    = dynamodb.Table('Indefesos.Adotantes')
    adocoes_table      = dynamodb.Table('Indefesos.Adocoes')

    adopter_doc_number = event['pathParameters']['docnumber']

    # fetch from the database
    adopter_result = adotantes_table.get_item(
        Key={
            'DocNumber': adopter_doc_number
        }
    )
    
    if(adopter_result == None or 'Item' not in adopter_result):
        return {
            "statusCode" : 404,
            "body"       : "Adopter not found!"
        }
    
    adopter          = adopter_result['Item']
    
    fe               = Attr('AdopterDocNumber').eq(adopter_doc_number)
    adoptions_result = adocoes_table.scan(FilterExpression=fe)

    if (adoptions_result == None or 'Items' not in adoptions_result):
        return {
            "statusCode" : 500,
            "body"       : "Couldn't find any adoptions!"
        }
        
    adopter["Adoptions"] = adoptions_result['Items']

    # create a response
    return {
        "statusCode": 200,
        "body": json.dumps(adopter)
    }
