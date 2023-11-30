import csv
from bs4 import BeautifulSoup
import urllib.request
import requests
import re
import math
import time

#URL一覧を取得
res=requests.get("https://job.mynavi.jp/sitemap_2024_corp_employment.xml")
res.raise_for_status()
soup=BeautifulSoup(res.content,'lxml-xml')
url_list=[]
for d in soup.find_all("loc"):
   url_list.append(d.text)
#URL一覧ここまで

#csvファイルとカラム一行目の準備
file=open("company_treatment.csv","w",encoding='utf-8')
writer = csv.writer(file)
clumn_name=["URL","会社名","業種","基本情報","初任給","支給額(備考)","試用期間","試用期間(備考)","残業","諸手当","昇給","賞与","年間休日数","福利厚生","福利厚生(備考)","受動喫煙防止の取り組み","勤務地","勤務地(備考)","勤務時間","1日あたりの勤務時間","勤務時間(備考)"]
writer.writerow(clumn_name)
#csvファイルの準備ここまで

#後に例外処理を追加
total_items=int(input("取得したい企業の数を整数で入力 20000以上は不可,テスト時は15"))

#各企業のスクレイピングスタート
for i in range(0,total_items):
  progress = (i + 1) / total_items * 100
  print(f"\rProgress: [{int(progress)}%]")

  time.sleep(0.5)
  csvRow=[]

  html = requests.get(url_list[i])
  soup = BeautifulSoup(html.content, 'html.parser')
  print(url_list[i])


#待遇部分全体のクラスを指定
  treatment_section=soup.find(attrs={'class':'dataTable last dataTable02'})


#コース別募集を行なっていた場合ループをスキップ
  if soup.find(attrs={'class':'companySec courseList'}):
       print("true")
       print("------------")
       continue
  print(i)
#コース別募集スキップここまで

#企業情報が公開されていない場合にスキップする
  if soup.find(attrs={'id':'bodyError'}):
     print("企業情報が未公開")
     continue
#スキップここまで




#社名、業種、基本情報の取得ここまで
  company_name=soup.find(attrs={'class':'heading1-inner-left'}).find('h1').text
  print(company_name)
  company_category=soup.find(attrs={'class':'category'}).find('span').text.replace(' ',"")
  print(company_category)
  company_info=soup.find(attrs={'class':'placeItem'}).find('dd').text.replace(' ',"")
  
  print(company_info)  
#社名、業種、基本情報の取得ここまで(company_name company_category company_infoが最終変数)


#初任給セクションの支給額のスクレイピング
  startSarary_table=treatment_section.find(attrs={'id':'startSalary'})
  courseRow=startSarary_table.find_all(attrs={'class':'courseRow'})
  startSarary_list=[]
  for p in courseRow:
     startSarary=p.find(attrs={'class':"courseData"}).find("p").text
     startSarary=re.sub(r"\D","",startSarary)
     startSarary=int(startSarary)
     startSarary_list.append(startSarary)
     
  startSarary_final=math.floor(sum(startSarary_list)/len(startSarary_list))
  print(startSarary_final)
#初任給セクションの支給額のスクレイピングここまで(最終変数はstartSarary_final)

#支給額（備考）
  startSarary_notes=treatment_section.find(attrs={'class':'salaryBreakdown'})
  if startSarary_notes:
     startSarary_notes=startSarary_notes.text
  else:
     startSarary_notes="none"
  print(startSarary_notes)
#支給額（備考）

#試用期間、試用期間（備考）、残業、残業（備考）
  probation_icon=treatment_section.find(attrs={'id':'hasProbation'}).text
  probation_text=treatment_section.find(attrs={'id':'probationText'}).text
  if probation_text==0:
     probation_text='none'
  print(probation_icon)
  print(probation_text)
  overtime=treatment_section.find(attrs={'id':'hasFixedOvertime'}).text
  print(overtime)
#試用期間、残業ここまで(probation_icon probation_text overtimeが最終変数)

#諸手当
  employ_treatment = treatment_section.find(attrs={'id':'employTreatmentListDescText3210'}).text
  print(employ_treatment)
#諸手当ここまで

#昇給
  raise_sarary = treatment_section.find(attrs={'id':'employTreatmentListDescText3220'}).text
  print(raise_sarary)
#昇給ここまで

#賞与
  bonus=treatment_section.find(attrs={'id':'employTreatmentListDescText3230'}).text
  print(bonus)
#賞与ここまで

#年間休日数
  holiday_num=treatment_section.find(attrs={'id':'holidaysNum'})
  if holiday_num:
     holiday_num=holiday_num.text
  else:
     holiday_num="none"
  print(holiday_num)
#年間休日数ここまで

#福利厚生
  hukuri_text=treatment_section.find(attrs={'id':'employTreatmentListDescText3250'}).text
  hukuri_icon=treatment_section.find(attrs={'id':'employTreatmentListDescText3250'}).text
#福利厚生ここまで

#受動喫煙防止の取り組み
  kituenn=treatment_section.find(attrs={'id':'employTreatmentListDescText4230'}).text
#受動喫煙防止の取り組みここまで

#勤務地
  location_icon_section=treatment_section.find(attrs={'id':'workLocation'}).find_all('span')
  location_icon=""
  for p in location_icon_section:
     location_icon+=p.text+"|"
  print(location_icon)

  location_text=treatment_section.find(attrs={'id':'workLocationText'})
  if location_text:
     location_text=location_text.text
  else:
     location_text="none"
     print(location_text.text)
#勤務地ここまで(location_icon location_text)

#勤務時間()
  worktime_section=treatment_section.find(attrs={'id':'workHour'}).find("li")
  try:
    worktime_section.find("dl").find("dt")
    worktime=worktime_section.find("dl").find("dt").text
  except:
    worktime="none"

  try:
    worktime_section.find("dl").find("dd")
    worktime_per_day=worktime_section.find("dl").find("dd").text
  except:
     worktime_per_day="none"

  try:
    worktime_section.find("p")
    worktime_notes=worktime_section.find("p").text
  except:
     worktime_notes="none"

  print(worktime)
  print(worktime_per_day)
  print(worktime_notes)
#勤務時間(worktime,worktime_per_day,worktime_notes))

#こんな学生に会ってみたい
  student_feature=treatment_section.find(attrs={'id':'studentFeature'})
  student_feature_list=""
  if student_feature:
     student_feature=student_feature.find_all("span")
     for p in student_feature:
        student_feature_list+= p.text + "|"
  else:
     student_feature_list="none"
  print(student_feature_list)
#こんな学生に会ってみたいここまで(student_feature_list)

# 採用情報提供方法の特徴
  recruit_featrure=treatment_section.find(attrs={"id":"recruitInfoFeature"})
  recruit_featrure_list=""
  if recruit_featrure:
     for p in recruit_featrure.find_all("span"):
        recruit_featrure_list+=p.text+"|"
  else:
     recruit_featrure_list="none"
  print(recruit_featrure_list)                           
#採用情報提供方法の特徴ここまで

#csv格納
  csvRow.extend([url_list[i],company_name,company_category,company_info,startSarary_final,startSarary_notes,probation_icon,probation_text,overtime,employ_treatment,raise_sarary,bonus,holiday_num,hukuri_icon,hukuri_text,kituenn,location_icon,location_text,worktime,worktime_per_day,worktime_notes])
  writer.writerow(csvRow)
#csv格納ここまで
  


print("------------")

file.close()
print("カレントディレクトリに出力完了、エクセルでの読み込み時はutf-8でデータ→データクエリから取り込むことを忘れない")



