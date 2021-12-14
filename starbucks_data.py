import pandas as pd
#스타벅스 지점 개수와 인구밀도 및 개인소득의 연관성
from matplotlib import font_manager, rc
import matplotlib.pyplot as plt

crowling = pd.DataFrame()
crowling = pd.read_csv('./스타벅스 매장 분포.csv', encoding='cp949')
crowling["count"]= 1 #매장수를 세기위해서 1씩 추가함
crowling=crowling.drop(['store','gungu'],axis=1)
print(crowling)

sido_list=['서울','부산','대구','인천','광주','대전','울산','세종','경기도','강원도','충청북도','충청남도','전라북도','전라남도','경상북도','경상남도','제주']
table=pd.DataFrame(columns=['시도','매장 수']) #빈 데이터프레임 생성 (열:시도, 매장 수 행:없음)
temp1 = pd.DataFrame({'시도':['전국'], '매장 수': [crowling['count'].sum()]})
table = table.append(temp1, ignore_index=True)
for i in sido_list: #지역리스트를 반복하면서
    temp=crowling[crowling['sido'].str.contains(i)] #지역이름을 포함하고 있으면 임시 데이터프레임에 저장
    
    temp=pd.DataFrame({'시도':[i],'매장 수':[temp['count'].sum()]}) #임시 데이터프레임에 지역과 매장수 합을 저장
    table=table.append(temp,ignore_index=True) #매장 수 합친 데이터프레임을 추가하고 인덱스 초기화

table.to_csv('./지역별 스타벅스 매장 수.csv',sep =',',na_rep='NaN', encoding ="utf-8-sig")    
print('==============')
print(table)
print('==============')

starbucks_loca = pd.read_csv('./지역별 스타벅스 매장 수.csv', encoding='UTF-8')
income = pd.read_csv('./시도별_1인당_지역내총생산__지역총소득__개인소득_2019.csv', encoding='cp949')
population = pd.read_csv('./시도별_주민등록_인구현황_2019.csv', encoding='cp949')
area = pd.read_csv('./지역별_면적_2019.csv', encoding='cp949')

starbucks = pd.DataFrame()
starbucks["시도별"] = starbucks_loca["시도"] 
starbucks["총인구 (명)"] = population["총인구 (명)"]
starbucks["1인당 개인소득(단위 : 천원)"] = income["1인당 개인소득"]
starbucks["면적 (㎢)"] = area["면적 (㎢)"]
starbucks["매장 수"] = starbucks_loca["매장 수"]
starbucks["10000명당 스타벅스 매장수"] = round(starbucks["매장 수"]/population["총인구 (명)"]*10000, 2)
starbucks["매장 1개당 지역소득(단위 : 억)"] = round(income["1인당 개인소득"]*population["총인구 (명)"]/starbucks["매장 수"]/100000,2)
starbucks["100㎢당 스타벅스 매장수"] = round(starbucks["매장 수"]/area["면적 (㎢)"]*100,2)
print(starbucks)
print("===================")
starbucks.to_csv('./RESULT.csv',sep =',',na_rep='NaN', encoding ="utf-8-sig")

star_pop = pd.DataFrame()
star_pop["전국 시 ∙ 도별"] = starbucks_loca["시도"]
star_pop["10000명당 스타벅스 매장수"] = round(starbucks["매장 수"]/population["총인구 (명)"]*10000, 2)

star_pop=star_pop.sort_values(by='10000명당 스타벅스 매장수', ascending=False,ignore_index=True)
print(star_pop)

star_per_pop = pd.DataFrame({'location':star_pop["전국 시 ∙ 도별"], 'star/pop': star_pop["10000명당 스타벅스 매장수"]})

font_name = font_manager.FontProperties(fname = "C:/Windows/Fonts/GULIM.TTC").get_name()
rc('font', family = font_name)

ax = star_per_pop.plot(kind = 'bar', fontsize = 15, figsize = (10,4), x='location', y='star/pop', color = 'green')

ax.set_xlabel('전국 시 ∙ 도별', fontsize = 16)
ax.set_ylabel('10000명당 스타벅스 매장수', fontsize = 16)
ax.legend(['10000명 당 스타벅스 매장 수'], fontsize = 13)

plt.show()