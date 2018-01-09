from pykafka import KafkaClient
from pykafka import SslConfig

config = SslConfig(cafile='/soft/kafka_2.10-0.10.0.1/SSL/ca-cert',certfile='/soft/kafka_2.10-0.10.0.1/SSL/client_120.27.144.161_client.pem',keyfile='/soft/kafka_2.10-0.10.0.1/SSL/client_120.27.144.161_client.key',password='JX#DV@123')  # optional
client = KafkaClient(hosts="120.27.144.161:9093",ssl_config=config)
topic=client.topics
print topic
#consumer = topic.get_simple_consumer(consumer_group='maybe__zhu',auto_commit_enable=True,reset_offset_on_start=True,auto_offset_reset=OffsetType.LATEST)
#for i in consumer:
#    print i.value

