from enum import Enum


class OrderStatus(Enum):
    PENDING = "order_status_pending"
    COMPLETED = "order_status_completed"
    CANCELLED = "order_status_cancelled"


ORDER_STATUS_TYPE = "order_status"
