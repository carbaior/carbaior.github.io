#!/usr/bin/python3

import bz2, asyncio
from pyscript import document
from pyweb import pydom


"""
  
 == CSN ON ECLIPTIC J2000 (modified 17.11.2007):==
   
 <31deg> ARIES <56deg> TAURUS <92deg> GEMINI
 <118deg> CANCER <137deg> LEO <172deg> VIRGO
 <215deg> LIBRA <239deg> SCORPIO
 <266deg> SAGITTARIUS <296deg> CAPRICORN
 <326deg> AQUARIUS <349deg> PISCES
  
  
  sol sagitario
  luna scorpio
  saturno leo
  jupiter scorpio
  marte scorpio
  venus sagitario
  mercurio capricornio
 
 	SOL	LUNA	SATURNO JUPITER	MARTE	VENUS	MERCURIO
# DESDE: --------------------------------------------------------
	7.5	6.5	3.5	6.5	6.5	7.5	8.5
# HASTA: --------------------------------------------------------
	9.0	8.0	5.0	8.0	8.0	9.0	10.0
# MEJOR: --------------------------------------------------------
        8.5	7.5	4.5	7.5	7.5	8.5	9.5


	SOL	LUNA	SATURNO JUPITER	MARTE	VENUS	MERCURIO
# DESDE: --------------------------------------------------------
	8.0	7.0	4.0	7.0	7.0	8.0	9.0
# HASTA: --------------------------------------------------------
	9.0	8.0	5.0	8.0	8.0	9.0	10.0
# MEJOR: --------------------------------------------------------
        8.5	7.5	4.5	7.5	7.5	8.5	9.5
        
============================================================
0 ARIES	1 TAURO 2 GEMINIS 3 CANCER 4 LEO 5 VIRGO 6 LIBRA 7 ESCORPIO 8 SAGITARIO 9 CAPRICORNIO 10 ACUARIO 11 PISCIS 12=0
============================================================

"""
#Z =  [310,560,920,1180,1370,1720,2150,2390,2660,2960,3260,3490,3900,4150]
#zod: te da pos zodiaco de una posición en décimas de grados
def zod(p):
	if p<310:
		i=11
		p+=3600
	else:
		for i in range(len(Z)-1):
			if p<Z[i+1]:
				break
	
	q=p-Z[i]
	d=(Z[i+1]-Z[i])/10
	q=int(q/d)
	return str(i)+'.'+str(q)
		


#ini: te da inicio del intervalo en *decimas de grados* (grados/10)
def ini(i):
	a=Z[int(h1[i])]
	b=(h1[i]-int(h1[i]))*(Z[int(h1[i])+1]-a)
	res = a+b+6
	if res > 3590:
		res-=3590
	return (res)

#fin: te da fin del intervalo en *decimas de grados* (grados/10)
def fin(i):
	a=Z[int(h2[i])]
	b=(h2[i]-int(h2[i]))*(Z[int(h2[i])+1]-a)
	res = a+b+6
	if res > 3590:
		res-=3590
	return (res)

#mejor: te da el "mejor punto" del intervalo en *decimas de grados* (grados/10)
def mejor(i):
	a=Z[int(m[i])]
	b=(m[i]-int(m[i]))*(Z[int(m[i])+1]-a)
	res = a+b+6
	if res > 3590:
		res-=3590
	return (res)
	
def suma(a,b):
	if (res := a + b) >= 3600:
		res-=3600
	return res
	
def resta(a,b):
	if (res := a - b) <= 0:
		res+=3600
	return res	
	
def ang(a,b):
	if (a < b):
		a,b = b,a
	if (res := a -b) > 1800:
		res=3600-res
	return res

def ang_s(a,b):
	s = 1
	if (a < b):
		a,b = b,a
		s = -1
	if (res := a -b) > 1800:
		res=3600-res
	return res*s
	
