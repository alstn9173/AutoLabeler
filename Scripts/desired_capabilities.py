import os


def get_desired_capabilities(app):
    desired_caps = {
        'app': os.getcwd() + "/" + app,
        'deviceName': 'AndroidEmulator',
        'platformName': 'Android',
        'platformVersion': '7.1.2'
    }
    return desired_caps
