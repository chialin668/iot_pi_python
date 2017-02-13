https://www.hackster.io/bees/aws-iot-and-beehives-c59fff
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
--
-- create DynamoDB table
--
aws dynamodb create-table \
	--table-name iot1 \
	--attribute-definitions \
			AttributeName=SerialNumber,AttributeType=S \
			AttributeName=Timestamp,AttributeType=S  \
	--key-schema \
			AttributeName=SerialNumber,KeyType=HASH \
			AttributeName=Timestamp,KeyType=RANGE \
	--provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1

	"arn:aws:dynamodb:us-west-2:123275298972:table/iot1"
    "arn:aws:dynamodb:us-west-2:123275298972:table/iot1"


-- create role 
cat > iot1-role.txt
{  
  "Version":"2012-10-17",
  "Statement":[  
    {  
      "Sid":"",
      "Effect":"Allow",
      "Principal":{  
        "Service":"iot.amazonaws.com"
      },
      "Action":"sts:AssumeRole"
    }
  ]
}

aws iam create-role --role-name "iot1-role" --assume-role-policy-document file://iot1-role.txt
	"arn:aws:iam::123275298972:role/iot1-role"

-- create policy (for accessing dynamoDB)
cat > iot1-policy.txt
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "dynamodb:*"
            ],
            "Resource": [
                "arn:aws:dynamodb:us-west-2:123275298972:table/iot1"
            ]
        }
    ]
}

aws iam create-policy --policy-name "iot1-policy" --policy-document file://iot1-policy.txt
	"arn:aws:iam::123275298972:policy/iot1-policy"

-- attach policy to role
aws iam attach-role-policy --role-name "iot1-role" --policy-arn "arn:aws:iam::123275298972:policy/iot1-policy"

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
--
-- basic rule
--
cat > iot1-rule.txt
{  
  "sql":"SELECT * FROM 'topic/iot1/data'",
  "ruleDisabled":false,
  "actions":[  
    {  
      "dynamoDB":{  
        "tableName":"iot1",
        "hashKeyField":"SerialNumber",
        "hashKeyValue":"${serial_number}",
        "rangeKeyField":"Timestamp",
        "rangeKeyValue":"${timestamp()}",
        "roleArn":"arn:aws:iam::123275298972:role/iot1-role"
      }
    }
  ]
}

aws iot create-topic-rule --rule-name "iot1_rule" --topic-rule-payload  file://iot1-rule.txt

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
-- test sending data through mosquitto client
apt-get install mosquitto-clients

mosquitto_pub \
	--cafile ../ssl/root-CA.crt \
	--cert ../ssl/cert.pem \
	--key ../ssl/privkey.pem \
	-h a1arqmop0meczp.iot.us-west-2.amazonaws.com \
	-p 8883 -q 1 -d \
	-t "topic/iot1/data" \
	-i iot-client1 \
	-m "{\"serial_number\": \"1234567\",  \"humidity\": \"60\"}"



