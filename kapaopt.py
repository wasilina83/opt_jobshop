import json as js
from collections import defaultdict
from optionsgenerator import dev_options_form_parts
import itertools

class Job :
    def __init__(self, operation, part, quantity, production_time, equip_time):
        self.operation = operation
        self.part = part
        self.quantity = quantity
        self.production_time = production_time
        self.equip_time = equip_time
        
    def __str__(self):
        return f"operation: {self.operation}, part: {self.part}, quantity: {self.quantity}, production_time: {self.production_time}, equip_time: {self.equip_time}"
    
    def __repr__(self):
        return str(self)


class Maschine_Schedule :
    def __init__(self, operation, schedule_list):
        self.operation = operation
        self.schedule_list = schedule_list

    def __str__(self):
        return f"operation: {self.operation}, schedule_list: {self.schedule_list}"
    
    def __repr__(self):
        return str(self)



def get_job_data_form_json(filename):
    with open(filename) as file:
        job_dict = defaultdict(list)
        data = js.load(file) 
        for part, quantity in data["manufacturing_needs"].items():
            for operation, production_time in data["production_time"][part].items():
                equip_time = data["equip_time"][operation]
                #machine_time = quantity * production_time * batch_size + equip_time
                job = Job(operation, part, quantity, production_time, equip_time)
                job_dict[job.operation].append(job)
    return job_dict    
        

def get_batch_size():
    with open("data.json") as file:
        data = js.load(file)
        batch_sizes = data["batch_sizes"]
        return batch_sizes


def get_max_time():
    with open("data.json") as file:
        data = js.load(file)
        max_time = data["workload_maximum"]
        return max_time
    
    
                
def get_schedule_from_json(filename):
    with open(filename) as file:
        data = js.load(file)
        schedule_dict = defaultdict(list)
        for operation, schedule_list in data["machine_schedule"].items():
            maschine_schedule = Maschine_Schedule(operation, schedule_list)
            schedule_dict[maschine_schedule.operation].append(maschine_schedule)
    return schedule_dict
        


def generate_maschine_plan(schedule_lists, job_list, max_time):
    for number in schedule_lists:
        for schedule_data in number.schedule_list:
            for slot in schedule_data["schedule"]:
                all_options = dev_options_form_parts(len(schedule_data["schedule"]))
                print(len(schedule_data["schedule"]))
                #print(all_options)
                machine_time_list=[]
                for job_data in job_list:
                    for batch_size in get_batch_size():
                        machine_time = job_data.quantity * job_data.production_time * batch_size + job_data.equip_time
                        machine_time_list.append(machine_time)

                

         


jobs_data = get_job_data_form_json("data.json")


for operation, schedule_list in get_schedule_from_json("data.json").items() :
     job_list = jobs_data[operation]
     maschine_plan = generate_maschine_plan(schedule_list, job_list, get_max_time())


# Die Funktion dev_options_form_parts kann zur Erzeugung aller möglichen Job-Reihenfolgen verwendet werden.
def generate_job_permutations(jobs_data):
    jobs = []
    for operation, job_list in jobs_data.items():
        for job in job_list:
            jobs.append(job)

    # Erzeugen Sie alle möglichen Permutationen der Jobs.
    job_permutations = itertools.permutations(jobs)

    return job_permutations

# Diese Funktion berechnet die Gesamtkosten für einen gegebenen Zeitplan.
def calculate_total_cost(schedule, max_time):
    # Hier implementieren Sie die Berechnung der Gesamtkosten für den Zeitplan.
    # Sie müssen die Maschinenzeitpläne und die Ressourcenkapazität (max_time) berücksichtigen.
    pass

def brute_force_job_shop_scheduling(jobs_data, schedule_lists, max_time):
    best_schedule = None
    best_cost = float('inf')

    job_permutations = generate_job_permutations(jobs_data)

    for permutation in job_permutations:
        # Erstellen Sie einen Zeitplan basierend auf der aktuellen Permutation.
        current_schedule = generate_schedule(permutation, schedule_lists)

        # Berechnen Sie die Gesamtkosten für den aktuellen Zeitplan.
        current_cost = calculate_total_cost(current_schedule, max_time)

        # Aktualisieren Sie den besten Zeitplan, wenn der aktuelle Zeitplan kostengünstiger ist.
        if current_cost < best_cost:
            best_cost = current_cost
            best_schedule = current_schedule

    return best_schedule, best_cost

# Beispielaufruf:
jobs_data = get_job_data_form_json("data.json")
schedule_lists = get_schedule_from_json("data.json")
max_time = get_max_time()

best_schedule, best_cost = brute_force_job_shop_scheduling(jobs_data, schedule_lists, max_time)
print("Best Schedule:", best_schedule)
print("Best Cost:", best_cost)
