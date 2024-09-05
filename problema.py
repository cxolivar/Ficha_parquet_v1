# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 09:43:35 2024

@author: Carmen
"""

import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")  # configura el modo ancho
st.image('imagenes/UA.png',width=200)


st.header("Ficha Académica")
rut="220337758"
periodo=202420

@st.cache_data
def carga_datos():
    notas = pd.read_parquet("notas.parquet")
    carga = pd.read_parquet("carga.parquet")
    matricula = pd.read_parquet("matricula.parquet")
    return notas,carga,matricula

def datos_alumno(matricula,rut):
    ultimoperiodo=max(matricula[matricula["DSC_RUT_DV"]==rut]["ID_PERIODO_ACADEMICO"])
    sede=matricula[matricula["DSC_RUT_DV"]==rut]
    sede=sede[sede["ID_PERIODO_ACADEMICO"]==ultimoperiodo].reset_index()["UWVMAHI_CAMPUS"][0]

    carrera=matricula[matricula["DSC_RUT_DV"]==rut]
    carrera=carrera[carrera["ID_PERIODO_ACADEMICO"]==ultimoperiodo].reset_index()["UWVMAHI_PROGRAMA"][0]

    nombre=matricula[matricula["DSC_RUT_DV"]==rut]
    nombre=nombre[nombre["ID_PERIODO_ACADEMICO"]==ultimoperiodo].reset_index()["DSC_NOMBRES"][0]

    apellido_paterno=matricula[matricula["DSC_RUT_DV"]==rut]
    apellido_paterno=apellido_paterno[apellido_paterno["ID_PERIODO_ACADEMICO"]==ultimoperiodo].reset_index()["DSC_APELLIDO_PATERNO"][0]

    apellido_materno=matricula[matricula["DSC_RUT_DV"]==rut]
    apellido_materno=apellido_materno[apellido_materno["ID_PERIODO_ACADEMICO"]==ultimoperiodo].reset_index()["DSC_APELLIDO_MATERNO"][0]

    return sede,carrera,nombre,apellido_paterno,apellido_materno


def proyeccion(rut,notas_historicas,carga_academica,matricula,periodo):    
    
    notas_historicas_rut=notas_historicas[notas_historicas["DSC_RUT_DV"]==rut]
    carga_academica_rut=carga_academica[carga_academica["DSC_RUT_DV"]==rut]


    if carga_academica_rut.empty==True:  # se revisa que el archivo de carga academica no venga vacio
        ultimo_periodo_carga=periodo+1
    else:
        ultimo_periodo_carga=max(carga_academica_rut[carga_academica_rut["DSC_RUT_DV"]==rut]["ID_PERIODO_ACADEMICO"])
    
    
    
    
    ultimo_periodo_programa=max(matricula[matricula["DSC_RUT_DV"]==rut]["ID_PERIODO_ACADEMICO"])
    carga_academica_rut=carga_academica_rut[carga_academica_rut["ID_PERIODO_ACADEMICO"]==ultimo_periodo_carga]


    programa=matricula[matricula["DSC_RUT_DV"]==rut]
    programa=programa[programa["ID_PERIODO_ACADEMICO"]==ultimo_periodo_programa].reset_index()["UWVMAHI_PROGRAM"][0]
    sede=matricula[matricula["DSC_RUT_DV"]==rut]
    sede=sede[sede["ID_PERIODO_ACADEMICO"]==ultimo_periodo_programa].reset_index()["UWVMAHI_CAMPUS"][0]

    if ultimo_periodo_carga!=periodo:
            carga_academica_rut=pd.DataFrame()
            carga_academica_rut["CÓDIGOASIGNATURA"]="Sin"
            carga_academica_rut["ASIGNATURA"]="Sin"
            carga_academica_rut["NIVEL"]="Sin"
        
    
    # Cursos realizados por el estudiante
    Curso_rut=notas_historicas_rut
    
    # correccion de las notas no numericas
    if Curso_rut.shape[0]!=0:
        Curso_rut["COD_GRDE_FINAL"]=Curso_rut["COD_GRDE_FINAL"].str.replace(",","")
        Curso_rut["COD_GRDE_FINAL"]=Curso_rut["COD_GRDE_FINAL"].str.replace("RC","10")
        Curso_rut["COD_GRDE_FINAL"]=Curso_rut["COD_GRDE_FINAL"].str.replace("RR","10")
        Curso_rut["COD_GRDE_FINAL"]=Curso_rut["COD_GRDE_FINAL"].str.replace("RM","10")
        Curso_rut["COD_GRDE_FINAL"]=Curso_rut["COD_GRDE_FINAL"].str.replace("P","10")
        Curso_rut["COD_GRDE_FINAL"]=Curso_rut["COD_GRDE_FINAL"].str.replace("RI","10")
        Curso_rut["COD_GRDE_FINAL"]=Curso_rut["COD_GRDE_FINAL"].astype(int)/10
        Curso_rut=Curso_rut.drop_duplicates()
    
    
      
    
    #Malla curricular
    Homologados=pd.read_excel(f"G:/Mi unidad/Camilo Olivares/Finanzas/Python/Proyeccion 202420/Mallas/{programa}.xlsx",sheet_name='Homologados')
    
    # cursos aprobados
    Curso_rut_aprobado=Curso_rut[Curso_rut["COD_GRDE_FINAL"]>=4.0]
    
    
    # cursos pendiente y a por aprobar######################################################################################
    
    curso_pendiente=[]
    curso_aprobado_segun_plan=[]
    i=0
    for curso in Homologados["CÓDIGOASIGNATURA"]:
        aux=Homologados[Homologados["CÓDIGOASIGNATURA"]==curso]
        
        curso1=Homologados["HOM1"][Homologados["CÓDIGOASIGNATURA"]==curso][i]
        curso2=Homologados["HOM2"][Homologados["CÓDIGOASIGNATURA"]==curso][i]
        curso3=Homologados["HOM3"][Homologados["CÓDIGOASIGNATURA"]==curso][i]
        curso4=Homologados["HOM4"][Homologados["CÓDIGOASIGNATURA"]==curso][i]
        curso5=Homologados["HOM5"][Homologados["CÓDIGOASIGNATURA"]==curso][i]
        curso6=Homologados["HOM6"][Homologados["CÓDIGOASIGNATURA"]==curso][i]
        curso7=Homologados["HOM7"][Homologados["CÓDIGOASIGNATURA"]==curso][i]
        curso8=Homologados["HOM8"][Homologados["CÓDIGOASIGNATURA"]==curso][i]
        curso9=Homologados["HOM9"][Homologados["CÓDIGOASIGNATURA"]==curso][i]
        curso10=Homologados["HOM10"][Homologados["CÓDIGOASIGNATURA"]==curso][i]
        curso11=Homologados["HOM11"][Homologados["CÓDIGOASIGNATURA"]==curso][i]
        curso12=Homologados["HOM12"][Homologados["CÓDIGOASIGNATURA"]==curso][i]
        curso13=Homologados["HOM13"][Homologados["CÓDIGOASIGNATURA"]==curso][i]    
        curso14=Homologados["HOM14"][Homologados["CÓDIGOASIGNATURA"]==curso][i]
        curso15=Homologados["HOM15"][Homologados["CÓDIGOASIGNATURA"]==curso][i]
        curso16=Homologados["HOM16"][Homologados["CÓDIGOASIGNATURA"]==curso][i]
        curso17=Homologados["HOM17"][Homologados["CÓDIGOASIGNATURA"]==curso][i]
        curso18=Homologados["HOM18"][Homologados["CÓDIGOASIGNATURA"]==curso][i]
        curso19=Homologados["HOM19"][Homologados["CÓDIGOASIGNATURA"]==curso][i]
        curso20=Homologados["HOM20"][Homologados["CÓDIGOASIGNATURA"]==curso][i]
        curso21=Homologados["HOM21"][Homologados["CÓDIGOASIGNATURA"]==curso][i]
        curso22=Homologados["HOM22"][Homologados["CÓDIGOASIGNATURA"]==curso][i]
        curso23=Homologados["HOM23"][Homologados["CÓDIGOASIGNATURA"]==curso][i]
        curso24=Homologados["HOM24"][Homologados["CÓDIGOASIGNATURA"]==curso][i]
        curso25=Homologados["HOM25"][Homologados["CÓDIGOASIGNATURA"]==curso][i]
        curso26=Homologados["HOM26"][Homologados["CÓDIGOASIGNATURA"]==curso][i]
        curso27=Homologados["HOM27"][Homologados["CÓDIGOASIGNATURA"]==curso][i]
        curso28=Homologados["HOM28"][Homologados["CÓDIGOASIGNATURA"]==curso][i]
        curso29=Homologados["HOM29"][Homologados["CÓDIGOASIGNATURA"]==curso][i]
        curso30=Homologados["HOM30"][Homologados["CÓDIGOASIGNATURA"]==curso][i]
        curso31=Homologados["HOM31"][Homologados["CÓDIGOASIGNATURA"]==curso][i]
        curso32=Homologados["HOM32"][Homologados["CÓDIGOASIGNATURA"]==curso][i]
        curso33=Homologados["HOM33"][Homologados["CÓDIGOASIGNATURA"]==curso][i]
        curso34=Homologados["HOM34"][Homologados["CÓDIGOASIGNATURA"]==curso][i]
        
        
        
        
        i=1+i
        
        test=curso in Curso_rut_aprobado["COD_ASIGNATURA"].to_numpy()
        test1=curso1 in Curso_rut_aprobado["COD_ASIGNATURA"].to_numpy()
        test2=curso2 in Curso_rut_aprobado["COD_ASIGNATURA"].to_numpy()
        test3=curso3 in Curso_rut_aprobado["COD_ASIGNATURA"].to_numpy()
        test4=curso4 in Curso_rut_aprobado["COD_ASIGNATURA"].to_numpy()
        test5=curso5 in Curso_rut_aprobado["COD_ASIGNATURA"].to_numpy()
        test6=curso6 in Curso_rut_aprobado["COD_ASIGNATURA"].to_numpy()
        test7=curso7 in Curso_rut_aprobado["COD_ASIGNATURA"].to_numpy()
        test8=curso8 in Curso_rut_aprobado["COD_ASIGNATURA"].to_numpy()
        test9=curso9 in Curso_rut_aprobado["COD_ASIGNATURA"].to_numpy()
        test10=curso10 in Curso_rut_aprobado["COD_ASIGNATURA"].to_numpy()
        test11=curso11 in Curso_rut_aprobado["COD_ASIGNATURA"].to_numpy()
        test12=curso12 in Curso_rut_aprobado["COD_ASIGNATURA"].to_numpy()
        test13=curso13 in Curso_rut_aprobado["COD_ASIGNATURA"].to_numpy()
        test14=curso14 in Curso_rut_aprobado["COD_ASIGNATURA"].to_numpy()
        test15=curso15 in Curso_rut_aprobado["COD_ASIGNATURA"].to_numpy()
        test16=curso16 in Curso_rut_aprobado["COD_ASIGNATURA"].to_numpy()
        test17=curso17 in Curso_rut_aprobado["COD_ASIGNATURA"].to_numpy()
        test18=curso18 in Curso_rut_aprobado["COD_ASIGNATURA"].to_numpy()
        test19=curso19 in Curso_rut_aprobado["COD_ASIGNATURA"].to_numpy()
        test20=curso20 in Curso_rut_aprobado["COD_ASIGNATURA"].to_numpy()
        test21=curso21 in Curso_rut_aprobado["COD_ASIGNATURA"].to_numpy()
        test22=curso22 in Curso_rut_aprobado["COD_ASIGNATURA"].to_numpy()
        test23=curso23 in Curso_rut_aprobado["COD_ASIGNATURA"].to_numpy()
        test24=curso24 in Curso_rut_aprobado["COD_ASIGNATURA"].to_numpy()
        test25=curso25 in Curso_rut_aprobado["COD_ASIGNATURA"].to_numpy()
        test26=curso26 in Curso_rut_aprobado["COD_ASIGNATURA"].to_numpy()
        test27=curso27 in Curso_rut_aprobado["COD_ASIGNATURA"].to_numpy()
        test28=curso28 in Curso_rut_aprobado["COD_ASIGNATURA"].to_numpy()
        test29=curso29 in Curso_rut_aprobado["COD_ASIGNATURA"].to_numpy()
        test30=curso30 in Curso_rut_aprobado["COD_ASIGNATURA"].to_numpy()
        test31=curso31 in Curso_rut_aprobado["COD_ASIGNATURA"].to_numpy()
        test32=curso32 in Curso_rut_aprobado["COD_ASIGNATURA"].to_numpy()
        test33=curso33 in Curso_rut_aprobado["COD_ASIGNATURA"].to_numpy()
        test34=curso34 in Curso_rut_aprobado["COD_ASIGNATURA"].to_numpy()
        
        
        
        
        
        
        
        
        if test==False and test1==False and test2==False and test3==False and test4==False and test5==False and test6==False and test7==False and test8==False and test9==False and test10==False and test11==False and test12==False and test13==False and test14==False and test15==False and test16==False and test17==False and test18==False and test19==False and test20==False and test21==False and test22==False and test23==False and test24==False and test25==False and test26==False and test27==False and test28==False and test29==False and test30==False and test31==False and test32==False and test33==False and test34==False:
            curso_pendiente.append(aux)    
        else:
            curso_aprobado_segun_plan.append(aux)
        
    largo=len(curso_pendiente)
    a=pd.DataFrame()
    for i in range(largo):
         a=pd.concat([a,curso_pendiente[i]],ignore_index=True)
    curso_pendiente=a
    
    largo=len(curso_aprobado_segun_plan)
    a=pd.DataFrame()
    for i in range(largo):
         a=pd.concat([a,curso_aprobado_segun_plan[i]],ignore_index=True)
    curso_aprobado_segun_plan=a
    
    if curso_aprobado_segun_plan.empty==True:
        
        curso_aprobado_segun_plan["CÓDIGOASIGNATURA"]="Sin"
        curso_aprobado_segun_plan["ASIGNATURA"]="Sin"
        curso_aprobado_segun_plan["NIVEL"]="Sin"
        #curso_aprobado_segun_plan["HOM1"]="Sin"
        #curso_aprobado_segun_plan["HOM2"]="Sin"
        #curso_aprobado_segun_plan["HOM3"]="Sin"
        #curso_aprobado_segun_plan["HOM4"]="Sin"
        #curso_aprobado_segun_plan["HOM5"]="Sin"
        #curso_aprobado_segun_plan["HOM6"]="Sin"
        #curso_aprobado_segun_plan["HOM7"]="Sin"
        #curso_aprobado_segun_plan["HOM8"]="Sin"
        #curso_aprobado_segun_plan["HOM9"]="Sin"
        #curso_aprobado_segun_plan["HOM10"]="Sin"
        
        
    if curso_pendiente.empty==True:
            
        curso_pendiente["CÓDIGOASIGNATURA"]="Sin"
        curso_pendiente["ASIGNATURA"]="Sin"
        curso_pendiente["NIVEL"]="Sin"

        
        
    
    curso_aprobado_segun_plan=curso_aprobado_segun_plan[["CÓDIGOASIGNATURA","ASIGNATURA","NIVEL"]]
    curso_pendiente=curso_pendiente[["CÓDIGOASIGNATURA","ASIGNATURA","NIVEL"]]
    
    return curso_aprobado_segun_plan,curso_pendiente,Homologados[["CÓDIGOASIGNATURA","ASIGNATURA","NIVEL"]],programa,carga_academica_rut


notas,carga,matricula=carga_datos()


todos_rut=matricula["DSC_RUT_DV"].drop_duplicates()
rut=st.selectbox("Ingrese el rut a consultar:",todos_rut)
aprobados,pendientes,malla,programa,cursos_carga=proyeccion(rut,notas,carga,matricula,periodo)
sede,carrera,nombre,apellido_paterno,apellido_materno=datos_alumno(matricula, rut) # informacion del alumno
st.header(f"Avance Curricular ID: {rut}")
st.subheader(f"Nombre: {nombre} {apellido_paterno} {apellido_materno}")
st.subheader(f"Sede: {sede}")
st.subheader(f"Carrera: {carrera}")  


elementos=malla["NIVEL"].drop_duplicates().reset_index()["NIVEL"]



#### se genera la malla con el avance            
columna=st.columns(len(elementos))
cont=0
for i in elementos:
    with columna[cont]:
        st.write(f"**Nivel: {i}**")
        cont=1+cont
    
        nivel=malla[malla["NIVEL"]==i].reset_index()
        for curso in nivel["CÓDIGOASIGNATURA"]:
            nombre=nivel[nivel["CÓDIGOASIGNATURA"]==curso]["ASIGNATURA"].reset_index()
            nombre=nombre["ASIGNATURA"][0]            
        
            if curso in aprobados["CÓDIGOASIGNATURA"].to_list():
                st.markdown(f"""
                <div style="background-color: lightgreen; padding: 8px;border:2px solid black;border-radius:10px;width:92px;height:50px;text-align:center">
                  {curso}
                </div>
                """, unsafe_allow_html=True,help=f"{nombre}")
                st.markdown(
                    """
                    <hr style="dash: 1px solid #ccc; margin: 10px 0;">
                    """,
                    unsafe_allow_html=True
                )
         
            elif cursos_carga.empty!=True and curso in cursos_carga["COD_ASIGNATURA"].to_list():
                st.markdown(f"""
                <div style="background-color: lightblue; padding: 8px;border:2px solid black;border-radius:10px;width:92px;height:50px;text-align:center">
                  {curso}
                </div>
                """, unsafe_allow_html=True,help=f"{nombre}")
                st.markdown(
                    """
                    <hr style="dash: 1px solid #ccc; margin: 10px 0;">
                    """,
                    unsafe_allow_html=True
                )             
            
            
            else:
                st.markdown(f"""
                <div style="background-color: yellow; padding: 8px;;border:2px solid black;border-radius:10px;width:92px;height:50px;text-align:center">
                  {curso}
                </div>
                """, unsafe_allow_html=True,help=f"{nombre}")  
                st.markdown(
                    """
                    <hr style="dash: 1px solid #ccc; margin: 10px 0;">
                    """,
                    unsafe_allow_html=True
                )                              
        


