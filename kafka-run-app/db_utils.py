import sqlite3
import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def initialize_database():
    connection = sqlite3.connect(resource_path("data\\kafka.db"))
    cursor = connection.cursor()

    listOfTables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='KAFKA';").fetchall()
    if listOfTables == []:
        cursor.execute("create table KAFKA (KEY text, VALUE text)")

        kafka_home = "C:\kafka\kafka_folder_path"  #"C:\kafka\kafka_2.13-2.8.0"
        try:
            kafka_home = os.environ['KAFKA_HOME']
        except KeyError:
            print("Environment variable 'KAFKA_HOME' not found.")

        kafka_values = [
            ("KAFKA_HOME", kafka_home),
            ("ZOOKEEPER", kafka_home+"\\bin\windows\zookeeper-server-start.bat "+kafka_home+"\config\zookeeper.properties"),
            ("KAFKA_SERVER", kafka_home+"\\bin\windows\kafka-server-start.bat "+kafka_home+"\config\server.properties"),
            ("TOPIC_CREATE_PRE", kafka_home+"\\bin\windows\kafka-topics.bat --bootstrap-server "),
            ("KAFKA_PRODUCER_PRE", kafka_home+"\\bin\windows\kafka-console-producer.bat --broker-list "),
            ("KAFKA_CONSUMER_PRE", kafka_home+"\\bin\windows\kafka-console-consumer.bat --bootstrap-server ")
        ]
      
        cursor.executemany("insert into KAFKA values (?,?)", kafka_values)
        connection.commit()
      
    listOfTables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='KAFKA_DOCS';").fetchall()
   
    if listOfTables == []:
        cursor.execute("create table KAFKA_DOCS (id INTEGER PRIMARY KEY AUTOINCREMENT, title text, command text, enabled boolean)")

        RUN_FLOW = """
        Follow the steps to START
        First set KAFKA_HOME Environment variable and its value is 'kafka folder path'
        Then the follow below steps
        1. start zookeeper
        2. start kafka server
        3. create topic
        4. run producer , run consumer
        """
        STOP_FLOW = """
        Follow the steps to STOP
        1. stop producers, stop consumers
        2. stop kafka server
        3. stop zookeeper
        """

        ZOOKEEPER = cursor.execute("SELECT VALUE FROM KAFKA WHERE KEY='ZOOKEEPER'").fetchone()[0]
        KAFKA_SERVER = cursor.execute("SELECT VALUE FROM KAFKA WHERE KEY='KAFKA_SERVER'").fetchone()[0]
        TOPIC_CREATE = cursor.execute("SELECT VALUE FROM KAFKA WHERE KEY='TOPIC_CREATE_PRE'").fetchone()[0]+" localhost:9092  --create  --topic topic-name  --partitions 3  --replication-factor 1"
        KAFKA_PRODUCER_RUN = cursor.execute("SELECT VALUE FROM KAFKA WHERE KEY='KAFKA_PRODUCER_PRE'").fetchone()[0]+" localhost:9092  --topic topic-name"
        KAFKA_CONSUMER_RUN = cursor.execute("SELECT VALUE FROM KAFKA WHERE KEY='KAFKA_CONSUMER_PRE'").fetchone()[0]+" localhost:9092  --topic topic-name  --from-beginning"

        KAFKA_TOPIC_LIST = cursor.execute("SELECT VALUE FROM KAFKA WHERE KEY='TOPIC_CREATE_PRE'").fetchone()[0]+" localhost:9092  --list"
        KAFKA_TOPIC_DESCRIBE = cursor.execute("SELECT VALUE FROM KAFKA WHERE KEY='TOPIC_CREATE_PRE'").fetchone()[0]+" localhost:9092  --describe  --topic  topic-name"

        kafka_docs = [
            ("Get Started : Run Methods", RUN_FLOW, 1),
            ("Get Started : Stop Methods", STOP_FLOW, 1),
            ("Zookeeper Run", ZOOKEEPER, 1),
            ("Kafka Server Run", KAFKA_SERVER, 1),
            ("Token Create", TOPIC_CREATE, 1),
            ("Producer Run", KAFKA_PRODUCER_RUN, 1),
            ("Subscriber Run", KAFKA_CONSUMER_RUN, 1),
            ("Topic List", KAFKA_TOPIC_LIST, 1),
            ("Topic Describe", KAFKA_TOPIC_DESCRIBE, 1)
        ]
        cursor.executemany("insert into KAFKA_DOCS(title, command, enabled) values (?,?,?)", kafka_docs)
        connection.commit()

    connection.close()
