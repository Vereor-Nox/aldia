import xml.etree.ElementTree as ET

#Create tex file that will be written
file = open('RIP.tex', 'w')

#Begin the intialization of the table in LaTeX
file.write(r"""\documentclass[12pt]{article} 
\usepackage{longtable} 
\usepackage{graphicx}
\usepackage{multirow}
\begin{document} 
	\begin{center}
		\setlength\LTleft{-1in}
		\setlength\LTright{-1in}
		\small
		\begin{longtable}{|c|c|c|c|c|c|c|}
		\caption{nmap scan results}\\
		\hline
		\textbf{Host} & \textbf{OS} & \textbf{Port} & \textbf{Service} & \textbf{Status} & \textbf{ScriptID} & \textbf{Script Result} \\
		\hline
		\endfirsthead
		\multicolumn{7}{c}%
		{\tablename\ \thetable\ } \\
		\hline
		\textbf{Host} & \textbf{OS} & \textbf{Port} & \textbf{Service} & \textbf{Status} & \textbf{ScriptID} & \textbf{Script Result} \\
		\hline
		\endhead
		\hline \multicolumn{7}{r}{} \\
		\endfoot
		\hline
		\endlastfoot

			""")

#Starts parsing the XML file from nmap scan
tree = ET.parse('SUpertest.xml')
root = tree.getroot()


#Looks for all hosts 
for host in root.findall('host'):	
	address = host.find('address').get('addr')

	#Arbitrary if statements to make sure we won't get any errors if something doesn't exist (Terrible error handling)
	#(They'll be used a lot)

	if host.find('os') != None and host.find('os').find('osmatch') != None and len(host.find('os').find('osmatch').get('name')) < 20:
		osmatch = host.find('os').find('osmatch').get('name')
	else:
		osmatch = ' '
	
	#Find better fix for osmatch instead of leaving it blank when too long

	#Looks through all services that were found for a host
	servicelist = list()
	if host.find('ports') != None and host.find('ports').findall('port') != None:


		for port in host.find('ports').findall('port'):
			
			#Finds interesting information about the service found
			portid = port.get('portid')
			state = port.find('state').get('state')
			service = port.find('service').get('name')

			if port.find('script') != None and port.find('script').get('id') != None:
				scriptid = port.find('script').get('id')
			else:
				scriptid = ' '
			#SHOULD BE FIXED

			if port.find('script') != None and port.find('script').get('output') != None and len(port.find('script').get('output')) > 40:
				scriptoutput = "Too long"
			elif port.find('script') != None and port.find('script').get('output') != None:
				scriptoutput = port.find('script').get('output')
			else:
				scriptoutput = ' '

			#Adds all the service information in a tuple, which then gets stored in a list of services
			servicetuple = (portid, service, state, scriptid, scriptoutput)
			servicelist.append(servicetuple)


	#Making cases for when it has services and when it doesn't
	if len(servicelist) > 0:
		file.write("""
	\multirow{""" + str(len(servicelist)) + '}{*}{' + address + '} & \multirow{' + str(len(servicelist)) + '}{*}{' + osmatch + '} ')

		#Shitty hacked together fence
		#Last element has to be different from the rest of them, to finish up this part of the table
		iterservices = iter(servicelist)
		prev = next(iterservices)
		for services in iterservices:
			#do thing
			file.write('& ' + prev[0] + ' & ' + prev[1] + ' & ' + prev[2] + ' & ' + prev[3] + ' & ' + prev[4] + """ \\\ \cline{3-7}
			& """)

			prev = services
		file.write('& ' + prev[0] + ' & ' + prev[1] + ' & ' + prev[2] + ' & ' + prev[3] + ' & ' + prev[4] + """ \\\ \cline{3-7}
		\cline{1-2} 

		""")
	
	else:
		file.write(address + ' & ' + osmatch + """ & & & & & \\\ 
			\cline{1-7}""")

#Finishes up the LaTeX document
file.write("""
		\end{longtable}
	\end{center}
\end{document}
	""")

#TODO
#Separate tables so script information can actually be shown properly
#Fix bad stuff

