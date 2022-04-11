import os
import sys

filename = 'trv.log'
filename_csv = os.getcwd() + "\\trv.csv"


n_sistema = 215
if(len(sys.argv) > 1):
    n_sistema = int(sys.argv[1])
n_valvula = 1
if(len(sys.argv) > 2):
    n_valvula = int(sys.argv[2])


data_time = []
data_temperatura = []
data_setpoint = []
data_cobertura = []
data_status = []

textfile = list(enumerate(open(filename, 'r')))

misistema = False

for lineindex,line in textfile:
    # Busca mi sistema
    if misistema == False and (("mapeado como trv: " + str(n_sistema)) in line):
        linedata = textfile[lineindex][1]
        data_time.append(linedata[1:13])
        misistema = True

    if misistema == True and '--------------------------------------------------------------' in line:
        misistema = False

    if misistema == True :
        # Search for the line with the data
        if ("sas_ws.valve[" + str(n_valvula) + "].status ") in line:
                # Search for the data in the line
                for index in range(len(line)):
                    if line[index] == ' ':
                        # Cobertura
                        data_cobertura.append(int(line[index+1:len(line)], base=16) >> 25)
                        # Estado ON-OFF
                        data_status.append((int(line[index+1:len(line)], base=16) >> 6) & 1)
                        break

        if ("sas_ws.valve[" + str(n_valvula) + "].temps_1 ") in line:
                # Search for the data in the line
                for index in range(len(line)):
                    if line[index] == ' ':
                        # Setpoint de la valvula
                        data_setpoint.append(int(line[index+1:len(line)], base=16) & 4095)
                        break

        if ("sas_ws.valve[" + str(n_valvula) + "].temps_2 ") in line:
                # Search for the data in the line
                for index in range(len(line)):
                    if line[index] == ' ':
                        # Temperatura de la valvula
                        # dataY.append(int(line[index+1:len(line)], base=16) & 255)
                        # Temperatura de la valvula sin offset
                        offset = ((int(line[index+1:len(line)], base=16) >> 16) & 255)
                        temperatura = int(line[index+1:len(line)], base=16) & 4095
                        if( offset > 6 ):
                            data_temperatura.append(temperatura + 60)
                        elif ( offset == 0 ):
                            data_temperatura.append(temperatura)
                        else :
                            data_temperatura.append(temperatura - 60)
                        # dataY.append(int(line[index+1:len(line)], base=16) & 255)
                        break

data_csv = "Time\tSetpoint\tTemperatura\tCobertura\tEstado\n"

for dataindex in range(len(data_time)):
    data_csv += (data_time[dataindex] + "\t" + str(data_setpoint[dataindex]) + "\t" + str(data_temperatura[dataindex]) + "\t" + str(data_cobertura[dataindex])+ "\t" + str(data_status[dataindex]) + "\n")

with open(filename_csv, 'w') as f:
    f.write(str(data_csv))
    f.close()

