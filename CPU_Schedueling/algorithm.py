# algorithm.py

import matplotlib.pyplot as plt
import matplotlib

# Use the TkAgg backend for Tkinter compatibility
matplotlib.use('TkAgg')


def avg_wt_tat(data):
    """
    Calculate average Turnaround Time (TAT) and Waiting Time (WT).

    :param data: List of task dictionaries with 'ct' (completion time) key.
    :return: Dictionary with 'avg_tat' and 'avg_wt'.
    """
    print("Calculating average Turnaround Time (TAT) and average Waiting Time (WT)...")
    for idx, dct in enumerate(data):
        if 'ct' not in dct:
            print(f"Task index {idx} is missing 'ct': {dct}")
            raise KeyError(f"Task {dct['id']} is missing 'ct'")
        dct['tat'] = dct['ct'] - dct['at']
        dct['wt'] = dct['tat'] - dct['bt']
        print(f"Task {dct['id']}: CT={dct['ct']}, AT={dct['at']}, BT={dct['bt']}, TAT={dct['tat']}, WT={dct['wt']}")

    total_wt = sum(task['wt'] for task in data)
    total_tat = sum(task['tat'] for task in data)
    n = len(data)
    avg = {'avg_tat': total_tat / n, 'avg_wt': total_wt / n}
    print(f"Average Turnaround Time (Average TAT): {avg['avg_tat']:.2f}")
    print(f"Average Waiting Time (Average WT): {avg['avg_wt']:.2f}")
    return avg


def first_come_first_serve(data):
    """
    First Come First Serve (FCFS) scheduling algorithm.

    :param data: List of task dictionaries.
    :return: Tuple of (updated data, execution_log).
    """
    execution_log = []
    arrival_sorted = sorted(enumerate(data), key=lambda x: x[1]['at'])
    curr_time = 0

    for index, task in arrival_sorted:
        if task['at'] > curr_time:
            curr_time = task['at']  # Wait for the task to arrive
        start_time = curr_time
        end_time = curr_time + task['bt']
        execution_log.append((index, start_time, end_time))  # (task_index, start, end)
        curr_time = end_time
        task['ct'] = curr_time
        print(f"Executing Task {task['id']} from {start_time} to {end_time}")

    return data, execution_log


def round_robin(data, tq):
    """
    Round Robin (RR) scheduling algorithm.

    :param data: List of task dictionaries.
    :param tq: Time quantum.
    :return: Tuple of (updated data, execution_log).
    """
    rr = []
    indx = 0
    curr_time = 0
    completed = 0  # The number of tasks completed
    n = len(data)
    execution_log = []  # Records a list of task execution fragments (task_index, start_time, end_time)

    # Initialize the task list and add the remaining execution time
    for task in data:
        rr.append({
            'id': task['id'],
            'at': task['at'],
            'bt': task['bt'],
            'remaining_bt': task['bt'],
            'index': indx
        })
        indx += 1

    # Sort tasks by arrival time
    rr.sort(key=lambda x: x['at'])

    queue = []
    i = 0  # Track the index of tasks added to the queue

    while completed < n:
        # Add all tasks that have arrived at the current time to the queue
        while i < n and rr[i]['at'] <= curr_time:
            queue.append(rr[i])
            print(f"Task {rr[i]['id']} arrived at {rr[i]['at']} and joined the queue.")
            i += 1

        if queue:
            # Fetch the first task in the queue
            current_task = queue.pop(0)
            exec_time = min(tq, current_task['remaining_bt'])

            # Record execution segment
            execution_log.append((current_task['index'], curr_time, curr_time + exec_time))  # (task_index, start, end)

            # Print execution information
            start_time = curr_time
            curr_time += exec_time
            current_task['remaining_bt'] -= exec_time
            print(
                f"Executing Task {current_task['id']} from {start_time} to {curr_time}, Remaining time {current_task['remaining_bt']}")

            # Add any new tasks that have arrived during execution
            while i < n and rr[i]['at'] <= curr_time:
                queue.append(rr[i])
                print(f"Task {rr[i]['id']} arrived at {rr[i]['at']} and joined the queue.")
                i += 1

            if current_task['remaining_bt'] > 0:
                # If the task is not completed, rejoin the end of the queue
                queue.append(current_task)
            else:
                # The task is complete. Set the completion time
                data[current_task['index']]['ct'] = curr_time
                print(f"Task {current_task['id']} completed at {curr_time}")
                completed += 1
        else:
            # If the queue is empty, jump to the arrival time of the next task
            if i < n:
                print(f"The queue is empty. Jumping from {curr_time} to {rr[i]['at']}")
                curr_time = rr[i]['at']
            else:
                break  # All tasks have been processed

    return data, execution_log


