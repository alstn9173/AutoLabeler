import os


def get_desired_capabilities(app):
    desired_caps = {
        'app': os.getcwd() + "/" + app,
        'app-activity': '.MainActivity',
        'deviceName': 'AndroidEmulator',
        'platformName': 'Android',
        'platformVersion': '7.0'
    }
    return desired_caps
