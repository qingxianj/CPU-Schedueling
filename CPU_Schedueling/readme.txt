Table of Contents
Overview
Features
Supported Algorithms
Installation
Usage
Example
Screenshots

Overview
The CPU Scheduling Simulator GUI is a user-friendly application built with Python's Tkinter library that allows users to simulate and visualize various CPU scheduling algorithms. Whether you're a student learning about operating systems or a developer interested in understanding scheduling mechanisms, this tool provides an interactive way to experiment with different scheduling strategies and observe their effects on task execution.

Features
Add and Manage Tasks: Input tasks with unique IDs, Arrival Times, Burst Times, and Priorities.
Multiple Scheduling Algorithms: Choose from First Come First Serve (FCFS), Round Robin (RR), Shortest Job First (SJF), Priority Non-Preemptive, and Priority Preemptive.
Execution Visualization: View detailed task execution information, including Completion Time (CT), Turnaround Time (TAT), and Waiting Time (WT).
Average Metrics: Automatically calculate and display average TAT and WT for all tasks.
Gantt Chart Generation: Visualize the scheduling sequence and task execution timelines through interactive Gantt charts.
Error Handling: Ensures unique Task IDs and validates input data to prevent errors during simulation.
Supported Algorithms
First Come First Serve (FCFS)

Executes tasks in the order they arrive.
Non-preemptive.
Round Robin (RR)

Assigns a fixed time quantum to each task in a cyclic order.
Preemptive.
Shortest Job First (SJF)

Executes the task with the shortest Burst Time next.
Non-preemptive.
Priority Non-Preemptive

Executes tasks based on priority levels.
Lower numerical value indicates higher priority.
Non-preemptive.
Priority Preemptive

Similar to Priority Non-Preemptive but can preempt currently running tasks if a higher priority task arrives.
Lower numerical value indicates higher priority.
Preemptive.
Installation
Prerequisites
Python 3.6 or higher: Ensure you have Python installed. You can download it from here.
Required Python Libraries
The application relies on the following Python libraries:

tkinter: Standard GUI library for Python (usually included with Python installations).
matplotlib: For generating Gantt charts.
Installing Dependencies
Tkinter: Most Python installations come with Tkinter. To verify, try importing it in Python:

python -c "import tkinter"
If you encounter an error, refer to Tkinter Installation Guide for your operating system.
Matplotlib: Install via pip if not already installed.
pip install matplotlib
Usage
Clone the Repository

Run the Application
python gui.py
Interact with the GUI

Add Tasks:
Enter a unique Task ID.
Specify Arrival Time (at), Burst Time (bt), and Priority (pr).
Click the "Add Task" button.

Delete Tasks:
Select a task from the task table.
Click the "Delete Selected Task" button.

Select Algorithm:
Choose your desired scheduling algorithm from the dropdown menu.

Run Algorithm:
For Round Robin, specify the Time Quantum (tq).
Click the "Run Algorithm" button to execute the simulation.

View Results:
The output area displays CT, TAT, WT for each task, along with average TAT and WT.
A Gantt chart visualizes the task execution timeline.

License
This project is licensed under the MIT License.