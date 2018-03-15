import xml.etree.ElementTree as ET

file = open('RIP.tex', 'w')
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
		\caption{A simple longtable example}\\
		\hline
		\textbf{Host} & \textbf{OS} & \textbf{Port} & \textbf{Service} & \textbf{Status} & \textbf{ScriptID} & \textbf{Script Result} \\
		\hline
		\endfirsthead
		\multicolumn{7}{c}%
		{\tablename\ \thetable\ -- \textit{Continued from previous page}} \\
		\hline
		\textbf{Host} & \textbf{OS} & \textbf{Port} & \textbf{Service} & \textbf{Status} & \textbf{ScriptID} & \textbf{Script Result} \\
		\hline
		\endhead
		\hline \multicolumn{4}{r}{\textit{Continued on next page}} \\
		\endfoot
		\hline
		\endlastfoot

			""")

tree = ET.parse('SUpertest.xml')
root = tree.getroot()

for host in root.findall('host'):	
	address = host.find('address').get('addr')

	if host.find('os') != None and host.find('os').find('osmatch') != None and len(host.find('os').find('osmatch').get('name')) < 20:
		osmatch = host.find('os').find('osmatch').get('name')
	else:
		osmatch = 'N/A'

	servicelist = list()
	if host.find('ports') != None and host.find('ports').findall('port') != None:


		for port in host.find('ports').findall('port'):
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

			servicetuple = (portid, service, state, scriptid, scriptoutput)
			servicelist.append(servicetuple)



	if len(servicelist) > 0:
		file.write("""
	\multirow{""" + str(len(servicelist)) + """}{*}{""" + address + """} & \multirow{"""+ str(len(servicelist)) + """}{*}{""" + osmatch + """} """)

		#shitty hacked together fence
		iterservices = iter(servicelist)
		prev = next(iterservices)
		for services in iterservices:
			#do thing
			file.write("""& """ + prev[0] + """ & """ + prev[1] + """ & """ + prev[2] + """ & """ + prev[3] + """ & """ + prev[4] + """ \\\ \cline{3-7}
			& """)

			prev = services
		file.write("""& """ + prev[0] + """ & """ + prev[1] + """ & """ + prev[2] + """ & """ + prev[3] + """ & """ + prev[4] + """ \\\ \cline{3-7}
		\cline{1-2} 

		""")
	#use prev to fix last one

	else:
		file.write(address + ' & ' + osmatch + """ & & & & & \\\ 
			\cline{1-7}""")

#skriv case for ingen services
file.write("""
		\end{longtable}
	\end{center}
\end{document}
	""")