def shortest_job_first(data):
    """
    Shortest Job First (SJF) scheduling algorithm.

    :param data: List of task dictionaries.
    :return: Tuple of (updated data, execution_log).
    """
    # Initialize task data
    sjf = []
    indx = 0
    for dct in data:
        sjf.append([dct['bt'], dct['at'], indx])  # [Burst Time, Arrival Time, Index]
        indx += 1

    sjf.sort(key=lambda x: x[1])  # Sort by arrival time
    curr_time = 0
    completed = []
    execution_log = []

    while len(completed) < len(data):
        # Find all arrived and unfinished tasks
        available = [task for task in sjf if task[1] <= curr_time and task not in completed]

        if available:
            # Sort by burst time (shortest job first)
            available.sort(key=lambda x: x[0])
            next_task = available[0]

            # Record the start and end time of the task
            start_time = curr_time
            end_time = curr_time + next_task[0]
            execution_log.append((next_task[2], start_time, end_time))  # (task_index, start, end)

            # Perform the task
            curr_time += next_task[0]  # Increase current time
            data[next_task[2]]['ct'] = curr_time  # Set completion time
            completed.append(next_task)  # Mark the task as completed
            print(f"Executing Task {data[next_task[2]]['id']} with completion time {curr_time}")
        else:
            # If no task is available, skip to the arrival time of the next task
            next_arrival = min(task[1] for task in sjf if task not in completed)
            print(f"Current time {curr_time} - No task available. Skipping to time {next_arrival}")
            curr_time = next_arrival

    return data, execution_log


def priority_non_preemptive(data):
    """
    Priority Non-Preemptive scheduling algorithm.

    :param data: List of task dictionaries.
    :return: Tuple of (updated data, execution_log).
    """
    curr_time = 0
    completed = []
    n = len(data)
    execution_log = []

    # Transform task data and add priority
    tasks = [[task['pr'], task['at'], task['bt'], i] for i, task in enumerate(data)]
    tasks.sort(key=lambda x: x[1])  # Sort by arrival time

    while len(completed) < n:
        # Find all arrived and unfinished tasks
        available_tasks = [task for task in tasks if task[1] <= curr_time and task not in completed]

        if available_tasks:
            # Sort by priority (lower number = higher priority) and arrival time
            available_tasks.sort(key=lambda x: (x[0], x[1]))
            next_task = available_tasks[0]

            # Record the start and end time of the task
            start_time = curr_time
            end_time = curr_time + next_task[2]
            execution_log.append((next_task[3], start_time, end_time))  # (task_index, start, end)

            # Perform the task
            curr_time += next_task[2]  # Increase current time
            data[next_task[3]]['ct'] = curr_time  # Set completion time
            completed.append(next_task)  # Mark the task as completed
            print(f"Executing Task {data[next_task[3]]['id']} with completion time {curr_time}")
        else:
            # If no task is available, skip to the arrival time of the next task
            next_arrival = min(task[1] for task in tasks if task not in completed)
            print(f"Current time {curr_time} - No task available. Skipping to time {next_arrival}")
            curr_time = next_arrival

    return data, execution_log


def priority_preemptive(data):
    """
    Priority Preemptive scheduling algorithm.

    :param data: List of task dictionaries.
    :return: Tuple of (updated data, execution_log).
    """

    def find_highest_priority_task(curr_time, tasks):
        # Find all arrived and unfinished tasks
        available_tasks = [task for task in tasks if task[1] <= curr_time and task[2] > 0]
        if not available_tasks:
            return None  # No task to execute
        # Sort by priority (lower number = higher priority) and arrival time
        available_tasks.sort(key=lambda x: (x[0], x[1]))
        return available_tasks[0]

    curr_time = 0
    completed = 0  # The number of tasks completed
    n = len(data)
    execution_log = []
    tasks = [[task['pr'], task['at'], task['bt'], i] for i, task in enumerate(data)]  # [PR, AT, BT, Index]

    while completed < n:
        task = find_highest_priority_task(curr_time, tasks)
        if task:
            # Execute the highest priority task for 1 unit time
            task[2] -= 1  # Reduce remaining execution time
            start_time = curr_time
            curr_time += 1
            execution_log.append((task[3], start_time, curr_time))  # (task_index, start, end)
            print(f"Executing Task {data[task[3]]['id']} from {start_time} to {curr_time}, Remaining time {task[2]}")
            if task[2] == 0:  # If the task is completed
                data[task[3]]['ct'] = curr_time  # Set completion time
                completed += 1
                print(f"Task {data[task[3]]['id']} completed at {curr_time}")
        else:
            # No task to execute, increment time
            print(f"Current time {curr_time} - No task to execute. Incrementing time.")
            curr_time += 1

    return data, execution_log
