import numpy
import random

def main():
    print('edtu program started.')
# constans fixed in the code
    my_filename_c = 'simulationResults_Shrestha2019'   # file name of the simulation results
    my_filename_s = 'sigmas'                           # file name of the estimated sigma values
    stratas = 50                                     # number of stratas in the sampling
# reading the simulation results file
    print('Reading concentration file', my_filename_c)
    concentrations = []
    i = 0
    with open(my_filename_c,'r') as results_file:
        for line in results_file:
            i = i + 1
            if line[0:2] != '->':
                mystr1 = line[0:9]
                mystr1 = mystr1.strip()
                mystr2 = line[10:31]
                mystr2 = mystr2.strip()
                mydata = [mystr1, mystr2, int(line[31:38]), float(line[40:53]), float(line[53:66]), float(line[66:79]), float(line[79:92]), float(line[92:105]), float(line[105:118]), float(line[118:131]), float(line[131:144]), float(line[144:157]), float(line[157:170]), float(line[170:183]), float(line[183:196])]
                concentrations.append(mydata)
    results_file.close()
    no_datapoints = len(concentrations)
    print('Number of datapoints in the simulation results file: ', no_datapoints)
# reading the estimated experimental sigmas file
    print('Reading estimated sigmas file', my_filename_s)
    sigmas = []
    i = -1
    j = 0
    error = False
    with open(my_filename_s,'r') as results_file:
        for line in results_file:
            j = j + 1
            if line[0:1] != '!':
                i = i + 1
                mystr1 = line[0:9]
                mystr1 = mystr1.strip()
                mystr2 = line[41:55]
                mystr2 = mystr2.strip()
                mydata = [mystr1, int(line[11:39]), mystr2, float(line[67:76])]
                if mydata[0] != concentrations[i][0]:
                    print('Mismathching xml name in line ', j , 'in sigma file.')
                    error = True                    
                if mydata[1] != concentrations[i][2]:
                    print('Mismathching point number in line ', j , 'in sigma file.')
                    error = True
                if mydata[2] != concentrations[i][1]:
                    print('Mismathching species name in line ', j , 'in sigma file.')
                    error = True
                if error:
                    return
                sigmas.append(mydata)
    results_file.close()
    print('Number of datapoints in the sigmas file: ', len(sigmas))
    if no_datapoints != len(sigmas):
        print('Different number of datapoints in the simulation results and the sigmas files.')

    print('Random sample generation started.')
    random_numbers = numpy.empty((stratas,no_datapoints),int)
    for i in range(stratas):
        print(i)
        for j in range(no_datapoints):
          random_numbers[i][j] = random.randint(0,9)
    print('Random sample generation finished.')
        

if __name__ == "__main__":
    main()