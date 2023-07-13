import numpy
import random

class dataseries():
    def __init__(self, speciesname):
        self.speciesname = speciesname
        self.mydatapoints = []

    def add_datapoint(self, data):
        self.mydatapoints.append(data)

class xmlfile():
    def __init__(self, name):
        self.xmlname = name
        self.myspecieslist = []
        self.mydataseries = []

    def addDataPoint(self, mydata):
#        mydata[name, species, pointnumber, nominalvalue, v1, v2, v3, v4, v5, v6, v7, v8, v9, v10]
        try:
            speciesindex = self.myspecieslist.index(mydata[1])
        except ValueError:
            self.myspecieslist.append(mydata[1])
            speciesindex = self.myspecieslist.index(mydata[1])
            self.mydataseries.append(dataseries(mydata[1]))
        self.mydataseries[speciesindex].add_datapoint(mydata[2:13])
        



def main():
    print('edtu program started.')
# constans fixed in the code
    my_filename_c = 'simulationResults_Shrestha2019'   # file name of the simulation results
    my_filename_s = 'sigmas'                           # file name of the estimated sigma values
    stratas = 50                                     # number of stratas in the sampling

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
                mydata = [mystr1, int(line[11:39]), mystr2, float(line[67:76])]
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

                # put the new data point in the structure
                # let us recover the corresponding sigma value by linear point number - should be rewritten to proper search later
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

    print('Random sample generation started.')
    random_numbers = numpy.empty((stratas,no_datapoints),int)
    for i in range(stratas):
        for j in range(no_datapoints):
          random_numbers[i][j] = random.randint(0,9)
    print('Random sample generation finished.')
        

if __name__ == "__main__":
    main()