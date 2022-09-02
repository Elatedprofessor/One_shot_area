from cvc_path_map import self_user_path

homedir = self_user_path()

dossier_source_afl = homedir + '/CV Consultants Dropbox/Travail clients CV Consultants/AMAZON/2022/06-2022/PENIBILITY 2021/AFL/WorkDocs-Bulk-Download-24-06-2022 15_00_12/01-Sources'
dossier_output_afl = homedir + '/CV Consultants Dropbox/Travail clients CV Consultants/AMAZON/2022/06-2022/PENIBILITY 2021/AFL/WorkDocs-Bulk-Download-24-06-2022 15_00_12/02-Outputs'
dossier_source_aft = homedir + '/CV Consultants Dropbox/Travail clients CV Consultants/AMAZON/2022/06-2022/PENIBILITY 2021/AFT/WorkDocs-Bulk-Download-24-06-2022 15_18_38/01-Sources'
dossier_output_aft = homedir + '/CV Consultants Dropbox/Travail clients CV Consultants/AMAZON/2022/06-2022/PENIBILITY 2021/AFT/WorkDocs-Bulk-Download-24-06-2022 15_18_38/02-Outputs'

filename1 = '06- 2022 POPULATION PRE CONTROLE CHASSENEUIL.xls'
filename2 = 'Pré controle 06 2022 - GB.xls'
filename3 = 'Pré controle 06 2022 - SB.xls'
filename4 = 'Pré controle.xls'
filename5 = 'Précontrole Juin 2022.xlsx'
filename6 = 'Precontrole JUIN22.xls'
filename7 = ''

def filepath(dossier, filename):
    filepath = dossier + filename
    return filepath


