#!/usr/bin/env python3

import getpass
from typing import Tuple
import json
import yaml

from pyscript_modules.tuya.api import TuyaAPI
from pyscript_modules.tuya.exceptions import InvalidAuthentication


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
  
    api = TuyaAPI(username, password)
    try:
        api.login()
    except InvalidAuthentication:
        print("Invalid authentication.")
        exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")

    print('---------------------------')
    print('Extracting schemas for all connected devices')    
    for group in api.groups():
        for dev in api.devices(group['groupId']):
            schema =  {
                    'device_name': dev.name,
                    'device_id': dev.id,
                    'schema': dev.schema
                }
            with open(f'device-{dev.name}-{dev.id}-schema.json', "w") as outfile:
                outfile.write(json.dumps(schema, indent=4))          
    

if __name__ == "__main__":
    main()

def getFriendlyName(id, schemas) -> str:
    for schema in dev.schema:
        if schema.id == id:
            return schema.code 