"""Router - handle message router (relaay)

Router to manage responses from a queue with relay.

"""

from typing import TYPE_CHECKING
from six.moves import queue

from .router_queue import MessageQueueRouter

if TYPE_CHECKING:
    from six.moves.queue import Queue


class MessageRelayRouter(MessageQueueRouter):
    _relay_queue: "Queue[pb.Result]"

    def __init__(
        self,
        request_queue: "Queue[pb.Record]",
        response_queue: "Queue[pb.Result]",
        relay_queue: "Queue[pb.Result]",
    ) -> None:
        self._relay_queue = relay_queue
        super(MessageRelayRouter, self).__init__(
            request_queue=request_queue, response_queue=response_queue
        )

    def _handle_msg_rcv(self, msg: "pb.Result") -> None:
        if msg.control.relay:
            self._relay_queue.put(msg)
            return
        super(MessageRelayRouter, self)._handle_msg_rcv(msg)
