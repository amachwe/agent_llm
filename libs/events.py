class Event(object):

    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name
    
    def __str__(self):
        return self.name
    
EVENT_QUEUE_PREFIX = "event_queue"
SYSTEM_EVENT_QUEUE = "system_event_queue"
GENERATE_EVENT = Event("GENERATE_EVENT")
PROMPT_EVENT = Event("PROMPT_EVENT")
