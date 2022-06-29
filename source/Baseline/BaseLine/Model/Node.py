from .Relation import *
from .Utils import *
from .EventInstance import *
from .Event import*
from .Pattern import*


class Node:
    def __init__(self, ids_event, bitmap, patterns=None):
        self.ids_event = ids_event
        self.bitmap = bitmap
        self.patterns = patterns

    def get_ids_events(self):
        return tuple(self.ids_event)

    # def get_list_events_label(self):
    #     return tuple([event.label for event in self.events])

    def get_bitmap(self):
        return self.bitmap

    def get_support(self):
        return len(self.bitmap)

    def get_patterns(self):
        return self.patterns

    def to_dict(self, event_table, maxper, minPS, event_instance_table=None):
        result = {}
        event_labels = self.get_ids_events()
        pattern_result = []
        for pattern in self.patterns:
            if pattern.isSeasonal:
                obj = pattern.to_dict(event_labels, maxper, minPS,
                                      event_instance_table)
                pattern_result.append(obj)
        event_name = ','.join(event_labels)

        if pattern_result:
            result['name_node'] = event_name
            result['patterns'] = pattern_result

        return result

    def __str__(self):
        return ','.join(self.ids_event)
