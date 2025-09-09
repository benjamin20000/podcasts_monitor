from stt_service import SttService
from shared.kafka_consumer import Consumer
from shared.config import stt_kafka_topic


def main():
    stt_service = SttService()
    stt_consumer = Consumer(stt_kafka_topic)
    stt_consumer.consume(stt_service.process_stt)


if __name__ == "__main__":
    main()