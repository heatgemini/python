# encoding:UTF-8
import datetime
import json
import sys
from decimal import Decimal

sys.path.append('../common/')
import ChartUtil
import Py3Email


def format_num_2_str(num, format_t='0.00'):
    return str(Decimal(num).quantize(Decimal(format_t)))


if __name__ == '__main__':
    electric_path = 'electric.json'
    data = json.load(open(electric_path, 'rb'))
    now = datetime.datetime.now()
    cur_month = '%s-%s' % (now.year, now.month)
    last_month = '%s-%s' % (now.year, (now.replace(day=1) - datetime.timedelta(days=1)).month)
    cur_mon_data = data[cur_month]
    last_mon_data = data[last_month]
    room_1 = cur_mon_data['room-1'] - last_mon_data['room-1']
    room_2 = cur_mon_data['room-2'] - last_mon_data['room-2']
    room_3 = cur_mon_data['room-3'] - last_mon_data['room-3']
    room_common = cur_mon_data['all'] - room_1 - room_2 - room_3
    data_money = cur_mon_data['money']
    w_fee = data_money / cur_mon_data['all']
    common_room_1 = 0.2 * room_common
    common_room_2 = 0.4 * room_common
    common_room_3 = 0.4 * room_common
    total_room_1 = room_1 + common_room_1
    total_room_2 = room_2 + common_room_2
    total_room_3 = room_3 + common_room_3
    room_1_fee = format_num_2_str(w_fee * total_room_1)
    room_2_fee = format_num_2_str(w_fee * total_room_2)
    room_3_fee = format_num_2_str(w_fee * total_room_3)
    month_zn = str('%s年%s月' % (now.year, now.month))
    table_head = [month_zn, '<b>本月电量</b>', '<b>上月电量</b>', '<b>自用电量</b>', '<b>公共电量</b>', '<b>总电量</b>',
                  '<b>单价（元）</b>', '<b>电费（元）</b>']
    w_fee_str = format_num_2_str(w_fee)
    table_list = [
        ['一号房间', '二号房间', '三号房间', '<b>总计</b>'],
        [str(cur_mon_data['room-1']), str(cur_mon_data['room-2']), str(cur_mon_data['room-3']), '--'],
        [str(last_mon_data['room-1']), str(last_mon_data['room-2']), str(last_mon_data['room-3']), '--'],
        [str(room_1), str(room_2), str(room_3), str(room_1 + room_2 + room_3)],
        [format_num_2_str(common_room_1), format_num_2_str(common_room_2), format_num_2_str(common_room_3),
         str(room_common)],
        [format_num_2_str(total_room_1), format_num_2_str(total_room_2), format_num_2_str(total_room_3),
         str(cur_mon_data['all'])],
        [w_fee_str, w_fee_str, w_fee_str, w_fee_str],
        ['<b>' + str(room_1_fee) + '</b>', '<b>' + str(room_2_fee) + '</b>', '<b>' + str(room_3_fee) + '</b>',
         str(data_money)]]
    electric_file_name = '../image/' + month_zn + '.png'
    ChartUtil.generate_table(table_head, table_list, electric_file_name)
    email_title = month_zn + '-电费汇总'
    email_content = ''
    Py3Email.fast_send('XXXXXXXX@qq.com', email_title, email_content, electric_file_name)
