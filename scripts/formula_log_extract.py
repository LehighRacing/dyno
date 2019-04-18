import sys

from pprint import pprint

import cantools

if len(sys.argv) != 3:
    sys.exit(1)

db_file = sys.argv[1]
trace_file = sys.argv[2]

db = cantools.database.load_file(db_file)

last_rpm = 0
GEAR_RATIO = (2.81 * 1.632 * 0.328)

print("ts,dyno_torque,rpm,torque,hp")

with open(trace_file) as f:
    for line in f:
        line = line.strip()

        timestamp, source, data = line.split(", ", 2)
        if source == "torque":
            torque = float(data)

            engine_torque = torque / GEAR_RATIO
            hp = last_rpm * engine_torque / 5252

            print("{}, {:.3f}, {}, {:.3f}, {:.3f}".format(timestamp, torque, last_rpm, engine_torque, hp))
            # print("ts: {} dyno_torque: {:.3f} rpm: {}  torque: {:.3f} hp: {:.3f}".format(timestamp, torque, last_rpm, engine_torque, hp))

        elif source.startswith("can_"):
            ident = int(source.split("_")[1])
            raw_data = bytearray(int(x) for x in data.strip("[]").split(" "))

            decoded = db.decode_message(ident, raw_data)

            # print('\t'.join([str(ident), str(list(raw_data)), str(decoded)]))

            if "rpm" in decoded:
                last_rpm = decoded["rpm"]
