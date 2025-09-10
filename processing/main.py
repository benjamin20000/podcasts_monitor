from shared.kafka_consumer import Consumer
from processor import Processor
from shared.config import processing_kafka_topic


def main():
    consumer = Consumer(processing_kafka_topic)
    processor = Processor()
    consumer.consume(processor.process)


if __name__ == "__main__":
    main()