#!/usr/bin/env python

import argparse
import asyncio, logging
import datetime
from ble_serial.bluetooth.ble_interface import BLE_interface
import cem_parser

logger = logging.getLogger(__name__)

parser = cem_parser.cem_parser()

output_file = None


def parse_cmdline():
    parser = argparse.ArgumentParser(
        description = "CEM BLE meter frame logger"
    )
    parser.add_argument(
        "-i", "--hcidev",
        help = "BT HCI device name",
        default = "hci0"
    )
    parser.add_argument(
        "-b", "--bdaddr",
        help = "BT device address",
        default = ""
    )
    parser.add_argument(
        "-o", "--output",
        help = "write data to file",
        default = ""
    )
    parser.add_argument(
        "-v", "--verbose",
        help = "increase verbosity",
        action = "count", default = 1
    )
    args = parser.parse_args()
    return args


def receive_callback(value: bytes):
    logger.debug("Received:", value)
    for i in value:
        parser.add_data(i)
        measurements = parser.check_frame()
        if measurements:
            #logger.info("data: " + ','.join(f'{m.get_value()},{m.get_unit()}' for m in measurements))
            global output_file
            if output_file:
                output_file.write(f"{datetime.datetime.now()}," + ','.join(f'{m.get_value()},{m.get_unit()}' for m in measurements) + "\n")
                output_file.flush()


async def main():
    # None uses default/autodetection, insert values if needed
    SERVICE_UUID = None
    WRITE_UUID = None
    READ_UUID = "0000fff2-0000-1000-8000-00805f9b34fb"

    logger.info("Start main")

    args = parse_cmdline()
    if not args.bdaddr:
        logger.error("No bluetoot address provided")
        return

    global output_file
    if args.output:
        output_file = open(args.output, "a")
        logger.info(f"write to output file {args.output}")

    device = args.bdaddr
    adapter = args.hcidev

    ble = BLE_interface(adapter, SERVICE_UUID)
    ble.set_receiver(receive_callback)

    try:
        await ble.connect(device, "public", 10.0)
        await ble.setup_chars(WRITE_UUID, READ_UUID, "r")

        while True:
            await asyncio.sleep(10)

    finally:
        logger.info("Disconnect Bluetooth")
        if output_file:
            output_file.close()
        await ble.disconnect()


if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt as e:
        print("Interrupted by key")