# coding: utf-8
import urllib
from bs4 import BeautifulSoup                    #beautifulsoup
from selenium import webdriver                   #selenium
from selenium.webdriver.support.ui import Select
import time
import json
import re
from datetime import datetime
import string
import subprocess
import types
import sys
import random
import pymysql

dbURL = "localhost"
dbUser = "spring"
dbPass = "book"
dbPort = 3306
dbName = "cfp"

conn = pymysql.connect(host=dbURL, port=dbPort, user=dbUser, passwd=dbPass, db=dbName, charset='utf8', use_unicode=True)


def getRecordsEqualJournalTitle(journal_title):
    cur = conn.cursor()
    sql_selectJournalsLikeJournalTitle = """SELECT * FROM {0}.cfp_journal WHERE cfp_type = "Regular" and title = "{1}" """.format(dbName, journal_title)
    cur.execute(sql_selectJournalsLikeJournalTitle)
    results = cur.fetchall()
    return results


list1 = [['bus'], ['chm'], ['eng'], ['med'], ['hum'], ['bio'], ['phy'], ['soc']] #여덟개 상위항목들.
list2 = [
        ['_accountingtaxation','_busgeneral','_developmenteconomics','_economichistory','_economicpolicy','_economics','_educationaladministration','_emergencymanagement','_entrepreneurshipinnovation','_finance','_gametheorydecisionscience','_humanresourcesorganizations','_internationalbusiness','_marketing','_strategicmanagement','_tourismhospitality'],
        ['_analyticalchemistry','_biochemistry','_ceramicengineering','_chmgeneral','_chemicalkineticscatalysis','_combustionpropulsion','_compositematerials','_crystallographystructuralchemistry','_dispersionchemistry','_electrochemistry','_inorganicchemistry','_materialsengineering','_medicinalchemistry','_molecularmodeling','_nanotechnology','_oilpetroleumnaturalgas','_organicchemistry','_polymersplastics'],
        ['_architecture','_artificialintelligence','_automationcontroltheory','_aviationaerospace','_bioinformatics','_biomedicaltechnology','_biotechnology','_ceramicengineering','_civilengineering','_combustionpropulsion','_computationallinguistics','_computergraphics','_computerhardwaredesign','_computernetworkswirelesscommunication','_computersecuritycryptography','_computervisionpatternrecognition','_computingsystems','_datamininganalysis','_databasesinformationsystems','_educationaltechnology','_enggeneral','_environmentalgeologicalengineering','_evolutionarycomputation','_foodsciencetechnology','_fuzzysystems','_gametheorydecisionscience','_humancomputerinteraction','_informationtheory','_libraryinformationscience','_manufacturingmachinery','_materialsengineering','_mechanicalengineering','_medicalinformatics','_metallurgy','_microelectronicselectronicpackaging','_miningmineralresources','_molecularmodeling','_multimedia','_nanotechnology','_oceanmarineengineering','_oilpetroleumnaturalgas','_operationsresearch','_plasmafusion','_powerengineering','_qualityreliability','_radarpositioningnavigation','_remotesensing','_robotics','_signalprocessing','_softwaresystems','_structuralengineering','_sustainableenergy','_technologylaw','_textileengineering','_theoreticalcomputerscience','_transportation','_watersupplytreatment','_woodsciencetechnology'],
        ['_addiction','_aidshiv','_alternativetraditionalmedicine','_anesthesiology','_audiologyspeechlanguagepathology','_bioethics','_biomedicaltechnology','_cardiology','_childadolescentpsychology','_clinicallaboratoryscience','_communicablediseases','_criticalcare','_dentistry','_dermatology','_developmentaldisabilities','_diabetes','_emergencymedicine','_endocrinology','_epidemiology','_gastroenterologyhepatology','_geneticsgenomics','_gerontologygeriatricmedicine','_gynecologyobstetrics','_medgeneral','_heartthoracicsurgery','_hematology','_hospicepalliativecare','_immunology','_medicalinformatics','_medicinalchemistry','_molecularbiology','_naturalmedicinesmedicinalplants','_neurology','_neurosurgery','_nuclearmedicineradiotherapymolecularimaging','_nursing','_nutritionscience','_obesity','_oncology','_ophthalmologyoptometry','_oralmaxillofacialsurgery','_orthopedicmedicinesurgery','_otolaryngology','_painpainmanagement','_pathology','_pediatricmedicine','_pharmacologypharmacy','_physicaleducationsportsmedicine','_physiology','_plasticreconstructivesurgery','_pregnancychildbirth','_primaryhealthcare','_psychiatry','_psychology','_publichealth','_pulmonology','_radiologymedicalimaging','_rehabilitationtherapy','_reproductivehealth','_rheumatology','_socialpsychology','_surgery','_toxicology','_transplantation','_tropicalmedicineparasitology','_urologynephrology','_vascularmedicine','_veterinarymedicine','_virology'],
        ['_africanstudieshistory','_americanliteraturestudies','_asianstudieshistory','_canadianstudieshistory','_chinesestudieshistory','_communication','_dramatheaterarts','_englishlanguageliterature','_epistemologyscientifichistory','_ethnicculturalstudies','_feminismwomensstudies','_film','_foreignlanguagelearning','_frenchstudies','_genderstudies','_history','_humgeneral','_languagelinguistics','_latinamericanstudies','_literaturewriting','_middleeasternislamicstudies','_musicmusicology','_philosophy','_religion','_sexsexuality','_visualarts'],
        ['_agronomycropscience','_animalbehavior','_animalhusbandry','_atmosphericsciences','_biochemistry','_biodiversityconservationbiology','_bioinformatics','_biophysics','_biotechnology','_birds','_botany','_cellbiology','_developmentalbiologyembryology','_ecology','_environmentalgeologicalengineering','_environmentalsciences','_evolutionarybiology','_foodsciencetechnology','_forestsforestry','_geochemistrymineralogy','_geology','_hydrology','_insectsarthropods','_biogeneral','_marinesciencesfisheries','_microbiology','_molecularbiology','_mycology','_oceanography','_paleontology','_pestcontrolpesticides','_plantpathology','_proteomicspeptides','_soilsciences','_sustainabledevelopment','_sustainableenergy','_virology','_woodsciencetechnology','_zoology'],
        ['_acousticssound','_algebra','_astronomyastrophysics','_biophysics','_computationalmathematics','_condensedmatterphysicssemiconductors','_discretemathematics','_electromagnetism','_fluidmechanics','_geometry','_geophysics','_highenergynuclearphysics','_mathematicalanalysis','_mathematicaloptimization','_mathematicalphysics','_nonlinearscience','_opticsphotonics','_phygeneral','_plasmafusion','_probabilitystatistics','_pureappliedmathematics','_quantummechanics','_spectroscopymolecularphysics','_thermalsciences'],
        ['_academicpsychologicaltesting','_africanstudieshistory','_anthropology','_archaeology','_architecture','_asianstudieshistory','_bioethics','_canadianstudieshistory','_chinesestudieshistory','_cognitivescience','_criminologycriminallawpolicing','_developmenteconomics','_diplomacyinternationalrelations','_earlychildhoodeducation','_economichistory','_education','_educationaladministration','_educationalpsychologycounseling','_educationaltechnology','_environmentaloccupationalmedicine','_environmentallawpolicy','_epistemologyscientifichistory','_ethics','_europeanlaw','_familystudies','_feminismwomensstudies','_forensicscience','_geographycartography','_healthpolicymedicallaw','_highereducation','_history','_humanmigration','_humanresourcesorganizations','_internationallaw','_law','_libraryinformationscience','_middleeasternislamicstudies','_militarystudies','_paleontology','_politicalscience','_publichealth','_publicpolicyadministration','_scienceengineeringeducation','_sexsexuality','_socgeneral','_socialwork','_sociology','_specialeducation','_sustainabledevelopment','_teachingteachereducation','_technologylaw','_urbanstudiesplanning']
        ]

