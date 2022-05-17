## GPLv3 Delli Ponti 2022

import os
import sys
import numpy
import subprocess

file_in=sys.argv[1] #cross input file
window=int(sys.argv[2]) #window of interest

#normalise shape-map in window

print("Normalising shape data in window "+str(window)+" ...")
file=open(file_in,"r").readlines()
vet=[]
i=1
n=1
out=open("normalised.shape","w")
fast=open("sequence.fasta","w")
fast.write(">sequence\n")
for line in file:
	camp=line.split()
	fast.write(camp[1])
	if i<=window:
		vet.append(float(camp[2]))
		i=i+1
	else:
		out.write(str(n*window)+"\t"+str(numpy.mean(vet))+"\n")
		i=1
		n=n+1
		vet=[]
		vet.append(float(camp[2]))
		
#cross normalisation in shape	

tmp=open("predshape.map","w")
for line in file:
	d=line.split()
	norm=((1)*((-float(d[2])+1)/2)-0)
	tmp.write(str(d[0])+" "+str(norm)+" 0 "+str(d[1])+"\n")
tmp.close()
out.close()
fast.close()

#scanfold
print("Launching Scanfold in step 1 and window "+str(window)+"...")
os.system("python3.6 ScanFold-Scan.py -i sequence.fasta -s 1 -w "+str(window)+" -p | awk '(NF==7){print $1,$2,$5,$6}' > scanfold.out")

#normalise scanfold

vet=[]
i=1
n=1
print("Normalising Scanfold in a window "+str(window)+"...")
scan=open("scanfold.out","r").readlines()
out=open("normalise.scan","w")
for line in scan:
	camp=line.split()
	if i<=window:
		vet.append(float(camp[2]))
		i=i+1
	else:
		out.write(str(n*window)+"\t"+str(numpy.mean(vet))+"\n")
		i=1
		n=n+1
		vet=[]
		vet.append(float(camp[2]))
out.close()

print("Launching Superfold with input shape data, this step will take a while...")
os.system("export DATAPATH=RNAstructure/data_tables/; export PATH=$PATH:RNAstructure/exe/; python2.7 Superfold/Superfold.py predshape.map") 

#normalise entropy

vet=[]
i=1
n=1
print("Normalising Entropy in a window "+str(window)+"...")
direct=os.getcwd()
files=os.listdir(direct)
for file in files:
	if file.split("_")[0]=="results" and file.split("_")[1]=="predshape.map":
			shan_path=file
entr=open("./"+shan_path+"/shannon"+shan_path.split("results")[1]+".txt","r").readlines()
out=open("normalise.entr","w")
leng=0
for line in entr:
	leng=leng+1
	camp=line.split()
	if i<=window:
		vet.append(float(camp[1]))
		i=i+1
	else:
		out.write(str(n*window)+"\t"+str(numpy.mean(vet))+"\n")
		i=1
		n=n+1
		vet=[]
		vet.append(float(camp[1]))
out.close()

#this value can be modfied in order to select for example the bottom 10% or 30%, instead of the default 20%
tot=round(n/10)*2

#plotting with R

#selecting the top 20% before plotting
os.system("export LC_ALL=C; sort -k2 -n normalise.entr | head -"+str(tot)+" | awk '{print \"Entropy\",$1}' > sort.1")
os.system("export LC_ALL=C; sort -k2 -n normalise.scan | head -"+str(tot)+" | awk '{print \"Scanfold\",$1}'> sort.2")
os.system("export LC_ALL=C; sort -k2 -n normalised.shape | head -"+str(tot)+" | awk '{print \"Secondary_Structure\",$1}' > sort.3")
os.system("cat sort.3 sort.2 sort.1 > topscores.txt")
subprocess.call("cat plot.r | R --slave --vanilla --args topscores.txt "+str(leng),shell=True)

#checking common regions

diz={}
file=open("topscores.txt","r").readlines()
for line in file:
	camp=line.split()
	if camp[1] not in diz:
		diz[camp[1]]=[]
		diz[camp[1]].append(camp[0])
	else:
		diz[camp[1]].append(camp[0])

#structural ouptut

direct=os.getcwd()
files=os.listdir(direct)
for file in files:
	if file.split("_")[0]=="results" and file.split("_")[1]==file_in:
			shan_path=file

file=open("./"+shan_path+"/merged"+shan_path.split("results")[1]+".ct","r").readlines()
out=open("out.tmp1","w")
vet=[]
chk=[]
i=1
n=1
for line in file[1:]:
	camp=line.split()
	if i<=window:
		if int(camp[4])==0:
			vet.append(".")
		else:
			if (int(camp[4]) not in chk):
				if (int(camp[4])<=n*window) and (int(camp[4])>=(n-1)*window):
					vet.append("(")
					chk.append(int(camp[0]))
				else:
					vet.append(".")
			else:
				vet.append(")")
			
	else:
		out.write(str(n*window)+"\t")
		for elem in vet:
			out.write(elem)
		out.write("\n")
		i=1
		n=n+1
		vet=[]
		chk=[]
		if int(camp[4])==0:
			vet.append(".")
		else:
			if (int(camp[4]) not in chk):
				if (int(camp[4])<=n*window) and (int(camp[4])>=(n-1)*window):
					vet.append("(")
					chk.append(int(camp[0]))
				else:
					vet.append(".")
			else:
				vet.append(")")
	i=i+1

out.close()

# final output writing

file=open("out.tmp1","r").readlines()
final=open("output/out.txt","w")
for line in file:
	camp=line.split()
	beg=int(camp[0])-window
	if camp[0] in diz:
		final.write(str(beg)+"-"+camp[0]+"\t")
		for elem in diz[camp[0]]:
			final.write(elem+";")
		final.write("\t")
		final.write(camp[1]+"\n")
final.close()
