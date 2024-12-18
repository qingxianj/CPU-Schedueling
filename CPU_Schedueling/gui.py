# gui.py

import tkinter as tk
from tkinter import ttk, messagebox
from algorithm import (first_come_first_serve, round_robin, shortest_job_first,
                      priority_non_preemptive, priority_preemptive, avg_wt_tat)
import copy
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm


class TaskSchedulerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Scheduler GUI")
        self.root.geometry("1200x700")  # Increased window size to accommodate Gantt chart

        self.tasks = []
        self.selected_algorithm = tk.StringVar()
        self.time_quantum = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        # Dropdown to select algorithm
        algorithms = [
            "First Come First Serve",
            "Round Robin",
            "Shortest Job First",
            "Priority Non-Preemptive",
            "Priority Preemptive"
        ]
        ttk.Label(self.root, text="Select Algorithm:").grid(row=0, column=0, padx=10, pady=10, sticky='W')
        self.algorithm_menu = ttk.Combobox(self.root, values=algorithms, textvariable=self.selected_algorithm, state='readonly')
        self.algorithm_menu.grid(row=0, column=1, padx=10, pady=10, sticky='W')

        # Time Quantum for Round Robin
        ttk.Label(self.root, text="Time Quantum (for Round Robin):").grid(row=1, column=0, padx=10, pady=10, sticky='W')
        self.time_quantum_entry = ttk.Entry(self.root, textvariable=self.time_quantum)
        self.time_quantum_entry.grid(row=1, column=1, padx=10, pady=10, sticky='W')

        # Task input fields
        ttk.Label(self.root, text="Task ID:").grid(row=2, column=0, padx=10, pady=10, sticky='W')
        self.task_id = tk.StringVar()
        self.task_id_entry = ttk.Entry(self.root, textvariable=self.task_id)
        self.task_id_entry.grid(row=2, column=1, padx=10, pady=10, sticky='W')

        ttk.Label(self.root, text="Arrival Time:").grid(row=3, column=0, padx=10, pady=10, sticky='W')
        self.arrival_time = tk.StringVar()
        self.arrival_time_entry = ttk.Entry(self.root, textvariable=self.arrival_time)
        self.arrival_time_entry.grid(row=3, column=1, padx=10, pady=10, sticky='W')

        ttk.Label(self.root, text="Burst Time:").grid(row=4, column=0, padx=10, pady=10, sticky='W')
        self.burst_time = tk.StringVar()
        self.burst_time_entry = ttk.Entry(self.root, textvariable=self.burst_time)
        self.burst_time_entry.grid(row=4, column=1, padx=10, pady=10, sticky='W')

        ttk.Label(self.root, text="Priority (lower number = higher priority):").grid(row=5, column=0, padx=10, pady=10, sticky='W')
        self.priority = tk.StringVar()
        self.priority_entry = ttk.Entry(self.root, textvariable=self.priority)
        self.priority_entry.grid(row=5, column=1, padx=10, pady=10, sticky='W')

        # Add Task Button
        self.add_task_button = ttk.Button(self.root, text="Add Task", command=self.add_task)
        self.add_task_button.grid(row=6, column=0, padx=10, pady=10, sticky='W')

        # Delete Task Button
        self.delete_task_button = ttk.Button(self.root, text="Delete Selected Task", command=self.delete_task)
        self.delete_task_button.grid(row=6, column=1, padx=10, pady=10, sticky='W')

        # Task Table
        columns = ("Task ID", "Arrival Time", "Burst Time", "Priority")
        self.task_table = ttk.Treeview(self.root, columns=columns, show="headings", height=10)
        for col in columns:
            self.task_table.heading(col, text=col)
        self.task_table.grid(row=7, column=0, columnspan=2, padx=10, pady=10)

        # Run Algorithm Button
        self.run_button = ttk.Button(self.root, text="Run Algorithm", command=self.run_algorithm)
        self.run_button.grid(row=8, column=0, padx=10, pady=10, sticky='W')

        # Output Area
        self.output_text = tk.Text(self.root, height=25, width=80)
        self.output_text.grid(row=7, column=2, rowspan=4, padx=10, pady=10)

    def add_task(self):
        """
        Add a new task to the task list after validating inputs.
        Ensures that Task ID is unique.
        """
        task_id = self.task_id.get()
        arrival_time = self.arrival_time.get()
        burst_time = self.burst_time.get()
        priority = self.priority.get()

        # Check if Task ID is unique
        if any(task['id'] == task_id for task in self.tasks):
            messagebox.showerror("Input Error", f"Task ID '{task_id}' already exists. Please use a unique Task ID.")
            return

        if task_id and arrival_time.isdigit() and burst_time.isdigit() and priority.isdigit():
            task = {
                'id': task_id,
                'at': int(arrival_time),
                'bt': int(burst_time),
                'pr': int(priority)
            }
            self.tasks.append(task)
            self.update_task_table()
            self.clear_input_fields()
        else:
            messagebox.showerror("Input Error", "Please enter valid Task ID, Arrival Time, Burst Time, and Priority.")

    def delete_task(self):
        """
        Delete the selected task from the task list.
        """
        selected_item = self.task_table.selection()
        if selected_item:
            task_index = self.task_table.index(selected_item[0])
            del self.tasks[task_index]
            self.update_task_table()
        else:
            messagebox.showerror("Selection Error", "Please select a task to delete.")

    def update_task_table(self):
        """
        Refresh the task table to display the current list of tasks.
        """
        # Clear existing entries
        for item in self.task_table.get_children():
            self.task_table.delete(item)
        # Insert all tasks
        for task in self.tasks:
            self.task_table.insert("", "end", values=(task['id'], task['at'], task['bt'], task['pr']))

    def clear_input_fields(self):
        """
        Clear the input fields after adding a task.
        """
        self.task_id.set("")
        self.arrival_time.set("")
        self.burst_time.set("")
        self.priority.set("")

    def run_algorithm(self):
        """
        Execute the selected scheduling algorithm and display the results.
        """
        algorithm = self.selected_algorithm.get()
        if not algorithm:
            messagebox.showerror("Selection Error", "Please select an algorithm.")
            return

        data_copy = copy.deepcopy(self.tasks)

        result, order_or_log = None, None
        if algorithm == "First Come First Serve":
            result, order_or_log = first_come_first_serve(data_copy)
        elif algorithm == "Round Robin":
            tq = self.time_quantum.get()
            if not tq.isdigit():
                messagebox.showerror("Input Error", "Please enter a valid Time Quantum for Round Robin.")
                return
            result, order_or_log = round_robin(data_copy, int(tq))
        elif algorithm == "Shortest Job First":
            result, order_or_log = shortest_job_first(data_copy)
        elif algorithm == "Priority Non-Preemptive":
            result, order_or_log = priority_non_preemptive(data_copy)
        elif algorithm == "Priority Preemptive":
            result, order_or_log = priority_preemptive(data_copy)
        else:
            messagebox.showerror("Selection Error", "Invalid algorithm selected.")
            return

        if result is not None:
            # Ensure all tasks have completion time
            missing_ct = [task for task in result if 'ct' not in task]
            if missing_ct:
                messagebox.showerror("Algorithm Error", "Some tasks did not complete. 'ct' not set for all tasks.")
                return

            avg_times = avg_wt_tat(result)

            if algorithm == "Round Robin":
                # For RR, order_or_log is execution_log
                # Format execution order as list of strings
                execution_order = [f"P{exec[0]}" for exec in order_or_log]
                self.display_output(result, avg_times, execution_order)
                # Generate Gantt chart using execution_log
                plot_gantt_chart(order_or_log, result)
            else:
                # For other algorithms, order_or_log is execution_log
                print("Execution Log:", order_or_log)  # Debugging statement
                try:
                    # Attempt to access by task_index
                    execution_order = [f"P{result[exec[0]]['id']}" for exec in order_or_log]
                except TypeError:
                    # If exec[0] is not integer, handle accordingly
                    execution_order = [f"P{exec[0]}" for exec in order_or_log]
                self.display_output(result, avg_times, execution_order)
                # Generate Gantt chart
                plot_gantt_chart(order_or_log, result)

    def display_output(self, result, avg_times, order):
        """
        Display the scheduling results and average times in the output text area.

        :param result: List of task dictionaries with updated times.
        :param avg_times: Dictionary with average TAT and WT.
        :param order: List representing the execution order of tasks.
        """
        self.output_text.delete("1.0", tk.END)
        for task in result:
            self.output_text.insert(
                tk.END, f"Task {task['id']}: CT={task['ct']}, TAT={task['tat']}, WT={task['wt']}\n"
            )
        self.output_text.insert(tk.END, f"\nAverage TAT: {avg_times['avg_tat']:.2f}\n")
        self.output_text.insert(tk.END, f"Average WT: {avg_times['avg_wt']:.2f}\n")
        if isinstance(order, list):
            # If order is execution_log, extract task execution order
            if all(isinstance(item, tuple) and len(item) == 3 for item in order):
                # Try to get task IDs from task_index
                try:
                    execution_order = [f"P{result[exec[0]]['id']}" for exec in order]
                except TypeError:
                    # If exec[0] is not integer, assume it's task_id
                    execution_order = [f"P{exec[0]}" for exec in order]
                self.output_text.insert(tk.END, f"\nExecution Order: {' -> '.join(execution_order)}\n")
            else:
                self.output_text.insert(tk.END, f"\nExecution Order: {' -> '.join(order)}\n")