argument = int(sys.argv[1])

if argument == 0:  # case of macOS
    driver = webdriver.Firefox(executable_path='/Users/yhhan/git/crawl/crawlPython/geckodriver')
else:
    driver = webdriver.Chrome("C:\chromedriver.exe")        #크롬드라이버로딩?

SiteURL = ["https://scholar.google.co.kr/citations?view_op=top_venues&hl=ko&vq="]  #Google Scholar 첫페이지 url
    
html = driver.page_source
soup = BeautifulSoup(html, "lxml")

maxSleepTime = 2

journal_dic_final_1 = {} ## 전체저널을 담는 리스트 실질적으로는 이차원리스트
journal_dic_final_2 = {} ## 전체저널을 담는 리스트 실질적으로는 이차원리스트

for i in range(len(list1)):
    for text in list1[i]:
        j=0
        for text2 in list2[i]:
            j+=1
            url = SiteURL[0] + text + text2
            driver.get(url)

            minRan = random.randrange(0, maxSleepTime)
            time.sleep(minRan)

            html = driver.page_source
            soup = BeautifulSoup(html, "lxml")
            table = soup.find('table', attrs={'id':'gs_kit_list_table'})
            table = BeautifulSoup(html, "lxml")
            table_body = table.find('tbody')   
            table_body = BeautifulSoup(html, "lxml")
            rows       = table_body.find_all('tr') 
            rows2 = rows[1:]
           
            for row in rows2:
                cells    = row.findAll('td')
                ##rank     = cells[0].find(text=True)
                name     = cells[1].find(text=True)
                index    = cells[2].find(text=True)

                journal_name = name.replace("'", "\'")

                if journal_name in journal_dic_final_1:
                    journal_subject_list = journal_dic_final_1[journal_name]
                else:
                    journal_subject_list = []
                journal_subject_list.append("%d.%d" % (i,j))
                journal_dic_final_1[journal_name] = journal_subject_list

                if journal_name not in journal_dic_final_2:
                    journal_dic_final_2[journal_name] = index