def imprimir(reg):
	"""
	dst = []
	for i in range(0,dst):
		dst.append(int(ang(reg[i+1],mejor[i])))
	
	"""
	
	a=ang(reg[1],mejor(0))
	b=ang(reg[2],mejor(1))
	c=ang(reg[3],mejor(2))
	d=ang(reg[4],mejor(3))
	e=ang(reg[5],mejor(4))
	f=ang(reg[6],mejor(5))
	g=ang(reg[7],mejor(6))
	avgdst=(a+b+c+d+e+f+g)/7
	
	cadena=""
	cadena+="\n----------------------------------------"
	cadena+="\nPLANETS FIT THE HOROSCOPE AT JD:"+str(reg[0])+"\n"
	gc=""
	if int(reg[0])>2299160:
		gc=" (GC)"
	cadena+='YEAR/MONTH/DAY='+str(reg[8])+'/ '+str(reg[9])+'/ '+str(reg[10])+gc+"\n"+"\n"
	cadena+="\tPositions: J2000/ planet-Sun J2000/ CS:\n\n"
	cadena+="\tSUN\tMOON\tSATURN\tJUPITER\tMARS\tVENUS\tMERCURY\n"
	cadena+='\t{:.1f}'.format(reg[1]/10)
	cadena+='\t{:.1f}'.format(reg[2]/10)
	cadena+='\t{:.1f}'.format(reg[3]/10)
	cadena+='\t{:.1f}'.format(reg[4]/10)
	cadena+='\t{:.1f}'.format(reg[5]/10)
	cadena+='\t{:.1f}'.format(reg[6]/10)
	cadena+='\t{:.1f}'.format(reg[7]/10)+'\n'
	cadena+='\t{:.1f}'.format(0.0)
	cadena+='\t{:.1f}'.format(ang_s(reg[2],reg[1])/10)
	cadena+='\t{:.1f}'.format(ang_s(reg[3],reg[1])/10)
	cadena+='\t{:.1f}'.format(ang_s(reg[4],reg[1])/10)
	cadena+='\t{:.1f}'.format(ang_s(reg[5],reg[1])/10)
	cadena+='\t{:.1f}'.format(ang_s(reg[6],reg[1])/10)
	cadena+='\t{:.1f}'.format(ang_s(reg[7],reg[1])/10)+'\n'
	for i in range (1,8):
		cadena+='\t'+zod(reg[i])
	cadena+='\n\nAVERAGE DISTANCE FROM BEST POINTS:'
	cadena+='\t{:.1f}'.format(avgdst/10) + ' deg'
	cadena+='\n                 YEAR/MONTH/DAY=\t'+str(reg[8])+'/ '+str(reg[9])+'/ '+str(reg[10])+gc
	cadena+="\n----------------------------------------"
	return cadena


def limpiar(event):
	infile = open('saludo','rt')
	#infile = open('planetpos.dat','rt')
	textarea = document.querySelector("#textarea")
	textarea.value = infile.read()
	runButton=document.getElementById("run")
	runButton.removeAttribute("disabled")
	dwnldButton=document.getElementById("save")
	dwnldButton.setAttribute("disabled","true")
	"""
	for i in ["sun","moon","sat","jup","mars","venus","merc"]:
		pos=document.querySelector("#i"+i)
		pos.value="0.0"
		pos=document.querySelector("#f"+i)	
		pos.value="0.0"
		pos=document.querySelector("#b"+i)
		pos.value="0.0"
	nombre=document.querySelector("#nombre")
	nombre.value=""
	"""
	infile.close()


