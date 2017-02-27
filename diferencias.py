import os
import numpy as np

sujetos = ['k3b','k6b','l1b']
clases  = ['izq','der']
canales = ['28','31','34']

def abrirArchivos():
    def abrir(archivo):
        f=open(archivo,'r')
        datos=f.readlines()
        return [float(d) for d in datos]
    
    resultado=[]
    for sujeto in sujetos:#Leer resultados de todos los sujetos
        clasesSujeto=[]
        for clase in clases:#Leer los canales de cada clase
            canalesClase=[]
            for canal in canales:#Leer los tres canales
                folder='signals/'+sujeto+'/'+clase+'/'+canal
                seriesCanal=[]
                for archivo in range(len(os.listdir(folder))):#Leer todas las senales del canal
                    seriesCanal.append(abrir(folder+'/'+str(archivo)))
                canalesClase.append(seriesCanal)
            clasesSujeto.append(canalesClase)
        resultado.append(clasesSujeto)
    return resultado
    
def phaseDifs(series):
    #Calcula la dif de fase entre los espectros de Ci y Cz
    def dif(ci,cz):
        resultado=[]
        for i in range(len(ci)):#Cada experimento
            serieI=ci[i]
            serieZ=cz[i]
            difs=[]
            for j in range(len(serieI)):#Cada valor de la serie
                theta=serieI[j]-serieZ[j]
                if theta<-np.pi:
                    theta+=2*np.pi
                elif np.pi<theta:
                    theta-=2*np.pi
                difs.append(theta)
            resultado.append(difs)
        return resultado
        
    resultado=[]
    for sujeto in series:#Cada sujeto (k3b,k6b,l1b)
        difsClase=[]
        for clase in sujeto:#Cada clase (izq,der)
            fasesCanales=[]
            for canal in clase:#C3, Cz, C4
                fasesCanal=[]
                espectros=np.fft.fft(canal)
                for espectro in espectros:#Obtener fase de espectros del canal
                    imag=[espectro.imag[i] for i in range(140)]
                    real=[espectro.real[i] for i in range(140)]
                    fasesCanal.append(np.arctan2(imag,real))#arctan(imag/real)
                fasesCanales.append(fasesCanal)#Unir fases de todos los canales de la clase
            difsClase.append(dif(fasesCanales[0],fasesCanales[1]))#C3-cz
            difsClase.append(dif(fasesCanales[2],fasesCanales[1]))#C4-Cz
        resultado.append(difsClase)
    return resultado
    
def guardar(diferencias):
    carpetas=['C3-Cz','C4-Cz']
    folder='diferencias'
    os.mkdir(folder)
    for i in range(3):
        os.mkdir(folder+'/'+sujetos[i])
        for j in range(2):
            os.mkdir(folder+'/'+sujetos[i]+'/'+clases[j])
            for k in range(2):
                os.mkdir(folder+'/'+sujetos[i]+'/'+clases[j]+'/'+carpetas[k])
                difs=diferencias[i][j][k]
                for l in range(len(difs)):
                    f=open(folder+'/'+sujetos[i]+'/'+clases[j]+'/'+carpetas[k]+'/'+str(l)+'.txt','w')
                    for t in range(len(difs)):
                        f.write(str(float(t)/4)+' '+str(difs[t])+'\n')
                    f.close()
if __name__=='__main__':
    series=abrirArchivos()
    diferencias=phaseDifs(series)
    guardar(diferencias)
