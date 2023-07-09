import hassapi as hass
# import globals

#
# App to send notification when a sensor changes state
#
# Args:
#
# sensor: sensor to monitor e.g. sensor.upstairs_smoke
# idle_state - normal state of sensor e.g. Idle
# turn_on - scene or device to activate when sensor changes e.g. scene.house_bright
# Release Notes
#
# Version 1.0:
#   Initial Version


#   module: vacuum_scheduler
#   class: VacuumScheduler
#   vacuum: vacuum.rockrobo
#   presence:
#     sensor: person.mark
#     interrup: true
#   min_frequency: 0.5
#   max_frequency: 1.5
#   rooms:
#     - name: livingroom
#       service_call:
#         service: vacuum.send_command
#           data:
#             entity_id: vacuum.rockrobo
#             command: segmented_cleanup
#             params:
#               segment_ids: ['Зал']
#               repeats: 2
#       frequency: 24
#       time: ["11:00"]


from datetime import datetime, timedelta


import importlib
import subprocess
try:
    importlib.import_module("croniter")
except ImportError:
    subprocess.call(['pip3', 'install', 'croniter'])
    
from croniter import croniter


STATE_SENSOR = "sensor.vacuum_schedule"
STATE_SENSOR_VALUE = "on"
VACUUM_READY_STATES = ["idle", "returning", "docked"]