async def horosweb(event):
	runButton=document.getElementById("run")
	runButton.setAttribute("value","Press 'New'")
	runButton.setAttribute("disabled","true")

	newButton=document.getElementById("new")
	newButton.setAttribute("disabled","true")
	dwnldButton=document.getElementById("save")
	dwnldButton.setAttribute("disabled","true")
	textarea = document.querySelector("#textarea")
	#desde:
	global h1 
	#h1 = [8,7,4,7,7,8,9]
	#h1 = [6,3,11,1,11,9,10]
	h1=[]
	
	#hasta:
	global h2
	#h2 = [9,8,5,8,8,9,10]
	#h2 = [11,4,12,2,12,11,11]
	h2=[]
	
	#mejor:
	global m
	#m =  [8.5,7.5,4.5,7.5,7.5,8.5,9.5]
	#m =  [10.5,3.5,11.5,1.5,11.5,10.5,10.5] 
	m=[]
	
	j=0
	for i in ["sun","moon","sat","jup","mars","venus","merc"]:
		pos=document.querySelector("#i"+i)
		h1.append(float(pos.value))
		pos=document.querySelector("#f"+i)	
		h2.append(float(pos.value))
		pos=document.querySelector("#b"+i)
		m.append(float(pos.value))

	#zodiaco J2000:
	global Z
	Z =  [310,560,920,1180,1370,1720,2150,2390,2660,2960,3260,3490,3900,4150]

	#EMENDATIONE TEMPORUM:
	emtemp=document.getElementById("emtemp")
		
	if emtemp.checked==True:
		for i in range(0,len(Z)):
			Z[i]=Z[i]-100

	#dopusk:
	global D
	D = 50
	
	#esto se puede simplificar, pero no tengo tiempo:
	sun_f = suma(resta(fin(0),resta(ini(0),D)),D)/2
	moon_f = suma(resta(fin(1),resta(ini(1),D)),D)/2
	saturn_f = suma(resta(fin(2),resta(ini(2),D)),D)/2
	jupiter_f = suma(resta(fin(3),resta(ini(3),D)),D)/2
	mars_f = suma(resta(fin(4),resta(ini(4),D)),D)/2
	venus_f = suma(resta(fin(5),resta(ini(5),D)),D)/2
	mercury_f = suma(resta(fin(6),resta(ini(6),D)),D)/2

	sun_i = suma(resta(ini(0),D),sun_f)
	moon_i = suma(resta(ini(1),D),moon_f)
	saturn_i = suma(resta(ini(2),D),saturn_f)
	jupiter_i = suma(resta(ini(3),D),jupiter_f)
	mars_i = suma(resta(ini(4),D),mars_f)
	venus_i = suma(resta(ini(5),D),venus_f)
	mercury_i = suma(resta(ini(6),D),mercury_f)

	cadena=""
	cadena+=" ======= CONSTELLATION    SCALE  ===================\n"
	cadena+="       12=0-ARIES-1-TAURUS-2-GEMINI-3\n"
	cadena+="       3-CANCER-4-LEO-5-VIRGO-6\n"
	cadena+="       6-LIBRA-7-SCORPIO-8-SAGITTARIUS-9\n"
	cadena+="       9-CAPRICORN-10-AQUARIUS-11-PISCES-12=0\n\n"
	cadena+=" --- HOROSCOPE ACCORDING TO CONSTELLATIONS SCALE: --\n"
	cadena+="\tSUN\tMOON\tSATURN\tJUPITER\tMARS\tVENUS\tMERCURY\n"
	cadena+='from:\t{:.1f}'.format(h1[0])
	cadena+='\t{:.1f}'.format(h1[1])
	cadena+='\t{:.1f}'.format(h1[2])
	cadena+='\t{:.1f}'.format(h1[3])
	cadena+='\t{:.1f}'.format(h1[4])
	cadena+='\t{:.1f}'.format(h1[5])
	cadena+='\t{:.1f}'.format(h1[6])+"\n"
	cadena+='to:\t{:.1f}'.format(h2[0])
	cadena+='\t{:.1f}'.format(h2[1])
	cadena+='\t{:.1f}'.format(h2[2])
	cadena+='\t{:.1f}'.format(h2[3])
	cadena+='\t{:.1f}'.format(h2[4])
	cadena+='\t{:.1f}'.format(h2[5])
	cadena+='\t{:.1f}'.format(h2[6])+"\n"
	cadena+='point:\t{:.1f}'.format(m[0])
	cadena+='\t{:.1f}'.format(m[1])
	cadena+='\t{:.1f}'.format(m[2])
	cadena+='\t{:.1f}'.format(m[3])
	cadena+='\t{:.1f}'.format(m[4])
	cadena+='\t{:.1f}'.format(m[5])
	cadena+='\t{:.1f}'.format(m[6])+"\n"
	cadena+="===================================================\n\n"
	cadena+=" == CSN ON ECLIPTIC J2000 (modified 17.11.2007):==\n\n"
	cadena+=' <31deg> ARIES <56deg> TAURUS <92deg> GEMINI\n'
	cadena+=' <118deg> CANCER <137deg> LEO <172deg> VIRGO\n'
	cadena+=' <215deg> LIBRA <239deg> SCORPIO\n'
	cadena+=' <266deg> SAGITTARIUS <296deg> CAPRICORN\n'
	cadena+=' <326deg> AQUARIUS <349deg> PISCES\n\n'
	cadena+="---- HOROSCOPE ON ECLIPTIC J2000 (IN DEGREES): -----\n"
	cadena+="\tSUN\tMOON\tSATURN\tJUPITER\tMARS\tVENUS\tMERCURY\n"
	cadena+='from:\t{:.1f}'.format(ini(0)/10)
	cadena+='\t{:.1f}'.format(ini(1)/10)
	cadena+='\t{:.1f}'.format(ini(2)/10)
	cadena+='\t{:.1f}'.format(ini(3)/10)
	cadena+='\t{:.1f}'.format(ini(4)/10)
	cadena+='\t{:.1f}'.format(ini(5)/10)
	cadena+='\t{:.1f}'.format(ini(6)/10)+"\n"
	cadena+='to:\t{:.1f}'.format(fin(0)/10)
	cadena+='\t{:.1f}'.format(fin(1)/10)
	cadena+='\t{:.1f}'.format(fin(2)/10)
	cadena+='\t{:.1f}'.format(fin(3)/10)
	cadena+='\t{:.1f}'.format(fin(4)/10)
	cadena+='\t{:.1f}'.format(fin(5)/10)
	cadena+='\t{:.1f}'.format(fin(6)/10)+"\n"
	cadena+="================================================================\n\n\n"
	cadena+="            RESULTS OF CALCULATIONS\n"
	cadena+="         From year -500 to year +1950\n"
	cadena+="         (with tolerance =  "+str(D/10)+" degrees)\n"
	
	infile = bz2.open('planetpos.dat.bz2','rt')
		
	textarea.value = cadena
	
	txt_area=pydom['#textarea']
	txt_area.style["color"] = "orange"
	
	cont=0
	cont2=0
	for line in infile:
		reg=[int(x) for x in line.strip().split('\t')]
		
		r=[]
		
		if ang(reg[1],sun_i) <= sun_f and \
		ang(reg[2],moon_i) <= moon_f and \
		ang(reg[3],saturn_i) <= saturn_f and \
		ang(reg[4],jupiter_i) <= jupiter_f  and \
		ang(reg[5],mars_i) <= mars_f  and \
		ang(reg[6],venus_i) <= venus_f and \
		ang(reg[7],mercury_i) <= mercury_f:
			cadena+=imprimir(reg)
		cont+=1
		if cont==20000:
			cont=0
			simbolos=["|","/","—","\\"]
			simbolo=simbolos[cont2]
			cont2+=1
			if cont2==4:
				cont2=0			
			textarea.value = cadena + "\n\n" + simbolo + "Searching " + str(int(reg[8]/100)*100) + "'s"
			textarea.scrollTop = textarea.scrollHeight
			await asyncio.sleep(0)

	
	cadena+="\n\n\tEND OF CALCULATIONS."
	textarea.value = cadena
	textarea.scrollTop = textarea.scrollHeight
	txt_area.style["color"] = "white"

	newButton.removeAttribute("disabled")
	dwnldButton.removeAttribute("disabled")
	
	infile.close()
	
