# RNAvigator

#Having the software ready

RNAvigator is a tool to identify potential functional RNA structure elements on an input RNA molecule. To run, RNAvigator requires additional software to be integrated in its pipeline. To download RNAvigator, you just need to clone it using the appropriated link on Github using the following command:  
  
git clone link  
  
To run RNAvigator, you need the following software:  
  
Superfold (https://github.com/Weeks-UNC/Superfold)  
Scanfold (https://github.com/moss-lab/ScanFold)  
python3.6 and python 2.7  
R  
  
Be aware that they also have several dependencies, including the algorithms RNAfold and RNAstructure, so be use to install all of them.  
  
Once everything is ready, be sure to install or to copy the folder of RNAstructure and Superfold inside the RNAvigator folder. Plus, you also need to copy in this folder the ScanFold-Scan.py script from Scanfold.  
  
Once everything is ready, the RNAvigator folder should have inside the following:  
  
RNAstructure  
Superfold  
output  
ScanFold-Scan.py  
rnavigator_shape.py  
rnavigator_cross.py  
plot.r  
  
#Launching RNAvigator:  
  
RNAvigator uses as input SHAPE.map files or CROSS predictions, respectively for rnavigator_shape.py (experimental pipeline) and rnavigator_cross.py (predictive pipeline). Be also sure that your input files are inside RNAvigator folder.  
  
At the moment, CROSS algorithm is only available as a webserver at: http://service.tartaglialab.com/new_submission/cross. So, to generate the input CROSS prediction, run the algorithm online having in input your sequence and by using the GLOBAL SCORE module. After that, save the output table with the predictions in a text file and have it ready as input.  
  
To run RNAvigator, you just need to type the following while inside RNAvigator folder:  
  
python3.6 rnavigator_shape.py shape_map_file window  
python3.6 rnavigator_cross.py cross_file window  
  
where window is an integer that corresponds to the window that you want to use to cut and slide the main sequence. As standard value for our publication, we used 150, but of course this number should change especially for smaller or way bigger RNAs. As general rule, we suggest to have at least a window size 20-30 times smaller than your RNA, and in multiples of 50 (for example 50 for 1000 nucleotides).  
  
RNAvigator will generate many intermediate files, but the most important ones are inside the folder “output”.
  
plot.png contains the top 20% regions plotted accordingly to the metric (entropy, secondary structure profile, or Scanfold z-score).  
  
out.txt contains the table having as output the information for each identified regions, specifically:  
  
col1: RNA region  
col2: the metric in which the region is identified in the top 20%.  
col3: the secondary structure in dots and brackets obtained from the merged ct file or Superfold.   
  
Please keep in mind that the majority of the output files, including the main ones, will be overwritten in a following run, so be sure to copy them or save with another name. Superfold folders results, partition, and fold, are based on the file name for the shape pipeline, while for the cross pipeline will always have the name predcross.  
  
 #License  
   
 RNAvigator is available under GPLv3 license.






