import tkinter as tk
from tkinter import ttk
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

from BACKEND import simulation
from GRAPHS import GIA, GST

def run_simulation(time, servers, diss1, diss2, wind):
    total_time = int(time.get())
    Inter_Arrival_Distribution = diss1.get()
    Service_Time_Distribution = diss2.get()
    num_servers = int(servers.get())

    result = simulation(SIM_TIME=total_time, n_servers=num_servers, IAdist=Inter_Arrival_Distribution,
                        STdist=Service_Time_Distribution)

    result[0].pop(0)
    result[1].pop(0)
    result[2].pop(0)
    result[3].pop(0)
    result[4].pop(0)
    result[5].pop(0)
    result[6].pop(0)
    result[7].pop(0)
    result[8].pop(0)

    arrivals = result[0]
    InterArrival = result[1]
    service_times = result[2]
    Start = result[3]
    End = result[4]
    TAT = result[5]
    WaitTime = result[6]
    IdleTime = result[7]
    ResponseTime = result[8]

    submit_button_clicked(Inter_Arrival_Distribution, Service_Time_Distribution, wind, arrivals, InterArrival, service_times, Start, End, TAT, WaitTime, IdleTime, ResponseTime)

    df = pd.DataFrame(result).T
    df.to_excel('Simulation_Result.xlsx')


def open_new_window():
    # Destroy the current window
    window.destroy()

    # Create new window
    new_window = tk.Tk()
    new_window.title("Simulation App")

    # Get screen dimensions
    screen_width = new_window.winfo_screenwidth()
    screen_height = new_window.winfo_screenheight()

    # Calculate application dimensions and position
    app_width = int(screen_width * 0.8)
    app_height = int(screen_height * 0.8)
    app_x = int((screen_width - app_width) / 2)
    app_y = int((screen_height - app_height) / 2)

    # Set window geometry
    new_window.geometry(f"{app_width}x{app_height}+{app_x}+{app_y}")

    # Set window background and foreground colors
    new_window.configure(background='#222222')

    # Create label and text box for first input
    input1_label = tk.Label(new_window, text="Total Time:", font=("Arial", 16), fg="white", bg="#222222", anchor="w")
    input1_label.pack(pady=10, padx=20)

    input1_textbox = tk.Entry(new_window, font=("Arial", 16), bg="white", fg="#222222", justify="center")
    input1_textbox.pack(pady=10, padx=20)

    # Create label and text box for second input
    input2_label = tk.Label(new_window, text="Number of Servers:", font=("Arial", 16), fg="white", bg="#222222", anchor="w")
    input2_label.pack(pady=10, padx=20)

    input2_textbox = tk.Entry(new_window, font=("Arial", 16), bg="white", fg="#222222", justify="center")
    input2_textbox.pack(pady=10, padx=20)

    # Create dropdown widget
    IAdistributions = ['Exponential', 'Normal', 'Uniform', 'Gamma']
    dropdown_label = tk.Label(new_window, text="Inter Arrival Distribution:", font=("Arial", 16), fg="white", bg="#222222",
                              anchor="w")
    dropdown_label.pack(pady=10, padx=20)

    dropdown = ttk.Combobox(new_window, values=IAdistributions, font=("Arial", 16), justify="center")
    dropdown.pack(pady=10, padx=20)

    # Create another dropdown widget
    STdistributions = ['Exponential', 'Normal', 'Uniform', 'Gamma']
    dropdown_label2 = tk.Label(new_window, text="Service Time Distribution:", font=("Arial", 16), fg="white", bg="#222222",
                               anchor="w")
    dropdown_label2.pack(pady=10, padx=20)

    dropdown2 = ttk.Combobox(new_window, values=STdistributions, font=("Arial", 16), justify="center")
    dropdown2.pack(pady=10, padx=20)

    # Create submit button
    submit_button = tk.Button(new_window, text="Submit", font=("Arial", 16), bg="white", fg="#222222", padx=20, pady=10,
                              command=lambda: [run_simulation(input1_textbox, input2_textbox, dropdown, dropdown2, new_window)])
    submit_button.pack(pady=10)

    # Run the main loop
    new_window.mainloop()

