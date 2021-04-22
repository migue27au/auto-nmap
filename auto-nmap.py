#!/usr/bin/python3

import subprocess
import sys
import re
import time
import sys

#os.system('ls -l')

usage = "usage"
help = "help"

address_pattern = re.compile("^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")
timing_pattern = re.compile("^-T[1-5]$")

def main(argv):
    # try:
    #   opts, args = getopt.getopt(argv,"a:h",["address=","h="])
    # except getopt.GetoptError:
    #     print(help_options)
    #     sys.exit(2)

    # for opt, arg in opts:
    #     if opt == in ("-h", "--help"):
    #         print (usage)
    #         print(help)
    #         sys.exit()
    #     elif opt in ("-a","--adress"):
    #         address = arg

    address = argv[0] 
    address_matched = address_pattern.match(address)
    
    try:
        timing = argv[1]
        timing_matched = timing_pattern.match(timing)
        if(timing_matched != None and timing_matched == True):
            timing = str(timing[2])
        else:
            timing = str(5)
    except IndexError as indexError:
        timing = str(5)

    if(address_matched):
        nmap_all_ports = "nmap -p- --open -n -vv -T" + timing + " -oN all_ports.txt " + address
        print("nmap -> " + nmap_all_ports)
    
        cmd = subprocess.run(nmap_all_ports, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        nmap_all_ports_out = str(cmd).split("\\n")
        nmap_all_ports_out = nmap_all_ports_out[:-1]

        index1 = 0
        for line in nmap_all_ports_out:            
            if "PORT" in line:
                index1 = nmap_all_ports_out.index(line)+1  #obtengo el índice de donde empiezan los puertos
                break
        
        
        index2 = nmap_all_ports_out.index("", index1)  #obtengo el índice de donde terminan los puertos

        all_ports = nmap_all_ports_out[index1:index2]
        for port in range(len(all_ports)):
            all_ports[port] = all_ports[port].split("/")[0]
        
        target_ports = ','.join(all_ports)
        print("open ports -> " + target_ports)

        nmap_target_ports = "nmap -p" + target_ports + " -n -sC -sV -v -T" + timing + " -oN target_ports.txt " + address
        print("target nmap -> " + nmap_target_ports)
    
        cmd = subprocess.run(nmap_target_ports, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        nmap_target_ports_out = str(cmd).split("\\n")
        nmap_target_ports_out = nmap_target_ports_out[:-1]

        for line in nmap_target_ports_out:
            print(line)


    else:
        print(help)





if __name__ == "__main__":
    main(sys.argv[1:])