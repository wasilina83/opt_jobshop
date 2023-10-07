import json as js
from collections import defaultdict
from optionsgenerator import dev_options_form_parts


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
     
#dev_options_form_parts()
