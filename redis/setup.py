import typing

if typing.TYPE_CHECKING:
    from redgrease import (
        GearsBuilder,
        execute
    )


GearsBuilder().foreach(
    lambda x: execute(
        "XADD", "notifications", "*", *sum([[k, v] for k, v in x.items()], [])
    )
).register(eventTypes=["hset", "hmset"], mode="sync")