driver.close()
driver.quit()

print len(journal_dic_final_1)
print len(journal_dic_final_2)

total_len = len(journal_dic_final_1)

num = 0

for journal_name in journal_dic_final_1.keys():
    db_results = getRecordsEqualJournalTitle(journal_name.encode('ascii', errors = 'ignore'))

    if journal_name != 'Remote Sensing' and len(db_results) > 1:
        print "Two or more journal names:", journal_name
        sys.exit(1)
    elif len(db_results) == 1:
        num += 1
        current_h2_idnex = db_results[0][5]
        journal_id = db_results[0][0]
        print "Already Exist:", journal_name, journal_id, current_h2_idnex

        updateRegularJournalSql = """UPDATE {0}.cfp_journal SET h2_index = %s WHERE id = %s""".format(dbName)
        cur = conn.cursor()
        cur.execute(updateRegularJournalSql,(journal_dic_final_2[journal_name], journal_id));
        conn.commit()
    elif journal_name == 'Remote Sensing' or len(db_results) == 0:
        cur = conn.cursor()
        ##cfp_journal_id 설정(최신화)
        cfp_journal_id = ''.join(random.SystemRandom().choice(string.ascii_uppercase) for _ in range(8)) + ''.join(random.SystemRandom().choice(string.digits) for _ in range(8)) + 'J'
        h2_index = journal_dic_final_2[journal_name]
        
        insertRegularJournalSql = """INSERT INTO {0}.cfp_journal (cfp_journal_id,title,h2_index,cfp_type,added_datetime) VALUES(%s, %s, %s, 'Regular', now());""".format(dbName)
       
        cur.execute(insertRegularJournalSql,(cfp_journal_id, journal_name, h2_index));
        last_journal_id = conn.insert_id()
        
        print "New:", journal_name, last_journal_id, h2_index #id 출력, title 출력

        for subject in journal_dic_final_1[journal_name]:
            selectJournalIDsubjectID = """SELECT * FROM {0}.cfp_journal_subject WHERE journal_id = %s and subject = %s;""".format(dbName)
            cur.execute(selectJournalIDsubjectID, (last_journal_id, subject));
            result = cur.fetchone()
            if result is None:
                insertJournalSubjectSql = """INSERT INTO {0}.cfp_journal_subject(journal_id, subject, added_datetime) VALUES(%s, %s, now());""".format(dbName)
                cur.execute(insertJournalSubjectSql, (last_journal_id, subject));

conn.commit()
conn.close()
print "Number of existing journals:", num
print "Insert Finished!"