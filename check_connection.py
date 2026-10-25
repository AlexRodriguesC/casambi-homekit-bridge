"""Quick check that a Casambi network can be controlled over this PC's Bluetooth."""
import asyncio
import getpass

from CasambiBt import Casambi, discover


def label(item):
    return getattr(item, "name", None) or repr(item)


async def main():
    print("Scanning for Casambi networks over Bluetooth (10-20 seconds)...")
    devices = await discover()
    if not devices:
        print("No Casambi devices found. Move closer to a light, and close the Casambi phone app.")
        return

    for i, dev in enumerate(devices):
        print(f"[{i}] {getattr(dev, 'name', '?')}  {dev.address}")
    choice = int(input("Pick a device number: ") or 0)
    device = devices[choice]

    password = getpass.getpass("Network password (typed hidden): ")

    casa = Casambi()
    try:
        await casa.connect(device, password)
        print("\nConnected.")

        print(f"\nUnits ({len(casa.units)}):")
        for unit in casa.units:
            print("  -", unit)

        print(f"\nGroups ({len(casa.groups)}):")
        for group in casa.groups:
            print("  -", label(group))

        print(f"\nScenes ({len(casa.scenes)}):")
        for i, scene in enumerate(casa.scenes):
            print(f"  [{i}] {label(scene)}")

        if casa.scenes:
            pick = input("\nScene number to activate (blank to skip): ").strip()
            if pick:
                await casa.switchToScene(casa.scenes[int(pick)])
                print("Scene sent. Did the lights change?")
    finally:
        await casa.disconnect()


asyncio.run(main())
