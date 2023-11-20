import json as js
from collections import defaultdict
from optionsgenerator import dev_options_form_parts
import itertools

class Job :
    def __init__(self, operation, part, quantity, production_time, equip_time):
        ''' ist eiene classe für die Jobs eigetlich un nötig aber ich wollte es lernen
        '''
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
    ''' ist eiene classe für die Maschienen eigetlich un nötig aber ich wollte es lernen
    '''
    def __init__(self, operation, schedule_list):
        self.operation = operation
        self.schedule_list = schedule_list

    def __str__(self):
        return f"operation: {self.operation}, schedule_list: {self.schedule_list}"
    
    def __repr__(self):
        return str(self)



def get_job_data_form_json(filename):
    '''mit eine json datei und liest die date aus gibt ein dict zurück
    defaultdict(<class 'list'>, {
    'milling': [operation: milling, part: T4, quantity: 20, production_time: 8, equip_time: 12], 
    'grinding': [operation: grinding, part: T4, quantity: 20, production_time: 16, equip_time: 24], 
    'turning': [operation: turning, part: T6, quantity: 30, production_time: 5, equip_time: 12]})
    '''
    with open(filename) as file:
        job_dict = defaultdict(list)
        data = js.load(file) 
        for part, quantity in data["manufacturing_needs"].items():
            for operation, production_time in data["production_time"][part].items():
                equip_time = data["equip_time"][operation]
                #machine_time = quantity * production_time * batch_size + equip_time
                job = Job(operation, part, quantity, production_time, equip_time)
                job_dict[job.operation].append(job)
                if operation in job_dict:
                    job_dict[operation] = [job]
                else:
                    job_dict[operation] = [job]
    return job_dict    


def get_batch_size():
    with open("data.json") as file:
        '''es gibt zwei arten von losen 1 ganzes und halbes
        '''
        data = js.load(file)
        batch_sizes = data["batch_sizes"]
        return batch_sizes


def get_max_time():
    '''es gibt eien maximale zeit die die maschnenzeit am Tag nicht überschtreiten darf 422.5 Stunden
    '''
    with open("data.json") as file:
        data = js.load(file)
        max_time = data["workload_maximum"]
        return max_time
    
                
def get_schedule_from_json(filename):
    '''mit eine json datei und liest die date aus gibt ein dict zurück
    defaultdict(<class 'list'>, {
        'milling': [operation: milling, schedule_list: 
        [{'number': 1, 'schedule': [350, 350, 320, 240, 200, 0, 0, 160, 80, 60]}, 
        {'number': 2, 'schedule': [400, 350, 320, 340, 200, 0, 0, 190, 120, 100]}]], 
        'grinding': [operation: grinding, schedule_list: 
        [{'number': 1, 'schedule': [280, 320, 360, 240, 160, 0, 0, 100, 80, 110]}]], 
        'turning': [operation: turning, schedule_list: 
        [{'number': 1, 'schedule': [380, 320, 320, 240, 200, 0, 0, 170, 150, 120]}]]})
    '''
    with open(filename) as file:
        data = js.load(file)
        schedule_dict = defaultdict(list)
        for operation, schedule_list in data["machine_schedule"].items():
            maschine_schedule = Maschine_Schedule(operation, schedule_list)
            schedule_dict[maschine_schedule.operation].append(maschine_schedule)
    return schedule_dict
        
def sort_jobs_for_mashine(filename):
    '''sortiert die Teile nach operation'''
    job_list = get_job_data_form_json(filename)
    milling_jobs = []
    grinding_jobs = []
    turning_jobs = []
    
    print(job_list)


sort_jobs_for_mashine("data.json")


def generate_maschine_plan(filename):
    max_time = get_max_time
    job_list = get_job_data_form_json(filename)
    schedule_lists = get_schedule_from_json(filename)
    '''not done'''
    # for operation, schedule_data in schedule_lists:
    #     print(operation, schedule_data)
         # for slot in schedule_data.schedule_list[0]["schedule"]:
        #     for slot in schedule_data["schedule"]:
        #         all_options = dev_options_form_parts(len(schedule_data.schedule_list[0]["schedule"]))
        #         #print(all_options)
        #         machine_time_list=[]
        #         for job_data in job_list[operation]:
        #             for batch_size in get_batch_size():
        #                 machine_time = job_data.quantity * job_data.production_time * batch_size + job_data.equip_time
        #                 machine_time_list.append(machine_time)
             



# Die Funktion dev_options_form_parts kann zur Erzeugung aller möglichen Job-Reihenfolgen verwendet werden.
def generate_job_permutations(filename):
    jobs_data = get_job_data_form_json(filename)
    maschne_data = get_schedule_from_json(filename)
    times = []
    jobs = []
    for operation, job_list in jobs_data.items():
        for job in job_list:
            jobs.append(job)
    for maschine, time in maschne_data.items():
        print(time)
    print(jobs)



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
