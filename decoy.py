from __future__ import division
from webthing import Action, Event, Property, SingleThing, Thing, Value, WebThingServer
import logging
import time
import uuid


class AmbientLightUpEvent(Event):
    def __init__(self, thing, data):
        Event.__init__(self, thing, 'ambient_light_up', data=data)


class AmbientLightDownEvent(Event):
    def __init__(self, thing, data):
        Event.__init__(self, thing, 'ambient_light_down', data=data)


class BrightAction(Action):
    def __init__(self, thing, input_):
        Action.__init__(self, uuid.uuid4().hex, thing, 'change_brightness', input_=input_)

    def perform_action(self):
        hour = int(time.strftime('%H'))
        if 18 < hour < 21:
            self.thing.set_property('on', True)
            self.thing.set_property('brightness', 50)
            self.thing.add_event(AmbientLightUpEvent(self.thing, 50))
        elif 5 < hour < 9:
            self.thing.set_property('brightness', 50)
            self.thing.add_event(AmbientLightDownEvent(self.thing, 50))
        elif hour > 20 or hour < 6:
            self.thing.set_property('brightness', 100)
            self.thing.add_event(AmbientLightUpEvent(self.thing, 100))
        elif 8 < hour < 19:
            self.thing.set_property('on', False)
            self.thing.set_property('brightness', 0)
            self.thing.add_event(AmbientLightDownEvent(self.thing, 0))
            logging.info('Off')


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
        },
        BrightAction)

    thing.add_available_event(
        'ambient_light_up',
        {
            'description': 'The ambient light has increase',
            'type': 'number',
            'unit': 'degree celsius',
        }
    )

    thing.add_available_event(
        'ambient_light_down',
        {
            'description': 'The ambient light has decrease',
            'type': 'number',
            'unit': 'degree celsius',
        }
    )

    return thing


def run_server():
    thing = initialize_thing()
    server = WebThingServer(SingleThing(thing), port=8888)

    try:
        logging.info('Server starts')
        server.start()
    except KeyboardInterrupt:
        logging.info('Server stops')
        server.stop()
        logging.info('Done')


if __name__ == '__main__':
    logging.basicConfig(
        level=10,
        format="%(asctime)s %(filename)s:%(lineno)s %(levelname)s %(message)s"
    )
    run_server()
