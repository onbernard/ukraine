from typing import (
    Optional
)

import redis
from redis_om import (
    JsonModel,
    EmbeddedJsonModel,
    Field,
    Migrator,
)

class BaseModel(JsonModel):

    class Meta:
        global_key_prefix = "main"
        model_key_prefix = "base"
    
    def save(self, pipeline: Optional[redis.client.Pipeline] = None) -> "JsonModel":
        outp = super().save(pipeline)
        self.db().xadd(f"{self.__class__.__name__.lower()}", fields=self.dict())
        return outp