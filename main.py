import pandas as pd
import glob
import path as pth
import fnmatch
import os
import datetime
from cvc_report_excel import excel_report
import time
import operator as op
dossier_source = pth.dossier_source_afl
dossier_output = pth.dossier_output_afl+'/'
#Try reset hard
nb_files = len(fnmatch.filter(os.listdir(dossier_source), '*.xlsx'))
dataframe_append = pd.DataFrame()
line = 0
print(nb_files)
for i in range(0, nb_files):
    print(str(i+1)+'/'+str(nb_files))
    nom_fichier = glob.glob(dossier_source+'/*.xlsx')[i]
    print(nom_fichier)
    dataframe = pd.read_excel(nom_fichier,dtype={'Matricule ' : str})
    dataframe  = dataframe[['Date','Matricule','Nom Prénom','Entrée 1','Dernière sortie']]

    fichier = os.path.basename(nom_fichier).replace('.xlsx','')
    dataframe['Fichier'] = fichier
    dataframe_append = pd.concat([dataframe_append,dataframe])
    line += len(dataframe)
    dataframe_append = dataframe_append.reset_index(drop=True)
print('Fin de compilage des fichiers')
dataframe_append = dataframe_append[dataframe_append['Entrée 1'].notna()]
dataframe_append = dataframe_append[dataframe_append['Dernière sortie'].notna()]
dataframe_append['Hours 1'] = dataframe_append['Entrée 1'].dt.time
dataframe_append['Hours 2'] = dataframe_append['Dernière sortie'].dt.time
#dataframe_append['Day 1'] = dataframe_append['Entrée 1'].dt.day
#dataframe_append['Day 2'] = dataframe_append['Dernière sortie'].dt.day


dataframe_append.loc[op.__and__(dataframe_append['Hours 1'] < datetime.time(hour=5,minute=0),dataframe_append['Hours 2'] > datetime.time(hour=0,minute=0)),'Flag Hours 1'] = 1


dataframe_append.loc[op.__and__(dataframe_append['Hours 1'] > datetime.time(hour=0,minute=0),dataframe_append['Hours 2'] <= datetime.time(hour=5,minute=0)),'Flag Hours 1'] = 1
dataframe_append.loc[op.__and__(dataframe_append['Hours 1'] > datetime.time(hour=0,minute=0),op.__and__(dataframe_append['Hours 2'] >= datetime.time(hour=5,minute=0),dataframe_append['Hours 2'] < dataframe_append['Hours 1'])),'Flag Hours 1'] = 1

dataframe_append['Flag Hours 1'] = dataframe_append['Flag Hours 1'].fillna(0)
dataframe_append = dataframe_append[dataframe_append['Flag Hours 1'] == 1]

dataframe_append.loc[dataframe_append['Hours 1'] >= datetime.time(hour=5,minute=0),'R Hours 1'] = datetime.time(hour=0,minute=0)
dataframe_append.loc[dataframe_append['Hours 1'] < datetime.time(hour=5,minute=0),'R Hours 1'] = dataframe_append['Hours 1']
dataframe_append.loc[dataframe_append['Hours 2'] >= datetime.time(hour=5,minute=0),'R Hours 2'] = datetime.time(hour=5,minute=0)
dataframe_append.loc[dataframe_append['Hours 2'] < datetime.time(hour=5,minute=0),'R Hours 2'] = dataframe_append['Hours 2']

dataframe_append['val_hours_e'] = dataframe_append['R Hours 1'].astype(str)
#dataframe_append['val_hours'] = dataframe_append['val_hours'].str.split(r":+",regex=True)
dataframe_append['val_hours1'] = dataframe_append['val_hours_e'].str.extract('^(\d+)',expand=True)
dataframe_append['val_hours1'] = dataframe_append['val_hours1'].astype(int)
dataframe_append['val_hours2'] = dataframe_append['val_hours_e'].str.extract('^\d+:(\d+)',expand=True)
dataframe_append['val_hours2'] = round(dataframe_append['val_hours2'].astype(int)/60,2)
dataframe_append['V_E'] = dataframe_append['val_hours1'] + dataframe_append['val_hours2']

dataframe_append['val_hours_s'] = dataframe_append['R Hours 2'].astype(str)
#dataframe_append['val_hours'] = dataframe_append['val_hours'].str.split(r":+",regex=True)
dataframe_append['val_hours3'] = dataframe_append['val_hours_s'].str.extract('^(\d+)',expand=True)
dataframe_append['val_hours3'] = dataframe_append['val_hours3'].astype(int)
dataframe_append['val_hours4'] = dataframe_append['val_hours_s'].str.extract('^\d+:(\d+)',expand=True)
dataframe_append['val_hours4'] = round(dataframe_append['val_hours4'].astype(int)/60,2)
dataframe_append['V_S'] = dataframe_append['val_hours3'] + dataframe_append['val_hours4']
dataframe_append['Elig_pen'] = dataframe_append['V_S']-dataframe_append['V_E']
dataframe_append = dataframe_append[['Date','Matricule','Nom Prénom','Entrée 1','Dernière sortie','Hours 1','Hours 2','Elig_pen']]
dataframe_append = dataframe_append.rename(columns={'Hours 1' : 'Heures entrée'})
dataframe_append = dataframe_append.rename(columns={'Hours 2' : 'Heures sortie'})
dataframe_append = dataframe_append[dataframe_append['Elig_pen'] >= 1]
dataframe_append.loc[dataframe_append['Elig_pen'] >= 1,'Elig_pen'] = 1
dataframe_append.loc[dataframe_append['Elig_pen'] < 1,'Elig_pen'] = 0
excel_report(dataframe_append,dossier_output+'Outputs_penibilité analyse.xlsx')
dataframe_append = dataframe_append.groupby(by=['Matricule','Nom Prénom'])['Elig_pen'].agg('sum').reset_index().fillna(0)
dataframe_append.loc[dataframe_append['Elig_pen'] >= 120,'Flag_penibility'] = 'O'
dataframe_append.loc[dataframe_append['Elig_pen'] < 120,'Flag_penibility'] = 'N'
excel_report(dataframe_append,dossier_output+'Outputs_penibilité détail.xlsx')
dataframe_append = dataframe_append[dataframe_append['Flag_penibility'] == 'O']
dataframe_append['Code PAC'] = '900112'
dataframe_append['Mois de paie\nFormat: AAAAMM'] = '202206'
dataframe_append['S21.G00.34.001\nFacteur d\'exposition\nFormat : X(2)'] = '08'
dataframe_append['S21.G00.34.003\nAnnée de rattachement\nFormat : N(4)'] = '2021'
dataframe_append = dataframe_append[['Code PAC','Mois de paie\nFormat: AAAAMM','Matricule','S21.G00.34.001\nFacteur d\'exposition\nFormat : X(2)','S21.G00.34.003\nAnnée de rattachement\nFormat : N(4)']]
excel_report(dataframe_append,dossier_output+'Outputs_penibilité.xlsx')

