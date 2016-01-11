import sys
import re

target = None
origin = None

states = []
transitions = []
events = []
eventList = []

names = {}

if len(sys.argv)==2:
    origin = open(sys.argv[1],'r')
    target = sys.stdout
elif len(sys.argv)==3:
    origin = open(sys.argv[1],'r')
    target = open(sys.argv[2],'w')
else:
    print("Execution: python <input.kts> [<output.xml>]\n")
    sys.exit(-1)

target.write("<?xml version=\"1.0\" encoding=\"UTF-8\" standalone=\"yes\"?>\n");
target.write("<XmlAutomaton Stochastic=\"false\" numberOfAgents=\"1\" hasOutput=\"false\">\n");

lines = [x.replace("\n","") for x in origin.readlines() if len(x)>1]

entities = zip(lines[0::3],lines[1::3],lines[2::3])
for entity in entities:
    stateNumber = entity[0].split()[1]
    stateMarked = "true" if stateNumber == "0" else "false"
    stateInitial = " initial=\"true\"" if stateNumber == "0" else ""

    aux = re.findall("IC[^ ]*",entity[1][12:])
    IC = ""
    if len(aux)==0:
        IC = "IC0"
    elif len(aux[0].replace("*",""))==2:
        IC = "IC1"
    else:
        IC = aux[0].replace("*","")

    aux = re.findall("AC[^ ]*",entity[1][12:])
    AC = ""
    if len(aux)==0:
        AC = "AC0"
    elif len(aux[0].replace("*",""))==2:
        AC = "AC1"
    else:
        AC = aux[0].replace("*","")

    aux = re.findall("P[^ ]*",entity[1][12:])
    P = ""
    if len(aux)==0:
        P = "P0"
    elif len(aux[0].replace("*",""))==1:
        P = "P1"
    else:
        P = aux[0].replace("*","")

    aux = re.findall("M1[^ ]*",entity[1][12:])
    M1 = aux[0] if len(aux)!=0 else "M1I"
    
    aux = re.findall("M2[^ ]*",entity[1][12:])
    M2 = aux[0] if len(aux)!=0 else "M2I"

    stateName = "{0},{1},{2},{3},{4}".format(IC,M1,M2,AC,P)

    if(stateName not in names.values()):
        states.append("\t<state name=\"{0}\" marked=\"{1}\"{2}>\n\t\t<size width=\"130\" height=\"40\"/>\n\t</state>\n".format(stateName,stateMarked,stateInitial))
    names[stateNumber] = stateName

entities = zip(lines[0::3],lines[1::3],lines[2::3])
for entity in entities:
    stateNumber = entity[0].split()[1]

    aux = re.findall("IC[^ ]*",entity[1][12:])
    IC = ""
    if len(aux)==0:
        IC = "IC0"
    elif len(aux[0].replace("*",""))==2:
        IC = "IC1"
    else:
        IC = aux[0].replace("*","")

    aux = re.findall("AC[^ ]*",entity[1][12:])
    AC = ""
    if len(aux)==0:
        AC = "AC0"
    elif len(aux[0].replace("*",""))==2:
        AC = "AC1"
    else:
        AC = aux[0].replace("*","")

    aux = re.findall("P[^ ]*",entity[1][12:])
    P = ""
    if len(aux)==0:
        P = "P0"
    elif len(aux[0].replace("*",""))==1:
        P = "P1"
    else:
        P = aux[0].replace("*","")

    aux = re.findall("M1[^ ]*",entity[1][12:])
    M1 = aux[0] if len(aux)!=0 else "M1I"
    
    aux = re.findall("M2[^ ]*",entity[1][12:])
    M2 = aux[0] if len(aux)!=0 else "M2I"

    stateName = "{0},{1},{2},{3},{4}".format(IC,M1,M2,AC,P)

    trans = entity[2][6:].split()
    for transition in trans:
        aux = transition.split("/")
        if aux[0] not in eventList:
            eventList.append(aux[0])
            events.append("\t<event xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xsi:type=\"XmlEvent\" name=\"{0}\" observable=\"true\" controllable=\"true\">\n\t\t<AgentProperty observable=\"true\" controllable=\"true\"/>\n\t</event>\n".format(aux[0]));
        transitionFrom = stateName
        transitionTo = names[aux[1]]
        transitionEvent = aux[0]
        transitions.append("\t<transition xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" xsi:type=\"XmlTransition\" name=\"{0}\" from=\"{1}\" to=\"{2}\" legal=\"true\">\n\t\t<labelPosition x=\"500\" y=\"0\"/>\n\t</transition>\n".format(transitionEvent,transitionFrom,transitionTo))

for state in states:
    target.write(state)

for transition in transitions:
    target.write(transition)

for event in events:
    target.write(event)


target.write("\t<initial>0</initial>\n");
target.write("</XmlAutomaton>\n");