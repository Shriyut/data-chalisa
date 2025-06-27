#!/bin/bash

# Set variables
PROJECT_ID=""
ZONE="us-central1-a"
MACHINE_TYPE="n1-standard-1"
INSTANCE_NAME="kafka-broker-1"
KAFKA_VERSION="3.6.1"
JAVA_VERSION="11"

# 1.  Install Java
echo "Installing Java..."
sudo apt update && \
  sudo apt install -y openjdk-"${JAVA_VERSION}"-jdk

# 2.  Download and Extract Kafka
echo "Downloading and extracting Kafka..."
wget https://downloads.apache.org/kafka/"${KAFKA_VERSION}"/kafka_2.13-"${KAFKA_VERSION}".tgz && \
  tar -xzf kafka_2.13-"${KAFKA_VERSION}".tgz && \
  sudo mv kafka_2.13-"${KAFKA_VERSION}" /opt/kafka

# 3.  Configure Kafka
echo "Configuring Kafka..."
EXTERNAL_IP=$(curl -s "http://metadata.google.internal/computeMetadata/v1/instance/network-interfaces/0/access-configs/0/external-ip" -H "Metadata-Flavor: Google")
sudo sed -i "s/#listeners=PLAINTEXT:\/\/:9092/listeners=PLAINTEXT:\/\/:"${EXTERNAL_IP}":9092/" /opt/kafka/config/server.properties && \
  sudo sed -i "s/zookeeper.connect=localhost:2181/zookeeper.connect="${EXTERNAL_IP}":2181/" /opt/kafka/config/server.properties && \
  sudo sed -i "s/#broker.id=0/broker.id=1/" /opt/kafka/config/server.properties

# 4.  Start ZooKeeper
echo "Starting ZooKeeper..."
sudo /opt/kafka/bin/zookeeper-server-start.sh /opt/kafka/config/zookeeper.properties &

# 5.  Start Kafka Broker
echo "Starting Kafka broker..."
sudo /opt/kafka/bin/kafka-server-start.sh /opt/kafka/config/server.properties &

# 6.  Configure Firewall Rules
echo "Configuring firewall rules..."
gcloud compute firewall-rules create allow-kafka \
    --project=$PROJECT_ID \
    --allow=tcp:9092,tcp:2181 \
    --source-ranges=0.0.0.0/0

echo "Kafka deployment complete!"
echo "You can access Kafka broker at ${EXTERNAL_IP}"