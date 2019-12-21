import csv
import datetime
import time

file_loc = input("Enter file directory: ")
file_name = input("Enter file name: ")

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
            time_split = row[2].split(":")
            total_seconds = datetime.timedelta(hours = int(time_split[0]), minutes = int(time_split[1]), seconds = int(time_split[2])).total_seconds()
            if(ip in ips):
                ips.get(ip).append(total_seconds)
            else:
                ips[ip]=[total_seconds]

            num_organized+=1
            if(num_organized%1000000==0):
                print("organized "+str(num_organized) + " entries")

print("finished organizing " + str(num_organized)+ " entries. Now processing data")
print("there are "+str(len(ips))+ " unique IPS")

num_processed=0
for ip in ips:
    times=ips.get(ip)
    times_len=len(times)
    if times_len>1000:
        for i in range(times_len - 5):
            if times[i+5]-times[i]<60:
                bot_ips.append(ip)
                break

    num_processed+=1
    if(num_processed%100000==0):
        print("processed "+str(num_processed) +" IPs")
t2=time.time()

print("All bots:\n"+ str(bot_ips))
print("There are "+str(len(bot_ips))+ " bots")
print("Finished in "+str(t2-t1)+" seconds")
input("press any key to continue")