def plot_gantt_chart(execution_log, task_details):
    """
    Plot Gantt chart based on execution_log and task_details.

    :param execution_log: List of tuples (task_index, start_time, end_time)
    :param task_details: List of task dictionaries
    """
    if not execution_log:
        print("Execution log is empty. No Gantt chart to display.")
        return

    # Set Chinese font path (adjust the path as per your system)
    font_path = 'C:/Windows/Fonts/simhei.ttf'  # Windows path for SimHei font
    try:
        font_prop = fm.FontProperties(fname=font_path)
    except FileNotFoundError:
        print(f"Font file not found: {font_path}")
        print("Please ensure the path is correct or use another Chinese-supporting font.")
        return

    fig, ax = plt.subplots(figsize=(12, 6))  # Increased figure size

    for exec in execution_log:
        task_index, start_time, end_time = exec
        # According to task_index, get task ID
        task_id = task_details[task_index]['id']
        task_label = f"P{task_id}"
        ax.barh(task_label, width=(end_time - start_time), left=start_time, height=0.4, color='skyblue', edgecolor='black')
        ax.text(start_time + (end_time - start_time)/2, task_label, task_label, ha='center', va='center', color='black', fontproperties=font_prop)

    # Customize the chart
    ax.set_xlabel("Time", fontproperties=font_prop)
    ax.set_ylabel("Tasks", fontproperties=font_prop)
    ax.set_title("Gantt Chart", fontproperties=font_prop)
    ax.grid(axis='x', linestyle='--', alpha=0.7)

    # Set y-axis task labels
    task_ids = sorted(list(set([f"P{task['id']}" for task in task_details])), key=lambda x: int(x[1:]))
    ax.set_yticks(range(len(task_ids)))
    ax.set_yticklabels(task_ids, fontproperties=font_prop)

    plt.tight_layout()
    plt.show()  # Keeps the window open


if __name__ == "__main__":
    root = tk.Tk()
    app = TaskSchedulerGUI(root)
    root.mainloop()
