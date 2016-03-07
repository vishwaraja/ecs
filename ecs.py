#!/usr/bin/env python
# Vishwaraja Pathi
# <2016-03-06 19:53 PT>

import logging
import random
import sys

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


class ElevatorControlSystem:
    """
    Top level class to control a system of multiple elevators.
    Note that no actions are performed until "step" function is called.
    """

    def __init__(self, num_elevators):
        """
        :param num_elevators: Number of elevators to initialize the system with.
        """
        self.elevators = [Elevator(x) for x in range(num_elevators)]
        self.pickup_requests = []

    def status(self):
        """
        :return: List containing status of every elevator in the system.
        """
        return [x.status() for x in self.elevators]

    def update(self, elevator_id, floor_number, goal_floor):
        """
        :param elevator_id: id of the elevator to update
        :param floor_number: new floor number of this elevator
        :param goal_floor: new goal number of this elevator
        """
        self.elevators[elevator_id].update(floor_number, goal_floor)

    def pickup(self, pickup_floor, direction):
        """
        Queue a new pickup request for this elevator control system.

        :param pickup_floor: floor this request was made
        :param direction: -1 for down, +1 for up
        """
        self.pickup_requests.append([pickup_floor, direction])

    def step(self):
        """
        Iterates through the pickup requests and assigns an elevator to each request.
        Also steps through each elevator and moves it up or down by one floor based on the request.
        """
        # Iterate through all the pickup requests we have
        for pickup_request in self.pickup_requests:
            elevator = self.elevators[self.find_elevator_for_pickup_request(pickup_request)]
            logger.info("Found elevator with id %s for pickup_request %s", elevator.elevator_id, pickup_request)
            logger.info("Setting goal for elevator %s to floor %s", elevator.elevator_id, pickup_request[0])
            elevator.update(elevator.current_floor, pickup_request[0])
            elevator.is_fulfilling_request = True
        del self.pickup_requests[:]

        # If an elevator is fulfilling request, it goes in the direction it is supposed to
        # If it is not, we assume that it has reached its goal floor
        for elevator in self.elevators:
            if elevator.current_floor == elevator.goal_floor:
                elevator.is_fulfilling_request = False

            if elevator.is_fulfilling_request:
                if elevator.get_direction() < 0:
                    elevator.current_floor -= 1
                else:
                    elevator.current_floor += 1

    def find_elevator_for_pickup_request(self, pickup_request):
        """
        :param pickup_request: [floor_number, direction]
        :return: elevator_id corresponding to the closest elevator
        """
        all_offsets = {}

        for elevator in self.elevators:
            pickup_floor = pickup_request[0]
            direction = pickup_request[1]

            delta = abs(pickup_floor - elevator.current_floor)
            if ((direction < 0 and elevator.get_direction() < 0) or
                    (direction > 0 and elevator.get_direction() > 0)) and \
                    (not elevator.is_fulfilling_request):
                all_offsets[elevator.elevator_id] = delta

        if len(all_offsets) == 1:
            logger.info("Found only one elevator for pickup request %s", pickup_request)
            return all_offsets.keys()[0]
        elif len(all_offsets) == 0:
            logger.info("Found no elevator for pickup request %s", pickup_request)
            return random.choice([x for x in self.elevators if not x.is_fulfilling_request]).elevator_id
        else:
            logger.info("Found multiple elevators for pickup request %s", pickup_request)
            min_val = min(all_offsets.itervalues())
            for key, value in all_offsets.iteritems():
                if value == min_val:
                    return key


class Elevator:
    """
    Class to hold the data related to an elevator.
    """

    def __init__(self, elevator_id):
        """
        :param elevator_id: id to initalize this elevator with.
        """
        self.elevator_id = elevator_id
        self.current_floor = 1
        self.goal_floor = -1
        self.is_fulfilling_request = False

    def update(self, floor_number, goal_floor):
        """
        :param floor_number: new floor number for this elevator
        :param goal_floor: new goal number for this elevator
        """
        self.current_floor = floor_number
        self.goal_floor = goal_floor

    def status(self):
        """
        :return: a list of this elevators id, current floor and goal floor
        """
        return [self.elevator_id, self.current_floor, self.goal_floor]

    def get_direction(self):
        """
        :return: a negative number if the elevator is going down, or a positive number if it's going up
        """
        return self.goal_floor - self.current_floor


def main():
    """
    A REPL for this elevator control system. See the README for instructions on how to operate it.
    """
    args = sys.argv[1:]
    if len(args) < 1:
        sys.exit('Required argument missing: number of elevators.')
    ecs = ElevatorControlSystem(int(args[0]))

    while True:
        try:
            user_input = raw_input('Enter action: ')
        except EOFError:
            break

        if user_input == 'status':
            print ecs.status()
        elif user_input == 'step':
            ecs.step()
            print 'Step action performed'
        elif user_input.startswith('pickup'):
            pickup_floor, direction = user_input.split()[1:]
            ecs.pickup(int(pickup_floor), int(direction))
        elif user_input == 'debug':
            logger.setLevel(logging.DEBUG)
        elif user_input == 'info':
            logger.setLevel(logging.INFO)


if __name__ == "__main__":
    main()
