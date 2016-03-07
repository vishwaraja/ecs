# ecs

This is a Elevator control system implemented in python.


To run:

1) From the project directory type:

	python ecs.py <number of elevators>
	
2) User can input one of the following options at the prompt:

	* status
	* step
	* update
	* pickup <pickup_floor> <direction>
	* debug 
	* info 
	
	
	Note : If you choose to enter pickup please enter two interger values corresponding the current floor and direction. Possible values for direction are "1" and "-1"
	 
	Note : The log level will be set accordingly if the user chooses to debug or info

