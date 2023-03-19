import numpy as np
import pandas as pd
import simpy
import matplotlib.pyplot as plt
from GRAPHS import GIA, GST
from DATA import lambda_, meu, IASTD, STSTD, IAalpha, IAbeta, STalpha, STbeta, IAlower, IAupper, STlower, STupper
import math
import ciw

arrivals = []  # interarrival time between consecutive customers
arrivalscopy = []  # interarrival time between consecutive customers
service_times = []  # service time for each customer
InterArrival = []
Start = []
End = []
TAT = []
WaitTime = []
IdleTime = []
ResponseTime = []
AtServer = []

def simulation(SIM_TIME, n_servers, IAdist, STdist):
    # create environment and store results
    env = simpy.Environment()
    # create customer generator
    def customer_generator(env, lambd):
        # global arrivals, service_times
        i = 0
        while True:
            i += 1
            if IAdist == 'Exponential':
                yield env.timeout(math.floor(np.random.exponential(1 / lambd)))
            elif IAdist == 'Normal':
                var = np.random.normal(1/lambd, IASTD)
                while var < 0:
                    var = np.random.normal(1/lambd, IASTD)
                yield env.timeout(math.floor(var))
            elif IAdist == 'Uniform':
                yield env.timeout(math.floor(np.random.uniform(low=IAlower, high=IAupper)))
            elif IAdist == 'Poisson':
                yield env.timeout(math.floor(np.random.poisson(lam=lambd)))
            elif IAdist == 'Gamma':
                yield env.timeout(math.ceil(np.random.gamma(shape=IAalpha, scale=IAbeta)))
            arrivals.append(env.now)
            env.process(customer(env, i))

    # create customer process
    def customer(env, i):
        # global service_times, arrivals
        # arrival_time = np.random.exponential(1/ARRIVAL_RATE)
        arrival_time = env.now
        with server.request() as req:
            yield req
            service_start_time = env.now
            Start.append(service_start_time)
            if STdist == 'Exponential':
                service_time = math.ceil(np.random.exponential(1 / meu))
            elif STdist == 'Normal':
                var = np.random.normal(1 / meu, STSTD)
                while var < 0:
                    var = np.random.normal(1 / meu, STSTD)
                service_time = math.ceil(var)
            elif STdist == 'Uniform':
                service_time = math.ceil(np.random.uniform(low=STlower, high=STupper))
            elif STdist == 'Gamma':
                service_time = math.ceil(np.random.gamma(shape=STalpha, scale=STbeta))
            service_times.append(service_time)
            yield env.timeout(service_time)
            service_end_time = math.floor(env.now)
            End.append(service_end_time)

    # run simulation
    # np.random.seed(SEED)
    server = simpy.Resource(env, capacity=n_servers)
    env.process(customer_generator(env, lambda_))
    env.run(until=abs(SIM_TIME * 10))

    print(arrivals)

    interarrival_times = np.diff([0] + arrivals)
    InterArrival = interarrival_times.tolist()
    InterArrival[0] = 0

    for x in range(len(End)):
        TAT.append(End[x] - arrivals[x])
        varwait = TAT[x] - service_times[x]
        if varwait < 0:
            IdleTime.append(abs(varwait))
            WaitTime.append(0)
        else:
            WaitTime.append(varwait)
            IdleTime.append(0)
        ResponseTime.append(Start[x] - arrivals[x])

    # lamb_ = 1 / (sum(InterArrival) / len(InterArrival))
    # mu_ = 1 / (sum(service_times) / len(service_times))

    # ################################ Parallel Universe ##########################
    # ### Avg_no_in_the_system ###
    # print(f"Lambda: {lambda_}")
    # print(f"Meu: {mu_}")
    # S_bar_or_L = lamb_ / mu_ - lamb_
    # print(f'Avg_no_in_the_system : {S_bar_or_L}')
    # ### Avg_no_in_the_queue ###
    # q_bar = S_bar_or_L - lamb_ / mu_
    # print(f'Avg_no_in_the_queue : {q_bar}')
    # ### Avg_wait_time ###
    # w_bar = S_bar_or_L * 1 / mu_
    # print(f'Avg_wait_time : {w_bar}')
    # ### Avg_time_in_system ###
    # t_bar = w_bar + 1 / mu_
    # print(f'Avg_time_in_system : {t_bar}')
    # ### probability_of_no_customer_in_the_system ###
    # p_0_ = 1 - lamb_ / mu_
    # print(f'probability_of_no_customer_in_the_system : {p_0_}')
    # ### util_factor ###
    # P = lamb_ / mu_
    # print(f'util_factor: {P}')
    # ### Avg_no_in_the_queue(when queue is not empty) ###
    # q_bar_2 = mu_ / mu_ - lamb_
    # print(f'Avg_no_in_the_queue(when queue is not empty) : {q_bar_2}')

    # summation
    # Arrival.append("TOTAL : ")
    TotalInterArrivalTime = sum(InterArrival)
    # print(f'Total InterArrival Time : {TotalInterArrivalTime}')
    TotalServiceTime = sum(service_times)
    # print(f'Total Service Time : {TotalServiceTime}')
    # ServiceTime.append(TotalServiceTime)
    TotalTAT = sum(TAT)
    # print(f'Total Turnaround Time : {TotalTAT}')
    # TAT.append(TotalTAT)
    TotalWaitTime = sum(WaitTime)
    # print(f'Total Wait Time : {TotalWaitTime}')
    # WaitTime.append(TotalWaitTime)
    TotalResponseTime = sum(ResponseTime)
    # print(f'Total Response Time : {TotalResponseTime}')
    # ResponseTime.append(TotalResponseTime)
    Total_cust = len(arrivals)
    Total_num_of_waiting_cus = np.count_nonzero(WaitTime)
    Total_idle_time = sum(IdleTime)

    # Performance Measures
    Avg_Wait_Time = TotalWaitTime / Total_cust
    print(f'Average Wait Time : {Avg_Wait_Time}')
    Probability_that_a_cust_has_to_wait = Total_num_of_waiting_cus / Total_cust
    print(f'Probability that a customer has to wait : {Probability_that_a_cust_has_to_wait}')
    Proportion_of_Idle_time_by_server = (Total_idle_time / TotalServiceTime) * 100
    print(f'Proportion of Idle time by server : {Proportion_of_Idle_time_by_server}')
    Utilization = 100 - Proportion_of_Idle_time_by_server
    print(f'Utilization of server : {Utilization}')
    # Avg_time_between_arrivals = ?????
    Avg_Wait_time_for_waiting_customers = TotalWaitTime / Total_num_of_waiting_cus
    print(f'Average Wait Time for Waiting Customers: {Avg_Wait_time_for_waiting_customers}')
    Avg_time_cust_spend_in_system = TotalTAT / Total_cust
    print(f'Average time customer spent in system : {Avg_time_cust_spend_in_system}')
    Avg_InterArrival_time = TotalInterArrivalTime / Total_cust
    print(f'Average InterArrival time : {Avg_InterArrival_time}')
    Avg_service_time = TotalServiceTime / Total_cust
    print(f'Average Service time : {Avg_service_time}')

    performance_measures = ["Performance Measures",
                            f"Total Inter Arrival Time : {TotalInterArrivalTime}",
                            f"Total Service Time : {TotalServiceTime}",
                            f"Total Turnaround Time : {TotalTAT}",
                            f"Total Wait Time : {TotalWaitTime}",
                            f"Total Response Time : {TotalResponseTime}",
                            f"Total Customers : {Total_cust}",
                            f"Total number of waiting customers : {Total_num_of_waiting_cus}",
                            f"Total Idle Time : {Total_idle_time}",
                            f"Average Wait Time : {Avg_Wait_Time}",
                            f"Probability that a customer has to wait : {Probability_that_a_cust_has_to_wait}",
                            f"Proportion of Idle time by server : {Proportion_of_Idle_time_by_server}",
                            f"Utilization of server : {Utilization}",
                            f"Average Wait Time for Waiting Customers: {Avg_Wait_time_for_waiting_customers}",
                            f"Average time customer spent in system : {Avg_time_cust_spend_in_system}",
                            f"Average Service time : {Avg_service_time}",
                            f"Average InterArrival time : {Avg_InterArrival_time}"
                            ]

    # GIA(IAdist, InterArrival)
    # GST(STdist, service_times)

    arrivals.insert(0, 'Arrival Time')
    InterArrival.insert(0, 'InterArrival Time')
    service_times.insert(0, 'Service Time')
    Start.insert(0, "Start")
    End.insert(0, "End")
    TAT.insert(0, "TAT")
    WaitTime.insert(0, "WaitTime")
    IdleTime.insert(0, "IdleTime")
    ResponseTime.insert(0, "Response Time")

    results = [arrivals, InterArrival, service_times, Start, End, TAT, WaitTime, IdleTime, ResponseTime]
    # df = pd.DataFrame(results).T
    # df.to_excel('Simulation_Result.xlsx')
    return results

# simulation(3000, 1, 'Gamma', 'Gamma')

