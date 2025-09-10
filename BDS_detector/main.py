from detector import Detector
from shared.kafka_consumer import Consumer
from shared.config import bds_kafka_topic


def main():
    kafka_consumer = Consumer(bds_kafka_topic)
    detector = Detector()
    kafka_consumer.consume(detector.detect)


if __name__ == "__main__":
    main()