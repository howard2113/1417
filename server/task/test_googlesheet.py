import gspread
from datetime import datetime
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials as SAC


Json = 'alpine-sentry-325407-58063405de05.json'  # Json 的單引號內容請改成個人下載的金鑰
Url = ['https://spreadsheets.google.com/feeds']

Connect = SAC.from_json_keyfile_name(Json, Url)
GoogleSheets = gspread.authorize(Connect)

# https://docs.google.com/spreadsheets/d/1KuPK5ABV50IeB95akCf-B6bTAnFJGMLR5GueeepRdlA/edit?resourcekey#gid=592949417
Sheet = GoogleSheets.open_by_key('1sK5DndzfpR1FV1yx-jQmbhr8riYMYRX9HOrr8jLOkbk') # 這裡請輸入妳自己的試算表代號
st_1 = Sheet.sheet1
moto_data_list = st_1.get_all_records()

moto_data_df = pd.DataFrame(moto_data_list)
moto_data_df['時間戳記'] = moto_data_df['時間戳記'].str.replace('上午', 'AM')
moto_data_df['時間戳記'] = moto_data_df['時間戳記'].str.replace('下午', 'PM')

moto_data_df['datetime'] = pd.to_datetime(moto_data_df['時間戳記'], format='%Y/%m/%d %p %I:%M:%S')

for idx, moto_data in moto_data_df.iterrows():
    src_time = datetime.strptime(moto_data['時間戳記'].replace('上午', 'AM').replace('下午', 'PM'), '%Y/%m/%d %p %I:%M:%S')
    a=moto_data_df['datetime'][idx]
    tt = src_time==a
    print(tt)



moto_data_df['時間戳記'] = pd.to_datetime(moto_data_df['時間戳記'])
moto_data_df.sort_values('時間戳記', inplace=True)
moto_data_df.drop_duplicates(subset=['停車場'], keep='last', inplace=True)
print(moto_data_list)