class VacuumScheduler(hass.Hass):
    def initialize(self):
        self.adapi = self.get_ad_api()
        
        self.log("Initializing vacuum automation")
        
        # load configuration
        self.min_frequency = self.args["min_frequency"]
        self.max_frequency = self.args["max_frequency"]
        self.rooms = {
            room["name"]: room
            for room in self.args["rooms"]
        }
        self.vacuum = self.get_entity(self.args["vacuum"])
        # display loaded config
        self.log(f"Known rooms: {self.rooms.keys()}")
        self.log(f"Cleaning: {self.min_frequency}x - {self.max_frequency}x of frequency")
        
        # reset cleaning if reloaded after error:
        if self.vacuum.get_state() in VACUUM_READY_STATES:
            self.log("Resetting vacuum room")
            self.current_room = None 
        
        # im-memory state
        self.clear_queue()
        self.clear_force_clean()  # on app restart all run_at(s) are lost!
        
        # subscribe to changes
        # to trigger cleaning while home is empty:
        self.listen_state(self.presence_change, self.args["presence"]["sensor"])
        # to detec completion of the cleaning:
        self.listen_state(self.vacuum_change, self.args["vacuum"])
        
        # attempt force clean now
        self.attempt_force_clean(None)
        
        # TODO: validate crontab
        #TODO: validate all other options

    def presence_change(self, entity, attribute, old, new, kwargs):
        self.log(f"Change of presence {old} -> {new}")
        if new == "off": # nobody home
            self.clean_on_no_presence()
        elif new == "on":  # somebody home
            # clear queue
            self.clear_queue()

    def clean_on_no_presence(self):
        no_presence_clean = {}
        for room in self.rooms.keys():
            last_clean = self.get_last_clean_time(room)
            if last_clean is None:
                no_presence_clean[room] = datetime.now()
            else:
                no_presence_clean[room] = last_clean + \
                    timedelta(hours=self.rooms[room]["frequency"] * self.min_frequency)
        
        no_presence_clean_start_now = {}
        for room, clean_starting in no_presence_clean.items():
            if clean_starting <= datetime.now():
                self.log(f"Room {room} should be cleaned since {clean_starting}")
                no_presence_clean_start_now[room] = clean_starting
            else:
                self.log(f"Room {room} shouldn't be cleaned yet {clean_starting}")

        self.log(f"Rooms to clean while no presence {list(no_presence_clean_start_now.keys())}")
        
        # start cleaning of rooms now
        # TODO: order by how long are we delayed
        for room in no_presence_clean_start_now.keys():
            self.log(f"Adding {room} to cleaning queue (no presence)")
            self.enqueue_room(room)  # no force
        if no_presence_clean_start_now:  # start if any rooms have to be cleaned now
            self.clean()

    def convert_to_cleaning_slot(self, room, clean_time):
        # for force clean move to the closest cleaning slot
        # TODO: support mulitiple slots
        iter = croniter(self.rooms[room]["schedule"], clean_time)
        prev = iter.get_prev(datetime)
        if ((datetime.now() - prev) < timedelta(seconds=59)): # crontab can't operate on seconds
            return prev
        return iter.get_next(datetime) # get next matching slot
        # input_time_str = str(clean_time)
        # slot_same_day = (
        #     clean_time.hour < self.rooms[room]["time"]["hour"]
        #     or (
        #         clean_time.hour == self.rooms[room]["time"]["hour"] and 
        #         clean_time.minute < self.rooms[room]["time"]["minute"]
        #     )
        # )
        # clean_time = clean_time.replace(hour=self.rooms[room]["time"]["hour"], minute=self.rooms[room]["time"]["minute"])
        # if not slot_same_day: # it is next day
        #     clean_time += timedelta(days=1)
        # self.log(f"Converted {input_time_str} to {clean_time}")
        # return clean_time

    def attempt_force_clean(self, _):  # ignore kwarg
        next_force_clean = {}
        for room in self.rooms.keys():
            last_clean = self.get_last_clean_time(room)
            if last_clean is None:
                next_force_clean[room] = self.convert_to_cleaning_slot(room, datetime.now())
            else:
                next_force_clean[room] = self.convert_to_cleaning_slot(
                    room,
                    last_clean + \
                    timedelta(hours=self.rooms[room]["frequency"] * self.max_frequency)
                )
        
        # select rooms that we need to clean now
        clean_now = {
            room: clean_time
            for room, clean_time in next_force_clean.items()
            if clean_time <= datetime.now()
        }
        self.log(f"Rooms to clean now: {list(clean_now.keys())}")
        clean_later = {
            room: clean_time
            for room, clean_time in next_force_clean.items()
            if clean_time > datetime.now()
        }
        self.log(f"Rooms to clean later: {list(clean_later.keys())}")
        
        # for each next force clean schedule attempt
        for room, clean_time in clean_later.items():
            # check is run_at is already scheduled to the same moment
            current_force_clean_time = self.get_force_clean_time(room)
            
            # if it is in the past OR it is in the future and new one is sooner
            # let's schedule (reversed)
            if (current_force_clean_time is not None) and \
                    current_force_clean_time > datetime.now() and \
                    current_force_clean_time < clean_time:
                self.log(f"Skipping scheduling of force clean of {room} - already scheduled at {current_force_clean_time}")
                continue
            self.log(f"Scheduling force clean of {room} at {clean_time}")
            self.set_force_clean_time(room, clean_time)
            self.run_at(self.attempt_force_clean, clean_time)  # recursive !
        
        # start cleaning of rooms now
        # TODO: order by how long are we delayed
        for room in clean_now.keys():
            self.log(f"Adding {room} to cleaning queue")
            self.enqueue_room(room, True)
        if clean_now:  # start if any rooms have to be cleaned now
            self.clean()
        
    def clean(self):
        if self.current_room is not None:
            self.log("Vacuum is busy, awaiting")
            return # await until cleaning will complete
        
        next_room, _ = self.dequeue_room()
        
        if next_room is None:
            self.log("Cleaning queue is empty")
            # try to schedule cleaning againm maybe something from future is ready to be cleaned
            self.attempt_force_clean(None)
            return # nothing to clean

        # select room and start cleaning
        self.current_room = next_room
        
        # TODO: if queue is empty -> notify and propose postpone
        
        service_call = dict(self.rooms[self.current_room]["service_call"])
        self.log(f"Starting cleaning of {self.current_room}")
        service_call_name = service_call.pop("service")
        
        self.call_service(service_call_name.replace('.','/'), **service_call["data"])

    def vacuum_change(self, entity, attribute, old, new, kwargs):
        if new in VACUUM_READY_STATES:
            if not  self.current_room:
                # maybe started manually?
                return
                
            finished_room = self.current_room
            
            #if not self.vacuum.get_state(attribute="finishedFlag"):
            #    self.log(f"Vacuum finished {room}, but not cleaned")
            #else:    
            
            # successful cleaning
            self.log(f"Vacuum cleaned {finished_room}")
        
            # save date
            self.set_last_clean_time(finished_room, datetime.now())
            
            # proceed to the next room
            self.current_room = None
            self.clean()  # proceed handling the queue

    # methods to manage state
    def get_last_clean_time(self, room):
        clean_history = self.get_state(STATE_SENSOR, attribute="clean_history")
        if clean_history is None:
            return None
        if room not in clean_history:
            return None
        if clean_history[room] is None:
            return None
        return datetime.fromisoformat(clean_history[room])

    def set_last_clean_time(self, room, value):
        clean_history = self.get_state(STATE_SENSOR, attribute="clean_history")
        if clean_history is None:
            clean_history = {}
        clean_history[room] = value.isoformat() if value is not None else None
        self.set_state(
            STATE_SENSOR,
            state = STATE_SENSOR_VALUE,
            attributes = {"clean_history": clean_history}
        )
    
    def get_force_clean_time(self, room):
        force_clean_schedule = self.get_state(STATE_SENSOR, attribute="force_clean_schedule")
        if force_clean_schedule is None:
            return None
        if room not in force_clean_schedule:
            return None
        if force_clean_schedule[room] is None:
            return None
        return datetime.fromisoformat(force_clean_schedule[room])

    def set_force_clean_time(self, room, value):
        force_clean_schedule = self.get_state(STATE_SENSOR, attribute="force_clean_schedule")
        if force_clean_schedule is None:
            force_clean_schedule = {}
        force_clean_schedule[room] = value.isoformat() if value is not None else None
        self.set_state(
            STATE_SENSOR,
            state = STATE_SENSOR_VALUE,
            attributes = {"force_clean_schedule": force_clean_schedule}
        )
    
    def clear_force_clean(self):
        self.set_state(
            STATE_SENSOR,
            state = STATE_SENSOR_VALUE,
            attributes = {"force_clean_schedule": {}}
        )

    @property
    def current_room(self):
        # return None if no room
        return self.get_state(STATE_SENSOR, attribute="current_room")

    @current_room.setter
    def current_room(self, value):
        self.set_state(
            STATE_SENSOR,
            state = STATE_SENSOR_VALUE,
            attributes = {"current_room": value}
        )

    # cleaning queue management
    def enqueue_room(self, room, force=False):
        queue = self.get_state(STATE_SENSOR, attribute="queue")
        if queue is None:
            queue = []
        if room in [queue_item["room"] for queue_item in queue]:
            self.log(f"Skipping addition of {room} to queue")
        queue.append({
            "room": room,
            "force": force
        })
        self.set_state(
            STATE_SENSOR,
            state = STATE_SENSOR_VALUE,
            attributes = {"queue": queue}
        )

    def dequeue_room(self):
        queue = self.get_state(STATE_SENSOR, attribute="queue")
        if not queue:
            return None, False
        next_room = queue[0]
        queue = queue[1:]
        self.set_state(
            STATE_SENSOR,
            state = STATE_SENSOR_VALUE,
            attributes = {"queue": queue}
        )
        return next_room["room"], next_room["force"]
    
    def clear_queue(self):
        self.set_state(
            STATE_SENSOR,
            state = STATE_SENSOR_VALUE,
            attributes = {"queue": []}
        )
