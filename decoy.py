from __future__ import division
from webthing import Action, Property, SingleThing, Thing, Value, WebThingServer
import logging
import subprocess
import uuid


class ChangeBrightnessAction(Action):
    def __init__(self, thing, input_):
        Action.__init__(self, uuid.uuid4().hex, thing, 'change_brightness', input_=input_)

    def perform_action(self):
        self.thing.set_property('brightness', self.input['brightness'])


def initialize_thing():
    thing = Thing(
        'urn:dev:ops:smart_lamp_7256',
        'SLamp',
        ['OnOffSwitch', 'Light'],
        'A smart lamp connected to the web'
    )

    thing.add_property(
        Property(thing, 'on', Value(True), metadata={
            '@type': 'SwitchProperty',
            'title': 'On/Off',
            'type': 'boolean',
            'description': 'Shows if the lamp is on',
        })
    )

    thing.add_property(
        Property(thing, 'brightness', Value(50), metadata={
            '@type': 'BrightnessProperty',
            'title': 'Brightness',
            'type': 'integer',
            'description': 'The light level from 0 to 100',
            'minimum': 0,
            'maximum': 100,
            'unit': 'percent',
        })
    )

    thing.add_available_action(
        'change_brightness', {
            'title': 'Change Brightness',
            'description': "Change the lamp brightness to a given level",
            'input': {
                'type': 'object',
                'required': [
                    'brightness',
                ],
                'properties': {
                    'brightness': {
                        'type': 'integer',
                        'minimum': 0,
                        'maximum': 100,
                        'unit': 'percent',
                    },
                },
            },
        },
        ChangeBrightnessAction)

    return thing


def run_server():
    thing = initialize_thing()
    subprocess.run("fuser -k 8888/tcp", shell=True)
    server = WebThingServer(SingleThing(thing), port=8888)
    server.start()


def decoy():
    logging.basicConfig(
        level=10,
        format="%(asctime)s %(filename)s:%(lineno)s %(levelname)s %(message)s"
    )
    run_server()
