import numpy
import random

class dataseries():
    def __init__(self, speciesname):
        self.speciesname = speciesname
        self.mydatapoints = []

    def add_datapoint(self, data):
        # structure of one record for each datapoint
        #  0 point number
        #  1 sigma value
        #  2 experimental value
        #  3 nominal value
        #  4-13 the ten T varied value
        self.mydatapoints.append(data)

class xmlfile():
    def __init__(self, name):
        self.xmlname = name
        self.myspecieslist = []
        self.mydataseries = []

    def addDataPoint(self, mydata):
        try:
            speciesindex = self.myspecieslist.index(mydata[1])
        except ValueError:
            self.myspecieslist.append(mydata[1])
            speciesindex = self.myspecieslist.index(mydata[1])
            self.mydataseries.append(dataseries(mydata[1]))
        self.mydataseries[speciesindex].add_datapoint(mydata[2:16])
        



def main():
    print('edtu program started.')
    no_print_steps = 20
    progress_value = numpy.empty(no_print_steps,int)

# reading the config file
    noc = True
    nos = True
    noe = True
    nor = True
    rndgener = True
    print('reading config file.')
    with open('.\config.txt','r') as C_file:
        for line in C_file:
            mystr1 = line[0:29]
            mystr1 = mystr1.strip()
            mystr2 = line[29:79]
            mystr2 = mystr2.strip()
            match mystr1:
                # file name of the simulation results
                case "simulation result file:":
                    my_filename_c = mystr2
                # file name of the estimated sigma values
                case "sigma file:":
                    my_filename_s = mystr2
                # file name of the E values
                case "E value file:":
                    my_filename_e = mystr2
                # number of stratas in the sampling
                case "number of random samples:":
                    stratas = int(mystr2)
                # type of the error used; valid values 'By datasets (XMLs)','By data series (profiles)','By data series and datasets'
                case "error type:":
                    error_type = mystr2
                case "random number file:":
                    my_filename_r = mystr2
                case "random numbers:":
                    rand_num_behav = mystr2
        try:
            print('Simulation result file name:', my_filename_c)
        except:
            print('No simulation result file name is given.')
            noc = False
        try:
            print('Sigma file name:', my_filename_s)
        except:
            print('No sigma file name is given.')
            nos = False
        try:
            print('E value file name:', my_filename_e)
        except:
            print('No E value file name is given.')
            noe = False
        if noe:
            print('The E value file was given, only its content is used.')
        else:
            if noc and nos:
                print('The simulation result and the sigma files were given, but the E value file not.')
            else:
                if noc:
                    print('No E value file and sigma file, not enough information. Please provide one of them.')
                    return
                else:
                    print('No E value file and simulation result file, not enough information. Please provide one of them.')
                    return
        try:
            print('Random number file name:', my_filename_r)
        except:
            print('No random number file name is given.')
            nor = False
        try:
            match rand_num_behav:
                case 'generate':
                    print('The random generator will generate the random numbers.')
                case 'read':
                    print('The random generator will read the random numbers.')
                    rndgener = False
                case default:
                    print('The specified random number generator behaviour is unknown, the random numbers will be generated.')
        except:
            print('Behaviour is not defined in the config file, the random numbers will be generated.')
    if not (rndgener or nor):   # Fatal error if the random numbers should be read, but no random number file name is given
        print('The random numbers should be read, but no random number file name is given: fatal error.')
        return
    if rndgener and not nor:   # Random numbers are generated, but no file name is given: use the default file name
        my_filename_r = 'random_numbers.txt'
        print('Random numbers are generated, but no file name is given: use the default file name (',my_filename_r,').')


    if noe:
        no_xmls = 0
        xmls = []
        j = 0
        # reading the data from the E file whihc is a space separated file
        # 1 line header starting with 'Dataset'
        # structure of the simulation results file for each datapoint
        #  0 xml name
        #  1 point number
        #  2 species
        #  3 nominal value
        #  4-13 the ten T varied value
        # no fixed number of T varied values, no check of the same number of elements in the file lines yet
        print('Reading E value file', my_filename_e)
        with open(my_filename_e,'r') as results_file:
            for line in results_file:
                if line[0:7] != 'Dataset':
                    j = j + 1
                    result_string = line.split(' ')
                    result_string_2 = []
                    for i in result_string:
                        if i != '':
                            result_string_2.append(i.strip())
                    # structure of the adddata for each datapoint
                    #  0 xml name
                    #  1 species
                    #  2 point number
                    #  3 sigma value NOT USED
                    #  4 experimental value NOT USED
                    #  5 nominal E value
                    #  6-15 the ten T varied E value
                    adddata = []
                    adddata.append(result_string_2[0])
                    adddata.append(result_string_2[2])
                    adddata.append(int(result_string_2[1]))
                    adddata.append(0)
                    adddata.append(0)
                    for i in range(len(result_string_2)-3):
                        adddata.append(float(result_string_2[i+3]))
