import simulator.computer as computer
from simulator.communication import Communication
from simulator.message import Message
from simulator.config import NodeState
import numpy as np
from utils.logger_config import logger

# collapse by message recieved
collapse_config = {
    "4": {
        "sent_msg_count": 1,
        "probability": 1
    }
}

reorder_config = None  # Placeholder for reorder configuration, if needed

colors = ["blue", "red", "green", "yellow", "purple", "pink", "orange", "cyan", "magenta", "lime", "teal", "lavender",
          "brown", "maroon", "navy", "olive", "coral", "salmon", "gold", "silver"]


def mainAlgorithm(self: computer.Computer, communication: Communication, _arrival_time, message=None):
    message_parts = message.split(" ")
    dist = float(message_parts[-3])
    parent = int(message_parts[-1])

    if dist + 1 < self.distance:
        self.parent = parent
        self.distance = dist + 1
        color_index = int(dist) % len(colors)
        self.color = colors[color_index]
        communication.send_to_all(self.id, f"running a BFS with distance {self.distance} from {self.id}", _arrival_time)


def init(self: computer.Computer, communication: Communication):
    if self.is_root:
        logger.info(f"{self.id} is the root")
        self.parent = self.id
        self.distance = 0
        communication.send_to_all(self.id, f"running a BFS with distance {self.distance} from {self.parent}")
        self.color = "#000000"
        self.state = NodeState.TERMINATED
    else:
        self.parent = None
        self.distance = np.inf
