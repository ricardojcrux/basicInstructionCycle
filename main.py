# Import basicCycle module from cpu file.
from cpu import basicCycle

# Create memory array with 200 empty spaces and program array with all four programs.
memory = [""]*200
programs = ["program1.txt","program2.txt","program3.txt","program4.txt"]

# Call the object cycle from basicCycle class.
cycle = basicCycle(memory, programs)

# Method that read each program and store the instructions in memory
cycle.startCycle() 