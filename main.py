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
# constans fixed in the code
    my_filename_c = 'simulationResults_Shrestha2019'   # file name of the simulation results
    my_filename_s = 'sigmas'                           # file name of the estimated sigma values
    stratas = 2000                                     # number of stratas in the sampling
    error_type = 'By data series and datasets'  # 'By datasets (XMLs)','By data series (profiles)','By data series and datasets'

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

    # generation of the random samples
    print('Random sample generation started.')
    no_print_steps = 20
    progress_value = numpy.empty(no_print_steps,int)
    progress_index = 0
    for i in range(no_print_steps):
        progress_value[i] = numpy.trunc((i + 1) * no_datapoints * stratas / no_print_steps)
        
    i = 0
    random_numbers = numpy.empty((stratas,no_datapoints),int)
    for s in range(stratas):
        for k in range(no_datapoints):
          random_numbers[s][k] = random.randint(0,9)
          if progress_value[progress_index] == i:
              progress_index = progress_index + 1
              print(str(int(progress_index * 100 / no_print_steps))+'%')
          i = i + 1
    print('Random sample generation finished.')


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
                E = ((xmls[i].mydataseries[j].mydatapoints[k][3] - xmls[i].mydataseries[j].mydatapoints[k][2]) / xmls[i].mydataseries[j].mydatapoints[k][1])**2
                E_file.write(xmls[i].xmlname + ' ' + xmls[i].myspecieslist[j] + ' ' + str(xmls[i].mydataseries[j].mydatapoints[k][0]) + ' ' + str(E) + '\n')
                S_file.write(xmls[i].xmlname + ' ' + xmls[i].myspecieslist[j] + ' ' + str(xmls[i].mydataseries[j].mydatapoints[k][0]) + ' ' + str(xmls[i].mydataseries[j].mydatapoints[k][1]) + '\n')
                Edataseries = Edataseries + E
                l = l + 1
            Edataseries = Edataseries / len(xmls[i].mydataseries[j].mydatapoints)
            Exml = Exml + Edataseries
            Edataseries = 0
        Exml = Exml / len(xmls[i].mydataseries)
        Etotal = Etotal + Exml
        Exml = 0
    Etotal = Etotal / len(xmls)
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
    E_file.close()
    print('Random sampled E value calculation finished. Data writing to file may take some more time.')

                

if __name__ == "__main__":
    main()