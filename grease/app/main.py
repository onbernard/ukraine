import sys

from redis_streams.consumer import Consumer
from redis import (
    Redis
)

def main():
    redis_conn = Redis(decode_responses=True)
    consumer = Consumer(
        redis_conn = redis_conn,
        stream = "notifications",
        consumer_group = "GROUP",
        batch_size=1,
        max_wait_time_ms=1000
    )

    while True:
        messages = consumer.get_items()
        n_messages = len(messages)
        for i, item in enumerate(messages):
            print(f"PROCESSING {i}/{n_messages} : {item}")
            consumer.remove_item_from_stream(item_id=item.msgid)


if __name__=="__main__":
    main()