def submit_button_clicked(IAdist, STdist, current_window, arrivals, InterArrival, service_times, Start, End, TAT, WaitTime, IdleTime, ResponseTime):

    # lamb_ = 1 / (sum(InterArrival) / len(InterArrival))
    # mu_ = 1 / (sum(service_times) / len(service_times))
    #
    # S_bar_or_L = lamb_ / (mu_ - lamb_)
    # q_bar = S_bar_or_L - (lamb_ / mu_)
    # w_bar = S_bar_or_L * (1 / mu_)
    # t_bar = w_bar + (1 / mu_)
    # p_0_ = 1 - (lamb_ / mu_)
    # P = (lamb_ / mu_)
    # q_bar_2 = mu_ / (mu_ - lamb_)

    TotalInterArrivalTime = sum(InterArrival)
    TotalServiceTime = sum(service_times)
    TotalTAT = sum(TAT)
    TotalWaitTime = sum(WaitTime)
    TotalResponseTime = sum(ResponseTime)
    Total_cust = len(arrivals)
    Total_num_of_waiting_cus = np.count_nonzero(WaitTime)
    Total_idle_time = sum(IdleTime)

    Avg_Wait_Time = TotalWaitTime / Total_cust
    Probability_that_a_cust_has_to_wait = Total_num_of_waiting_cus / Total_cust
    Proportion_of_Idle_time_by_server = (Total_idle_time / TotalServiceTime) * 100
    Utilization = 100 - Proportion_of_Idle_time_by_server
    Avg_Wait_time_for_waiting_customers = TotalWaitTime / Total_num_of_waiting_cus
    Avg_time_cust_spend_in_system = TotalTAT / Total_cust
    Avg_InterArrival_time = TotalInterArrivalTime / Total_cust
    Avg_service_time = TotalServiceTime / Total_cust

    # Destroy the current window
    current_window.destroy()

    # Open a new window
    window = tk.Tk()
    window.title("Simulation App")

    # Get screen dimensions
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Calculate application dimensions and position
    app_width = int(screen_width * 0.8)
    app_height = int(screen_height * 0.8)
    app_x = int((screen_width - app_width) / 2)
    app_y = int((screen_height - app_height) / 2)

    # Set window geometry
    window.geometry(f"{app_width}x{app_height}+{app_x}+{app_y}")

    # Set window background and foreground colors
    # window.configure(background='#222222')

    # Add a heading before displaying the output
    heading_label = tk.Label(window, text="Performance Measures", font=("Arial", 24))
    heading_label.pack(pady=10)

    # Add a text widget to display the output
    output_text = tk.Text(window, font=("Arial", 18))
    output_text.pack(fill=tk.BOTH, expand=True)

    # Redirect print statements to the text widget
    def write_output(text):
        output_text.insert(tk.END, text + "\n\n")

    printer = write_output

    # Print some output
    # printer(f'Avg_no_in_the_system : {S_bar_or_L}')
    # printer(f'Avg_no_in_the_queue : {q_bar}')
    # printer(f'Avg_wait_time : {w_bar}')
    # printer(f'Avg_time_in_system : {t_bar}')
    # printer(f'probability_of_no_customer_in_the_system : {p_0_}')
    # printer(f'util_factor: {P}')
    # printer(f'Avg_no_in_the_queue(when queue is not empty) : {q_bar_2}')
    printer(f'Average Wait Time : {Avg_Wait_Time}')
    printer(f'Probability that a customer has to wait : {Probability_that_a_cust_has_to_wait}')
    printer(f'Proportion of Idle time by server : {Proportion_of_Idle_time_by_server}')
    printer(f'Utilization of server : {Utilization}')
    printer(f'Average Wait Time for Waiting Customers: {Avg_Wait_time_for_waiting_customers}')
    printer(f'Average time customer spent in system : {Avg_time_cust_spend_in_system}')
    printer(f'Average InterArrival time : {Avg_InterArrival_time}')
    printer(f'Average Service time : {Avg_service_time}')

    # Add two buttons to the window
    button1 = tk.Button(window, text="Graph of InterArrivals", font=("Arial", 16), bg="#333333", fg="white", padx=20, pady=10, command=lambda: [plt.close(), GIA(IAdist, InterArrival)])
    button1.pack(pady=10)

    button2 = tk.Button(window, text="Graph of Service Time", font=("Arial", 16), bg="#333333", fg="white", padx=20, pady=10, command=lambda: [plt.close(), GST(STdist, service_times)])
    button2.pack(pady=10)

    # Start the main event loop
    window.mainloop()


# Create main window
window = tk.Tk()
window.title("Simulation App")

# Get screen dimensions
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Calculate application dimensions and position
app_width = int(screen_width * 0.8)
app_height = int(screen_height * 0.8)
app_x = int((screen_width - app_width) / 2)
app_y = int((screen_height - app_height) / 2)

# Set window geometry
window.geometry(f"{app_width}x{app_height}+{app_x}+{app_y}")

# Set window background and foreground colors
window.configure(background='#222222')

# Create welcome message label
welcome_msg = tk.Label(window, text="Welcome to the Simulation App!", font=("Arial", 36, "bold"), fg="white", bg="#222222")
welcome_msg.pack(pady=40)

# Create a subtitle label in the main frame
subtitle_label = tk.Label(window, text="This app lets you simulate various scenarios and explore their outcomes.",
                               bg="#222222", fg="white", font=("Arial", 20))
subtitle_label.pack(pady=20)

# Create a description label in the main frame
desc_label = tk.Label(window, text="With Simulation App, you can visualize and analyze different situations using computer models that simulate real-world events. You can customize various parameters to see how they affect the outcome, and use the data to make informed decisions.",
                           bg="#222222", fg="white", font=("Arial", 16), wraplength=800)
desc_label.pack(pady=40)

# Create start button
start_button = tk.Button(window, text="Start Simulation", font=("Arial", 20, "bold"), bg="white", fg="#222222", padx=20, pady=10, command=open_new_window)
start_button.pack(pady=20)

# Create a Group description label in the main frame
Group_label = tk.Label(window, text="Group Members : \n Muhammad Humza EB19103063 \n Muhammad Shehryar Siddiqui EB19103080 \n Shabib Ahmed EB19103108 \n Muhammad Uzair Khan EB19103086",
                       bg="#222222", fg="white", font=("Arial", 16, "bold"))
Group_label.pack(pady=40)

# Create a Instructor description label in the main frame
Instructor_label = tk.Label(window, text="Course & Project Instructor : Ma'am Shaista Rais",
                       bg="#222222", fg="white", font=("Arial", 17, "bold"))
Instructor_label.pack(pady=40)

# Run the main loop
window.mainloop()


# # Create a title label in the main frame
#         self.title_label = tk.Label(master, text="Welcome to the Simulation App!", bg="#2b2b2b", fg="white",
#                                     font=("Arial", 36, "bold"))
#         self.title_label.pack(pady=40)
#
#
#
#
#
#         # Create a start button in the main frame
#         self.start_button = tk.Button(master, text="Start Simulation", bg="#80c1ff", fg="white",
#                                       font=("Arial", 20, "bold"), padx=20, pady=10, command=self.start_simulation)
#         self.start_button.pack(pady=20)


