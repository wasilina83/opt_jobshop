import itertools

def dev_options_form_parts(patrs_number):
    option = [1,0]
    option_list = []
    n=0
    while n < patrs_number:
        for rec in option:
            print(rec)
            
            option_list.append(option + 0)
            #option_list.append(option + 1)
        n = n+1
    return option_list
# i läuft von 1 bis n
#soll eine [0,1] generieren
#diese verduppeln
#jedes element aus [[0,1,0,0,i],[2i]] mit nx1 und 2nx0 erweitern

def gen_all_possible_job_sequences(jobs_data):
    jobs =[]
    for operation, job_list in jobs_data.items():
        for job in job_list:
            jobs.append(job)

    job_possibilities =itertools.permutations(jobs)
    return


 

print(dev_options_form_parts(1))
