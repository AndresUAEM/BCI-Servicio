#crear para cada sujetos
function crearCarpetas(sujeto)
  nombre='signals';
  mkdir(nombre);
  mkdir(cstrcat(nombre,"/",sujeto));#Crear carpeta de sujeto
  class={'izq','der'};
  mkdir(cstrcat(nombre,"/",sujeto,"/",char(class(1))));#Carpeta mano izquierda
  mkdir(cstrcat(nombre,"/",sujeto,"/",char(class(2))));#Carpeta mano derecha
  for channel = [28,31,34]#Canales c3,cz y c4
    mkdir(cstrcat(nombre,"/",sujeto,"/",char(class(1)),"/",int2str(channel)));#Carpeta mano izquierda
    mkdir(cstrcat(nombre,"/",sujeto,"/",char(class(2)),"/",int2str(channel)));#Carpeta mano derecha      
  endfor
endfunction

class={'izq','der'};
for suj = {'k3b','k6b','l1b'}
  sujeto=char(suj);
  archivoLectura=cstrcat(sujeto,".gdf");
  [s,HDR]=sload(archivoLectura);#abrir gdf
  triggers=HDR.TRIG;#Inicio de cada experimento
  classlabel=HDR.Classlabel;#Izq, der , pie, lengua, prueba(1,2,3,4,5)
  artefactos=HDR.ArtifactSelection;
  crearCarpetas(sujeto);
  numExp=[0,0];
  
  for i=1:rows(triggers)#Cada experimento
    clase=classlabel(i);
    trigger=triggers(i);
    #if (i!=1)
    #	disp((trigger-triggers(i-1))/250);
    #endif
    if (clase==1 || clase==2)#Mano izquierda o derecha.
      for channel = [28,31,34]#Canales c3,cz y c4
        nomF=cstrcat("signals/",sujeto,"/",char(class(clase)),"/",int2str(channel),"/",int2str(numExp(clase)));
        archivo=fopen(nomF,"w");
        for j =0:999
          fdisp(nomF,s(trigger+750+j,channel));
        endfor
        fclose(nomF);
      endfor
      numExp(clase)++;
    endif
  endfor
  
endfor
