import csv
import datetime
import time
import os

file_loc = input("Enter file directory: ")
file_name = input("Enter file name (include .csv): ")

ips={}
bot_ips=[]
num_organized=0

print("organizing data")
t1=time.time()
with open(file_loc+"/"+file_name, encoding='utf-8') as csvfile:
    file = csv.reader(csvfile)
    for row in file:
        ip=row[0]
        if(ip!="ip"):
            cik=int(float(row[4]))
            time_split = row[2].split(":")
            total_seconds = datetime.timedelta(hours = int(time_split[0]), minutes = int(time_split[1]), seconds = int(time_split[2])).total_seconds()

            if ip not in ips:
                ips[ip]=[[cik],[total_seconds]]
            else:
                ips[ip][0].append(cik)
                ips[ip][1].append(total_seconds)

            num_organized+=1
            if(num_organized%1000000==0):
                print("organized "+str(num_organized) + " entries")

print("finished organizing " + str(num_organized)+ " entries. Now processing data")
print("there are "+str(len(ips))+ " unique IPS")
cik_log={}
num_processed=0

for ip in ips:
    is_human=True
    times=ips[ip][1]
    times_len=len(times)
    if times_len>1000:
        for i in range(times_len - 4):
            if times[i+4]-times[i]<60:
                is_human=False
                break
    if is_human:
        ciks=ips[ip][0]
        for cik in ciks:
            if cik not in cik_log:
                cik_log[cik]=1
            else:
                cik_log[cik]+=1

    num_processed+=1
    if(num_processed%100000==0):
        print("processed "+str(num_processed) +" IPs")

print("writing to new file")
output_file_name=file_name.split(".")[0]+"_DRT.txt"
if os.path.exists(file_loc+"/"+output_file_name):
    os.remove(file_loc+"/"+output_file_name)
output_file=open(file_loc+"/"+output_file_name,"w")
for cik in sorted(cik_log):
    output_file.write(str(cik)+":"+str(cik_log[cik])+"\n")
output_file.close()

t2=time.time()
print("Finished in "+str(t2-t1)+" seconds")
input("press any key to continue")
