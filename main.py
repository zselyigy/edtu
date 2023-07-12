def main():
    print('edtu program started.')
# reading the simulation results file
    my_filename = 'simulationResults_Shrestha2019'
    print('Reading concentration file', my_filename)
    concentrations = []
    i = 0
    with open(my_filename,'r') as results_file:
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
    print('Number of datapoints in the simulation results file: ', len(concentrations))
# reading the estimated experimental sigmas file
    my_filename = 'sigmas'
    print('Reading estimated sigmas file', my_filename)
    sigmas = []
    i = -1
    j = 0
    with open(my_filename,'r') as results_file:
        for line in results_file:
            j = j + 1
            if line[0:1] != '!':
                i = i + 1
                mystr1 = line[0:9]
                mystr1 = mystr1.strip()
                mystr2 = line[44:53]
                mystr2 = mystr2.strip()
                mydata = [mystr1, int(line[33:36]), mystr2, float(line[67:76])]
                if mydata[0] != concentrations[i][0]:
                    print('Mismathching xml name at line ', j , 'in sigma file')
                    return
                if mydata[1] != concentrations[i][2]:
                    print('Mismathching point number at line ', j , 'in sigma file')
                    return
                if mydata[2] != concentrations[i][1]:
                    print('Mismathching species name at line ', j , 'in sigma file')
                    return
                sigmas.append(mydata)
    results_file.close()
    print('Number of datapoints in the sigmas file: ', len(sigmas))


if __name__ == "__main__":
    main()