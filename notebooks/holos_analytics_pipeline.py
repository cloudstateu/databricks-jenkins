# Databricks notebook source
# MAGIC %md
# MAGIC # Pipeline

# COMMAND ----------

# MAGIC %scala
# MAGIC import io.relayr.data.analytics.functions.Runner
# MAGIC import scala.collection.JavaConversions._
# MAGIC import spark.implicits._
# MAGIC import collection.mutable._
# MAGIC import collection.JavaConverters._
# MAGIC 
# MAGIC val apiUrl = "https://cloud.stg.az.relayr.io"
# MAGIC val conf = dbutils.secrets.get(scope = "cloud_2_0", key = "configuration")
# MAGIC val jsons = new Runner().generateInputs(apiUrl, conf).asScala
# MAGIC val preprocessing_output = jsons.toDF("preprocessing_output")
# MAGIC preprocessing_output.createOrReplaceTempView("asset_data_list")
# MAGIC println(s"Generated dataframes for ${jsons.size} assets")

# COMMAND ----------

import json
from maintenance_solution_analytics.main import process_data

def process_data_wrapper(wrapped_feature_vector: str):
  """
  wrapper for process_data function of analytics module. Saves configuration field and wraps it with each event into a new json.
  """
  payload = json.loads(wrapped_feature_vector)
  configuration = payload["configuration"]
  events_list_json = process_data(json.dumps(payload["data"]))
  events_list = json.loads(events_list_json)
  new_events_list = [{"configuration": configuration, "data": event} for event in events_list]
  return new_events_list

# load preprocessed data and call analytics module
asset_feature_vectors = spark.table("asset_data_list")

analytics_output = asset_feature_vectors.rdd.map(lambda feature_vector: process_data_wrapper(feature_vector.preprocessing_output))

# COMMAND ----------

# check if analytics output is correct
# analytics_output.collect()

# COMMAND ----------

# flatten the resulting list of list into one list and create a pyspark dataframe with one column ("events") from it.
import json

analytics_output_flat = analytics_output.reduce(lambda a, b: a+b)
analytics_output_df = spark.createDataFrame(data=[[json.dumps(event)] for event in analytics_output_flat], schema=["events"])

# COMMAND ----------

#  display(analytics_output_df)

# COMMAND ----------

bootstrap_servers = "ehubs-holos-stg-analytics-temporary.servicebus.windows.net:9093"
event_hub = "holos-stg-hub-temporary-analytics"
security_protocol="SASL_SSL"
sasl_mechanism="PLAIN"
kafka_sasl = dbutils.secrets.get(scope = "cloud_2_0", key = "kafka_sasl")

sasl_jaas_config = 'kafkashaded.org.apache.kafka.common.security.plain.PlainLoginModule required username="$ConnectionString" password="%s";' % kafka_sasl

analytics_output_df.withColumnRenamed("events", "value") \
  .write  \
  .format("kafka") \
  .option("kafka.sasl.mechanism", sasl_mechanism) \
  .option("kafka.security.protocol", security_protocol) \
  .option("kafka.sasl.jaas.config", sasl_jaas_config) \
  .option("kafka.bootstrap.servers", bootstrap_servers) \
  .option("topic", event_hub) \
  .save()

# COMMAND ----------

# This cell may be used to listen to a event hub topic

# from azure.eventhub import EventHubConsumerClient
# def on_event(partition_context, event):
#    # Print the event data.
#     #print(event.enqueued_time)
#     print("Received the event: \"{}\" from the partition with ID: \"{}\"".format(event.body_as_str(encoding='UTF-8'), partition_context.partition_id))
# client = EventHubConsumerClient.from_connection_string(kafka_sasl, consumer_group="$Default", eventhub_name=event_hub)
# with client:
#  # Call the receive method. Read from the beginning of the partition (starting_position: "-1")
#  client.receive(on_event=on_event, starting_position="-1")

# COMMAND ----------

# Publish each event (== each row) of the analytics_output_df dataframe to eventhub

# import json
# from kafka import KafkaProducer
# from kafka.errors import KafkaError
# bootstrap_servers = "ehubs-holos-stg-analytics-temporary.servicebus.windows.net:9093"
# event_hub = "holos-stg-hub-temporary-analytics"
# security_protocol="SASL_SSL"
# sasl_mechanism="PLAIN"
# sasl_plain_username="$ConnectionString"
# #sasl_plain_password= "Endpoint=sb://ehubs-holos-stg-analytics-temporary.servicebus.windows.net/;SharedAccessKeyName=RootManageSharedAccessKey;SharedAccessKey=nGioF8eF8OTTNvs0hslS5NFXZU/N6cOxfEMfvbkakyE="
# val kafka_sasl = dbutils.secrets.get(scope = "cloud_2_0", key = "kafka_sasl")

# producer = KafkaProducer(
#   bootstrap_servers=[bootstrap_servers],
#   value_serializer=lambda m: json.dumps(m).encode('ascii'),
#   security_protocol=security_protocol,
#   sasl_mechanism=sasl_mechanism,
#   sasl_plain_username=sasl_plain_username,
#   sasl_plain_password=kafka_sasl
# )
# def on_send_success(record_metadata):
#     print(record_metadata.topic)
#     print(record_metadata.partition)
#     print(record_metadata.offset)
# def on_send_error(excp):
#     log.error('I am an errback', exc_info=excp)
#     # handle exception
# # produce asynchronously, Messages are sent in batches

# def publish_event(row):
#   #print(row.events)
#   producer.send(event_hub, row).add_callback(on_send_success).add_errback(on_send_error)


# for row in analytics_output_df.collect():
#   publish_event(row.events)

# # block until all async messages are sent
# producer.flush()

# COMMAND ----------


