import asyncio
from dataclasses import dataclass
from ipv8.community import Community, CommunitySettings
from ipv8.configuration import ConfigBuilder, Strategy, WalkerDefinition, default_bootstrap_defs
from ipv8.keyvault.crypto import default_eccrypto
from ipv8.lazy_community import lazy_wrapper
from ipv8.messaging.payload_dataclass import VariablePayload
from ipv8.types import Peer
from ipv8.util import run_forever
from ipv8_service import IPv8

COMMUNITY_ID = bytes.fromhex("2c1cc6e35ff484f99ebdfb6108477783c0102881")
SERVER_PUBLIC_KEY = bytes.fromhex("4c69624e61434c504b3a86b23934a28d669c390e2d1fc0b0870706c4591cc0cb178bc5a811da6d87d27ef319b2638ef60cc8d119724f4c53a1ebfad919c3ac4136c501ce5c09364e0ebb")

EMAIL = "s.raghavendran@student.tudelft.nl"
GITHUB_URL = "https://github.com/swetha14-r/cs4160_blockchain"
NONCE = 389213872


class SubmissionPayload(VariablePayload):
    msg_id = 1
    format_list = ["varlenHutf8", "varlenHutf8", "q"]
    names = ["email", "github_url", "nonce"]

class ResponsePayload(VariablePayload):
    msg_id = 2
    format_list = ["?", "varlenHutf8"]
    names = ["success", "message"]

class Lab1Community(Community):
    community_id = COMMUNITY_ID

    def __init__(self, settings: CommunitySettings) -> None:
        super().__init__(settings)
        self.add_message_handler(ResponsePayload, self.on_response)
        self.server_peer = None
        self.submitted = False

    @lazy_wrapper(ResponsePayload)
    def on_response(self, peer: Peer, payload: ResponsePayload) -> None:
        print(f"Response from server: success={payload.success}, message={payload.message}")

    def find_server(self):
        for peer in self.get_peers():
            if peer.public_key.key_to_bin() == SERVER_PUBLIC_KEY:
                return peer
        return None

    async def started(self) -> None:
        self.register_task("submit", self.try_submit, interval=5.0, delay=5.0)

    async def try_submit(self) -> None:
        if self.submitted:
            return
        server = self.find_server()
        if server is None:
            print("Server not found yet, waiting...")
            return
        print("Server found! Sending submission...")
        self.ez_send(server, SubmissionPayload(EMAIL, GITHUB_URL, NONCE))
        self.submitted = True

async def start_ipv8() -> None:
    with open("my_key.pem", "rb") as f:
        key_bin = f.read()
    key = default_eccrypto.key_from_private_bin(key_bin)

    builder = ConfigBuilder().clear_keys().clear_overlays()
    builder.add_key("my key", "curve25519", "my_key.pem")
    builder.add_overlay(
        "Lab1Community",
        "my key",
        [WalkerDefinition(Strategy.RandomWalk, 10, {"timeout": 3.0})],
        default_bootstrap_defs,
        {},
        [("started",)]
    )

    ipv8 = IPv8(builder.finalize(), extra_communities={"Lab1Community": Lab1Community})
    await ipv8.start()
    print("IPv8 started, looking for server...")
    await run_forever()
    await ipv8.stop()

asyncio.run(start_ipv8())