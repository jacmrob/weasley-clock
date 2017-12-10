import json
from pyicloud import PyiCloudService
import sys, os
import click


# give a user a "location" which is one of the 12 hands of the clock

class Phone:
    def __init__(self, profile):
        self.name = profile['username']
        self.api = PyiCloudService(profile['username'], profile['password'])
        self.iphone = self.login_to_phone(profile['device_num'])

    def get_location(self):
        return self.api.devices[1].location()

    def get_devices(self):
        return self.api.devices

    def get_status(self):
        return self.iphone.status()

    def login_to_phone(self, device_num):
        device = self.api.devices[device_num]
        print device.status()
        if self.api.requires_2fa:
            code = click.prompt('Please enter validation code')
            if not self.api.validate_verification_code(device, code):
                print "Failed to verify verification code"
                sys.exit(1)
        print device.status()
        print "returning device..."
        return device



if __name__ == '__main__':
    profile = {'username': 'jacqueline_roberti@alumni.brown.edu', 'password': '3lil_Birds', 'device_num': 1}
    jackie = Phone(profile)

    print jackie.get_devices()
    print jackie.iphone
    print jackie.get_location()
    print jackie.get_status()
