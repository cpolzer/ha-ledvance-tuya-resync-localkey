#!/usr/bin/env python3

import getpass
from typing import Tuple
import json
import yaml

from pyscript_modules.tuya.api import TuyaAPI
from pyscript_modules.tuya.exceptions import InvalidAuthentication

def getFriendlyName(id, schemas) -> str:
    for schema in schemas:
        if schema['id'] == int(id):
            return schema['code'] 

def get_scene_name() -> str:
    def ask_until_ok(fn) -> str:
        while True:
            try:
                return fn()
            except KeyboardInterrupt as e:
                print("Aborted.")
                raise
            except:
                pass
            print()
    return (
        ask_until_ok(lambda: input("Please enter the alias for your settings (as in scene/preset): "))
    )

def get_device_id() -> str:
    def ask_until_ok(fn) -> str:
        while True:
            try:
                return fn()
            except KeyboardInterrupt as e:
                print("Aborted.")
                raise
            except:
                pass
            print()
    return (
        ask_until_ok(lambda: input("Please enter id of the device you want to capture: "))
    )


def get_login() -> Tuple[str, str]:
    def ask_until_ok(fn) -> str:
        while True:
            try:
                return fn()
            except KeyboardInterrupt as e:
                print("Aborted.")
                raise
            except:
                pass
            print()
    return (
        ask_until_ok(lambda: input("Please put your Tuya/Ledvance username: ")),
        ask_until_ok(lambda: getpass.getpass("Please put your Tuya/Ledvance password: "))
    )

def main():
    username, password = get_login()
    device_id = get_device_id()
    preset_name = get_scene_name()

    api = TuyaAPI(username, password)
    try:
        api.login()
    except InvalidAuthentication:
        print("Invalid authentication.")
        exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")

    print('---------------------------')


    for group in api.groups():
        for dev in api.devices(group['groupId']):
            if dev.id == device_id:
                print(f'Extracting settings for device {dev.name} and id {dev.id}')    

                infos = []
                for dps in dev.dps:
                        info = {
                            "id": dps,
                            "friendlyName": getFriendlyName(dps, dev.schema),
                            "value": dev.dps[dps],
                        }
                        print(f'\n{json.dumps(info)}')  
                        infos.append(info)
                preset = {
                    'device_name': dev.name,
                    'device_id': dev.id,
                    'scene': preset_name,
                    'settings': infos
                }
                with open(f'device-{dev.name}-{dev.id}-setting-{preset_name}.json', "w") as outfile:
                    outfile.write(json.dumps(preset, indent=4))
                
    print('---------------------------')

if __name__ == "__main__":
    main()

def getFriendlyName(id, schemas) -> str:
    for schema in dev.schema:
        if schema.id == id:
            return schema.code 