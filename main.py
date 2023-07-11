def main():
    print('edtu program started.')
    my_filename = 'simulationResults_Shrestha2019'
    print('Reading concentration file', my_filename)

    concentrations = []
    with open(my_filename,'r') as results_file:
        for line in results_file:
            if line[0:2] != '->':
                mydata = [line[0:9], line[10:31], int(line[31:38]), float(line[40:53]), float(line[53:66]), float(line[66:79]), float(line[79:92]), float(line[92:105]), float(line[105:118]), float(line[118:131]), float(line[131:144]), float(line[144:157]), float(line[157:170]), float(line[170:183]), float(line[183:196])]
                concentrations.append(mydata)
    results_file.close()
    print('Number of datapoints: ', len(concentrations))
    

if __name__ == "__main__":
    main()