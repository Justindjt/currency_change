"""
作者:Justin
功能:汇率兑换
"""

import requests
from bs4 import BeautifulSoup
import re


def calculate_data(currency_data, user_number):
    """计算用户兑换数目"""
    currency_calculate_data = round(currency_data * user_number, 2)
    print('您兑换的数目是：{}\n'.format(currency_calculate_data))


def get_currency_data(url_data, url_soup, user_choose):
    """获取汇率信息"""
    currency_name_dict = {}
    currency_county_en_name = re.findall('\((.*?)\)', url_soup.find('optgroup', {'label': '常用货币'}).text)
    currency_county_ch_name = re.findall('(.*?)\(', url_soup.find('optgroup', {'label': '常用货币'}).text)
    currency_name_dict = dict(zip(currency_county_en_name, currency_county_ch_name))
    if user_choose == '1':
        user_want = input('请问你需要兑换哪种货币（输入货币英文）：')
        user_number = float(input('请输入需要兑换的数目： '))
        patten_data = '人民币 = (.*?) <a href=' \
                      '"rate_{}.aspx">{}'.format(user_want.upper(), currency_name_dict[user_want.upper()])
        currency_data = float(re.findall(patten_data, url_data.text)[0])
        calculate_data(currency_data, user_number)
        # print(int_data)
    elif user_choose == '2':
        user_want = input('请问你需要哪种货币兑换哪种货币（输入货币大写英文，以空格相间）：')
        user_number = float(input('请输入需要兑换的数目： '))
        user_want_str = user_want.split(' ')
        user_want1 = user_want_str[0].upper()
        user_want2 = user_want_str[1].upper()
        patten_data1 = '人民币 = (.*?) <a href=' \
                        '"rate_{}.aspx">{}'.format(user_want1, currency_name_dict[user_want1])
        patten_data2 = '人民币 = (.*?) <a href=' \
                         '"rate_{}.aspx">{}'.format(user_want2, currency_name_dict[user_want2])
        currency_data1 = re.findall(patten_data1, url_data.text)
        currency_data2 = re.findall(patten_data2, url_data.text)
        currency_data = float(currency_data2[0])/float(currency_data1[0])
        calculate_data(currency_data, user_number)
        # print(int_data)
    else:
        print('你已退出程序,欢迎您的使用!!')
        return False

    return True


def main():
    """主函数"""
    response = requests.get('http://hl.anseo.cn/')
    currency_soup = BeautifulSoup(response.text, 'lxml')
    currency_county_name = currency_soup.find('optgroup', {'label': '常用货币'}).text.strip().split('\n')
    print('目前只支持兑换以下货币：{}'.format('  '.join(currency_county_name[1:])))
    flag = True
    while flag:
        user_choose = input('若需要人民币兑换外币，请输入1\n若需要不同外币间兑换，请输入2\n'
                        '若需要退出程序，请输入Q。:  ')
        flag = get_currency_data(response, currency_soup, user_choose)


if __name__ == '__main__':
    main()