#                    adddata = [mydata[0], mydata[1], mydata[2], sigmas[i][3], mydata[3], mydata[4], mydata[5], mydata[6], mydata[7], mydata[8], mydata[9], mydata[10], mydata[11], mydata[12], mydata[13], mydata[14]]   # let us compose the sigma value and the data series
                    if no_xmls == 0:
                        xmls.append(xmlfile(result_string_2[0]))
                        xmls[no_xmls].addDataPoint(adddata)
                        no_xmls = no_xmls + 1
                    else:
                        if xmls[no_xmls-1].xmlname != result_string_2[0]:
                            xmls.append(xmlfile(result_string_2[0]))
                            xmls[no_xmls].addDataPoint(adddata)
                            no_xmls = no_xmls + 1
                        else:
                            xmls[no_xmls-1].addDataPoint(adddata)
        results_file.close()
        no_datapoints = j
        print('Number of datapoints in the E value file: ', no_datapoints)


    else:
    # constans fixed in the code
    #    my_filename_c = 'simulationResults_Shrestha2019'   # file name of the simulation results
    #    my_filename_s = 'sigmas'                           # file name of the estimated sigma values
    #    stratas = 100                                     # number of stratas in the sampling
    #    error_type = 'By data series and datasets'  # 'By datasets (XMLs)','By data series (profiles)','By data series and datasets'

    # reading the estimated experimental sigmas file
        print('Reading estimated sigmas file', my_filename_s)
        sigmas = []
        error = False
        with open(my_filename_s,'r') as results_file:
            for line in results_file:
                if line[0:1] != '!':
                    mystr1 = line[0:9]
                    mystr1 = mystr1.strip()
                    mystr2 = line[41:55]
                    mystr2 = mystr2.strip()
                    mydata = [mystr1, int(line[11:39]), mystr2, float(line[73:83])]
                    sigmas.append(mydata)
        results_file.close()
        print('Number of datapoints in the sigmas file: ', len(sigmas))

    # reading the simulation results file
        print('Reading concentration file', my_filename_c)
        concentrations = []
        xmls = []
        i = -1
        j = 0
        no_xmls = 0
        with open(my_filename_c,'r') as results_file:
            for line in results_file:
                j = j + 1
                if line[0:2] != '->':
                    i = i + 1
                    mystr1 = line[0:9]
                    mystr1 = mystr1.strip()
                    mystr2 = line[10:31]
                    mystr2 = mystr2.strip()
                    # structure of the simulation results file for each datapoint
                    #  0 xml name
                    #  1 species
                    #  2 point number
                    #  3 experimental value
                    #  4 nominal value
                    #  5-14 the ten T varied value
                    mydata = [mystr1, mystr2, int(line[31:38]), float(line[40:53]), float(line[53:66]), float(line[66:79]), float(line[79:92]), float(line[92:105]), float(line[105:118]), float(line[118:131]), float(line[131:144]), float(line[144:157]), float(line[157:170]), float(line[170:183]), float(line[183:196])]
                    # check if the point is the same as it was in the sigma file
                    if sigmas[i][0] != mydata[0]:
                        print('Mismathching xml name in line ', j , 'in simulation result file.')
                        error = True                    
                    if sigmas[i][1] != mydata[2]:
                        print('Mismathching point number in line ', j , 'in simulation result file.')
                        error = True
                    if sigmas[i][2] != mydata[1]:
                        print('Mismathching species name in line ', j , 'in simulation result file.')
                        error = True
                    if error:
                        return
                    concentrations.append(mydata)

                    # structure of the adddata for each datapoint
                    #  0 xml name
                    #  1 species
                    #  2 point number
                    #  3 sigma value
                    #  4 experimental value
                    #  5 nominal value
                    #  6-15 the ten T varied value
                    adddata = [mydata[0], mydata[1], mydata[2], sigmas[i][3], mydata[3], mydata[4], mydata[5], mydata[6], mydata[7], mydata[8], mydata[9], mydata[10], mydata[11], mydata[12], mydata[13], mydata[14]]   # let us compose the sigma value and the data series
                    if no_xmls == 0:
                        xmls.append(xmlfile(mydata[0]))
                        xmls[no_xmls].addDataPoint(adddata)
                        no_xmls = no_xmls + 1
                    else:
                        if xmls[no_xmls-1].xmlname != mydata[0]:
                            xmls.append(xmlfile(mydata[0]))
                            xmls[no_xmls].addDataPoint(adddata)
                            no_xmls = no_xmls + 1
                        else:
                            xmls[no_xmls-1].addDataPoint(adddata)
        results_file.close()
        no_datapoints = len(concentrations)
        print('Number of datapoints in the simulation results file: ', no_datapoints)
        if no_datapoints != len(sigmas):
            print('Different number of datapoints in the simulation results and the sigmas files.')

    # reading or generation of the random samples
    if rndgener:
        print('Random sample generation started.')
        R_file = open(my_filename_r ,'w')
        progress_index = 0
        for i in range(no_print_steps):
            progress_value[i] = numpy.trunc((i + 1) * no_datapoints * stratas / no_print_steps)
            
        i = 0
        random_numbers = numpy.empty((stratas,no_datapoints),int)
        for s in range(stratas):
            for k in range(no_datapoints):
                random_numbers[s][k] = random.randint(0,9)
                R_file.write(str(random_numbers[s][k])+' ')
                if progress_value[progress_index] == i:
                    progress_index = progress_index + 1
                    print(str(int(progress_index * 100 / no_print_steps))+'%')
                i = i + 1
            R_file.write('\n')
        print('Random sample generation finished.')
    else:
        print('Random samples are read from file', my_filename_r)
        j = 0
        random_numbers = numpy.empty((stratas,no_datapoints),int)
        with open(my_filename_r,'r') as results_file:
            for line in results_file:
                result_string = line.split(' ')
                k = 0
                for i in result_string:
                    if i != '\n':
                        random_numbers[j][k] =int(i)
                        k = k + 1
                j = j + 1
        print(j, 'random samples were read.')
        if j != stratas:
            print('The number of stratas (',stratas,') is not equal to the number of random numbers read. Fatal error.')
            return

    # calculation of the overall E value for the nominal values
    print('Nominal E value calculation started.')
    Etotal = 0
    Exml = 0
    Edataseries = 0
    l = -1
    E_file = open('.\calculatedEvaluesbyPoints.txt','w')
    S_file = open('.\sigmas_used.txt','w')

    for i in range(len(xmls)):
        for j in range(len(xmls[i].mydataseries)):
            for k in range(len(xmls[i].mydataseries[j].mydatapoints)):
                if noe:   # if we already have the E values just read them
                    E = xmls[i].mydataseries[j].mydatapoints[k][3]
                else:     # if we have c and sigma data we have to calculate the E values
                    E = ((xmls[i].mydataseries[j].mydatapoints[k][3] - xmls[i].mydataseries[j].mydatapoints[k][2]) / xmls[i].mydataseries[j].mydatapoints[k][1])**2
                E_file.write(xmls[i].xmlname + ' ' + xmls[i].myspecieslist[j] + ' ' + str(xmls[i].mydataseries[j].mydatapoints[k][0]) + ' ' + str(E) + '\n')
                S_file.write(xmls[i].xmlname + ' ' + xmls[i].myspecieslist[j] + ' ' + str(xmls[i].mydataseries[j].mydatapoints[k][0]) + ' ' + str(xmls[i].mydataseries[j].mydatapoints[k][1]) + '\n')
                Edataseries = Edataseries + E
                l = l + 1
            Edataseries = Edataseries / len(xmls[i].mydataseries[j].mydatapoints)
            E_file.write(xmls[i].xmlname + ' ' + xmls[i].myspecieslist[j] + ' ' + str(Edataseries) + ' ' + str(len(xmls[i].mydataseries[j].mydatapoints)) + '\n')
            Exml = Exml + Edataseries
            Edataseries = 0
        Exml = Exml / len(xmls[i].mydataseries)
        E_file.write(xmls[i].xmlname + ' ' + str(Exml) + '\n')
        Etotal = Etotal + Exml
        Exml = 0
