# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 09:37:59 2020

@author: jejia
"""
    #open database connection = ODBC
import csv
import pyodbc
import pandas as pd

    #loop through all drivers we have acces to
#for driver in pyodbc.drivers():
#    print (driver)
#%%




#test with single table
#cursor = conn.cursor()
#dftest = cursor.execute('SELECT*FROM TrainingODS_Test.dbo.Assessment')
#with open(r'C:\Users\jejia\Desktop\DataScience\1 data pilots\Chaojin1.csv', 'w', newline='') as csvfile:
#    writer = csv.writer(csvfile)
#    writer.writerow([x[0] for x in cursor.description])  # column headers
#    for row in dftest:

#        writer.writerow(row)

#conn.setencoding(cursor, conn)
#for row in cursor:

#cursor.to_csv(r'C:\Users\jejia\Desktop\DataScience\1 data pilots\Chaojin1.csv')
    
#%%

startDate = '2019-07-01'
endDate = '2019-12-31' 
query_session ='''
SELECT distinct
         
            TrainingSession.TrainingSessionId,
            TrainingSession.StartTime as TrainingSessionStartTime,
            TrainingSession.EndTime as TrainingSessionEndTime,
            Assessment.AssessmentId,
            AssessmentDefinition.Name as AssessmentName,
            Assessment.StartTime as AssessmentStartTime,
            Assessment.EndTime as AssessmentEndTime,
            AssessmentCrewMember.AssessmentCrewMemberId,
            AssessmentCrewMember.CrewMemberId,
            AssessmentRole.Name as AssessmentRoleName,
            CASE
                WHEN AssessmentCrewMember.OverallGrade='PASS' or AssessmentCrewMember.OverallGrade='PPASS' THEN 'PASS'
                WHEN AssessmentCrewMember.OverallGrade='FAIL' THEN 'FAIL'
                ELSE null
            END as OverallGrade,
            TrainingCompetency.Name as CompetencyName,
            /*TrainingCompetencyAssessment.Grade as CompetencyGrade,   */
            CASE
                WHEN TrainingCompetencyAssessment.Grade='1' THEN 1
                WHEN TrainingCompetencyAssessment.Grade='2' THEN 2
                WHEN TrainingCompetencyAssessment.Grade='3' THEN 3
                WHEN TrainingCompetencyAssessment.Grade='4' THEN 4
                ELSE null
            END as CompetencyGrade,
            AssessmentCrewMember.TrainingRecommended as RemedialTrainingRec,
            TeachingPoint.TeachingPointId,
            TeachingPointDefinition.Name as TeachingPointName,
            TrainingEventDefinition.TrainingEventDefinitionId,
            TrainingEventDefinition.Name as TrainingEventName,
            CASE
                WHEN TeachingPoint.Grade='1' THEN 1
                WHEN TeachingPoint.Grade='2' THEN 2
                WHEN TeachingPoint.Grade='3' or TeachingPoint.Grade='PERF' or TeachingPoint.Grade='NPERF' THEN 3
                WHEN TeachingPoint.Grade='4' THEN 4
                ELSE null
            END as InstructorGrade,

            TeachingPoint.Comment as TeachingPointComment,
          
            TC.Name as FlaggedCompetencyName,
            TrainingCompetencyIndicator.Name as FlaggedBehaviorIndicatorName,
                                    TeachingPointCompetencyIndicatorAssessment.Comment as FlaggedBehaviorIndicatorComment,
          
            Scorecard.ScorecardId,
            Scorecard.TrainingEventStart,
            Scorecard.TrainingEventStop,
            Scorecard.SuggestedGrade as OAGrade,
            ScorecardBelowStandardCriteria.Grade as ReasonGrade,
            BelowStandardCriteriaReason.Reason,
          
            SentinelAircraftType.Model,
            SentinelTrainingDevice.DeviceKey,
          
            Person.Email as TrainingInstructorEmail,
            Customer.Name as CustomerName
        FROM
            TeachingPoint
            /* Training Event Definition */
            LEFT JOIN TeachingPointDefinition ON TeachingPoint.TeachingPointDefinitionId = TeachingPointDefinition.TeachingPointDefinitionId
            LEFT JOIN TrainingEventDefinition ON TeachingPointDefinition.EventDefinitionId = TrainingEventDefinition.TrainingEventDefinitionId
      
            /* Scorecards */
            LEFT JOIN AssessmentCrewMember ON TeachingPoint.AssessmentCrewMemberId = AssessmentCrewMember.AssessmentCrewMemberId
            LEFT JOIN Scorecard       ON (AssessmentCrewMember.AssessmentCrewMemberId = Scorecard.AssessmentCrewMemberId
                                     AND TrainingEventDefinition.TrainingEventDefinitionId=Scorecard.TrainingEventDefinitionId)
          
                   
            /* Assessment Role */
            LEFT JOIN AssessmentRole       ON AssessmentRole.AssessmentRoleId = AssessmentCrewMember.AssessmentRoleId
      
            /* Training Device */
            left JOIN Assessment                ON AssessmentCrewMember.AssessmentId = Assessment.AssessmentId
            left JOIN TrainingSession           ON TrainingSession.TrainingSessionId = Assessment.TrainingSessionId
            left JOIN TrainingSessionInstructor ON TrainingSession.TrainingSessionId = TrainingSessionInstructor.TrainingSessionId
            left JOIN PairingSession            ON PairingSession.PairingSessionId = TrainingSessionInstructor.PairingSessionId
            left JOIN SentinelTrainingDevice    ON SentinelTrainingDevice.TrainingDeviceId =  PairingSession.TrainingDeviceId
            left JOIN SentinelAircraftType      ON SentinelAircraftType.AircraftTypeId =  SentinelTrainingDevice.AircraftTypeId

            /* Customer */
            left JOIN AssessmentDefinition ON Assessment.AssessmentDefinitionId = AssessmentDefinition.AssessmentDefinitionId
            left JOIN Customer             ON AssessmentDefinition.CustomerId   = Customer.CustomerId
          
            /* Instructor */
            left JOIN Person                    ON TrainingSessionInstructor.InstructorId = Person.PersonId
          
            /* Competency */   
            LEFT JOIN TrainingCompetencyAssessment ON AssessmentCrewMember.AssessmentCrewMemberId = TrainingCompetencyAssessment.AssessmentCrewMemberId
            LEFT JOIN TrainingCompetency ON TrainingCompetencyAssessment.TrainingCompetencyId = TrainingCompetency.TrainingCompetencyId
            LEFT JOIN TeachingPointCompetencyIndicatorAssessment ON TeachingPoint.TeachingPointId =TeachingPointCompetencyIndicatorAssessment.TeachingPointId
            LEFT JOIN TrainingCompetencyIndicator ON    TeachingPointCompetencyIndicatorAssessment.TrainingCompetencyIndicatorId =     TrainingCompetencyIndicator.TrainingCompetencyIndicatorId
            LEFT JOIN TrainingCompetency TC ON TrainingCompetencyIndicator.TrainingCompetencyId = TC.TrainingCompetencyId

          
            /* Reasons below criteria */
            LEFT JOIN ScorecardBelowStandardCriteria ON Scorecard.ScorecardId                                        = ScorecardBelowStandardCriteria.ScorecardId
            LEFT JOIN BelowStandardCriteriaReason    ON ScorecardBelowStandardCriteria.BelowStandardCriteriaReasonId = BelowStandardCriteriaReason.BelowStandardCriteriaReasonId
                 
        WHERE
            TrainingSession.StartTime >= CONVERT(DATETIME,'2019-07-01')
            AND TrainingSession.EndTime <= CONVERT(DATETIME,'2019-12-31')
            AND AssessmentDefinition.Name like '%AirAsia REC%'
            and AssessmentDefinition.Name like '%Jul%'
            and (AssessmentRole.AssessmentRoleId = '2' OR AssessmentRole.AssessmentRoleId = '3')
            and TeachingPoint.Grade is not null
            and Person.Email like '%airasia%'
            and Customer.name like '%Air Asia%' or Customer.name like '%AirAsia%'
   

'''.format(startDate, endDate, 'Jul')
#%%
def JoinDB():
    conn = pyodbc.connect(
            'DRIVER={SQL Server};\
            SERVER=gacptest.database.windows.net;DATABASE=trainingODS-test;\
            UID=gacp;PWD=Password1234')
            
    cur = conn.cursor()
    dftest = cur.execute(query_session)
    results = cur.fetchall
    fields = cur.description 
    return list (results), list(fields)

S = JoinDB()
results=S[0]
fields=S[1]
def writer_file(results,fields):
    ##查看文件大小
    file_size = os.path.getsize(r'C:\Users\jejia\Desktop\DataScience\1 data pilots\Chaojin5.csv')
    if file_size == 0:
        ##表头
        name=[]
        results_list=[]
        for  i  in  range(len(fields)):
            name.append(fields[i][0])
        print(name)
        for  i  in  range(len(results)):
            results_list.append(results[i])
        ##建立DataFrame对象
        file_test = pd.DataFrame(columns=name, data=results_list)
        ##数据写入,不要索引
        file_test.to_csv(r'C:\Users\jejia\Desktop\DataScience\1 data pilots\Chaojin5.csv', encoding='utf-8', index=False)
    else:
        with  open(r'C:\Users\jejia\Desktop\DataScience\1 data pilots\Chaojin5.csv', 'a+', newline='') as  file_test:
            ##追加到文件后面
            writer = csv.writer(file_test)
            ##写文件
            writer.writerows(results)


if __name__ == '__main__':
    writer_file(results,fields)








#%%

with open(r'C:\Users\jejia\Desktop\DataScience\1 data pilots\Chaojin.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow([x[0] for x in cursor1.description])  # column headers
    for row in dftest:
#conn.setencoding(cursor, conn)
#for row in cursor:
        writer.writerow(row)
        
        
#df = pd.read_sql(query_session, conn)
#conn.setencoding(query_session, conn)

#df.to_csv(r'C:\Users\jejia\Desktop\DataScience\1 data pilots\Chaojin.csv')


