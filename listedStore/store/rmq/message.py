import json
from decimal import Decimal, ROUND_HALF_UP
from dataclasses import dataclass, field, asdict
from typing import List


def decimal_serializer(obj):
    if isinstance(obj, Decimal):
        return str(obj)
    raise TypeError("Type not serializable")


@dataclass
class MessageItem:
    name: str
    quantity: int
    price: Decimal
    subtotal: float = field(init=False)

    def __post_init__(self):
        self.subtotal = (self.quantity * self.price).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


@dataclass
class MessageContext:
    name: str
    items: List[MessageItem]
    total: Decimal = field(init=False)

    def __post_init__(self):
        self.total = sum(item.subtotal for item in self.items).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)


@dataclass
class Message:
    email: str
    subject: str
    context: MessageContext


    def json(self, indent=4) -> str:
        return json.dumps(asdict(self), indent=indent, default=decimal_serializer)