#    if error_type == 'By datasets (XMLs)' or error_type == 'By data series and datasets':
    Etotal = Etotal / len(xmls)
#    else:
        
    print('Nominal E value calculation finished.')
    E_file.close()
    S_file.close()
    print('Nominal Etotal =', Etotal)

    # calculation of the overall E value for each random sample
    print('Random sampled E value calculation started.')
    E_file = open('.\calculatedEvalues.txt','w')

    progress_index = 0
    for i in range(no_print_steps):
        progress_value[i] = numpy.trunc((i + 1) * no_datapoints / no_print_steps)
   
    for s in range(stratas):
        Etotal = 0
        Exml = 0
        Edataseries = 0
        l = -1
        for i in range(len(xmls)):
            for j in range(len(xmls[i].mydataseries)):
                for k in range(len(xmls[i].mydataseries[j].mydatapoints)):
                    if noe:   # if we already have the E values just read them
                        E = xmls[i].mydataseries[j].mydatapoints[k][4+random_numbers[s][l]]
                    else:     # if we have c and sigma data we have to calculate the E values
                        E = ((xmls[i].mydataseries[j].mydatapoints[k][4+random_numbers[s][l]] - xmls[i].mydataseries[j].mydatapoints[k][2]) / xmls[i].mydataseries[j].mydatapoints[k][1])**2
#                    E_file.write(xmls[i].xmlname + ' ' + xmls[i].myspecieslist[j] + ' ' + str(xmls[i].mydataseries[j].mydatapoints[k][0]) + ' ' + str(E) + '\n')
                    Edataseries = Edataseries + E
                    l = l + 1
                    if progress_value[progress_index] == l:
                        progress_index = progress_index + 1
                        print(str(int(progress_index * 100 / no_print_steps))+'%')
                Edataseries = Edataseries / len(xmls[i].mydataseries[j].mydatapoints)
                Exml = Exml + Edataseries
                Edataseries = 0                
            Exml = Exml / len(xmls[i].mydataseries)
            Etotal = Etotal + Exml
            Exml = 0
        Etotal = Etotal / len(xmls)
#        print(Etotal)
        E_file.write(str(Etotal)+'\n')
    print('Random sampled E value calculation finished. Data writing to file may take some more time.')
    E_file.close()

if __name__ == "__main__":
    main()