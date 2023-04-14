import sys

sys.path.insert(0, "src/libs")

import os
from alfred5 import WorkflowClient, WorkflowError


async def main(client: WorkflowClient):
    from yconverter.client import YConverter

    match client.query:
        case "help":
            client.add_result("Help", "Usage: amount source destination")
            return
        case "list":
            key = os.environ["api_key"]
            converter = YConverter(key)
            for icon_path, source, destination in [
                ("icons/usdt.png", "USDT", "TRY"),
                ("icons/usd.png", "USD", "TRY"),
                ("icons/btc.png", "BTC", "USDT"),
                ("icons/eth.png", "ETH", "USDT"),
                ("icons/xau.png", "XAU", "USD"),
            ]:
                value = converter.convert(1, source, destination)
                client.add_result(
                    f"{value:,f}",
                    f"{source} -> {destination}",
                    icon_path=icon_path,
                    arg=f"{value:,f}",
                )
            return
        case _:
            assert client.query is not None
            argv = client.query.split(" ")
            amount = float(argv[0])
            if len(argv) == 1:
                client.add_result("Waiting source...", f"{amount} source destination")
                return

            source = argv[1].upper()
            if len(argv) == 2:
                client.add_result(
                    "Waiting destination...", f"{amount} {source} destination"
                )
                return
            if 3 > len(source) and len(argv) > 2:
                raise WorkflowError(
                    f"Source symbol is wrong!",
                    f"The length of `{source}` must be greater than 3",
                )

            destination = argv[2].upper()
            if 3 > len(destination):
                client.add_result(
                    f"Waiting for {3 - len(destination)} chars more...",
                    f"{amount} {source} {destination}",
                )
                return

            key = os.environ["OPEN_EXCHANGE_RATES_API_KEY"]
            converter = YConverter(key)
            value = converter.convert(amount, source, destination)
            client.add_result(
                f"{value:,f}",
                f"1 {source} = {value / amount:,f} {destination}",
                arg=f"{value:,f}",
            )


if __name__ == "__main__":
    WorkflowClient.run(main)
