import pandas as pd

# etag_df = pd.read_csv('eTagStatic.csv')
# etag_df['DatetimeCol'] = pd.to_datetime(etag_df['DatetimeCol'])
# etag_df['TravelTimeSum'] = etag_df.groupby(["SectionID", pd.Grouper(key='DatetimeCol', freq='1h')])['TravelTime'].transform('sum')
# etag_df = etag_df[etag_df['SectionID'] == '007-060-006-060']
# etag_df2 = etag_df.groupby(["SectionID", pd.Grouper(key='DatetimeCol', freq='1h')]).TravelTime.agg('sum').reset_index()
# etag_df2 = etag_df2[etag_df2['SectionID'] == '007-060-006-060']
#

import asyncio
import logging
import re
import time
import cmsCommandLib

logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(message)s', datefmt='%m-%d %H:%M:%S')
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)

async def CMS_writer(writer):
    '''
    寫入CMS的指令
    '''
    message = cmsCommandLib.commandAF13(100,10,0)
    logging.info(message.hex())
    writer.write(message)
    logging.info(f'WriteCMS:{message.hex()}')

async def CMS_reader(host, port):
    '''
    讀出CMS的指令
    '''
    reader, writer = await asyncio.open_connection(host,port)

    buffer = bytearray()
    asyncio.create_task(CMS_writer(writer))

    while True:
        data = await reader.read(1024)
        if len(data) > 0:
            logging.debug("ReadCMS:{}".format(data.hex()))

def main():
    asyncio.run(CMS_reader("192.168.16.49",8888))

if __name__ == '__main__':
    main()
