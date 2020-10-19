from simplemonads import Future, run, _
import asyncio


async def effect(data=1):
    await asyncio.sleep(1)
    return data ** data


@run
def main():
    return Future(2) + effect + effect


def test_future_value():
    assert main() | {_: lambda x: x} == 256
