"""
BunqServer configuration module providing server endpoints and pinned keys for secure connections.
"""

from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True)
class BunqServer:
    """Configuration for a bunq API server including base URL and pinned key for secure connections"""
    base_url: str
    pinned_key: str


# Production bunq API server configuration
BUNQ_PUBLIC_SERVER: Final[BunqServer] = BunqServer(
    base_url="https://api.bunq.com/v1/",
    pinned_key="sha256/nI/T/sDfioCBHB5mVppDPyLi2HXYanwk2arpZuHLOu0="
)

# Sandbox bunq API server configuration for testing and development
BUNQ_SANDBOX_SERVER: Final[BunqServer] = BunqServer(
    base_url="https://public-api.sandbox.bunq.com/v1/",
    pinned_key="sha256/++MBgDH5WGvL9Bcn5Be30cRcL0f5O+NyoXuWtQdX1aI="
)