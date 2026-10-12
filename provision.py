#!/usr/bin/env python3
"""USB Improv 配网；密码仅在进程内使用，不写文件、不打印。"""
import argparse
import getpass
import time
import serial

def frame(command, fields=()):
    args = b"".join(bytes([len(v.encode())]) + v.encode() for v in fields)
    rpc = bytes([command, len(args)]) + args
    out = b"IMPROV" + bytes([1, 3, len(rpc)]) + rpc
    return out + bytes([sum(out) & 255]) + b"\n"

def provision(port, ssid, password):
    if not 1 <= len(ssid.encode()) <= 32:
        raise ValueError("SSID must be 1-32 bytes")
    if password and not 8 <= len(password.encode()) <= 63:
        raise ValueError("WPA password must be 8-63 bytes")
    with serial.Serial(port, 115200, timeout=0.2) as conn:
        conn.reset_input_buffer()
        conn.write(frame(1, (ssid, password)))
        buf = bytearray()
        deadline = time.monotonic() + 60
        while time.monotonic() < deadline:
            buf.extend(conn.read(2048))
            while True:
                start = buf.find(b"IMPROV")
                if start < 0:
                    buf[:] = buf[-5:]
                    break
                del buf[:start]
                if len(buf) < 9:
                    break
                length = buf[8]
                total = 10 + length
                if len(buf) < total:
                    break
                packet = bytes(buf[:total]); del buf[:total]
                if (sum(packet[:-1]) & 255) != packet[-1]:
                    continue
                typ, data = packet[7], packet[9:-1]
                if typ == 2 and data and data[0]:
                    raise RuntimeError(f"Improv error: {data[0]}")
                if typ == 4 and len(data) >= 2 and data[0] in (1, 2):
                    fields = []; i = 2
                    while i < len(data):
                        n = data[i]; fields.append(data[i+1:i+1+n].decode(errors="replace")); i += n+1
                    print("Wi-Fi configured:", ", ".join(fields) or "connected")
                    return fields
        raise TimeoutError("No successful Wi-Fi provisioning response within 60 seconds")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", default="/dev/ttyACM0")
    parser.add_argument("--ssid")
    args = parser.parse_args()
    provision(args.port, args.ssid or input("2.4 GHz Wi-Fi SSID: "), getpass.getpass("Wi-Fi password: "))
