"""PILOT API resource modules."""

from pilot.resources.admin import AdminResource
from pilot.resources.briefing import BriefingResource
from pilot.resources.capture import CaptureResource
from pilot.resources.chat import ChatResource
from pilot.resources.decisions import DecisionsResource
from pilot.resources.delegations import DelegationsResource
from pilot.resources.email import EmailResource
from pilot.resources.graph import GraphResource
from pilot.resources.operations import OperationsResource
from pilot.resources.rpm import RPMResource
from pilot.resources.someday import SomedayResource
from pilot.resources.tasks import TasksResource

__all__ = [
    "AdminResource",
    "BriefingResource",
    "CaptureResource",
    "ChatResource",
    "DecisionsResource",
    "DelegationsResource",
    "EmailResource",
    "GraphResource",
    "OperationsResource",
    "RPMResource",
    "SomedayResource",
    "TasksResource",
]
