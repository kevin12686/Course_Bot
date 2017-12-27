import sys
import requests
import re
import time
from bs4 import BeautifulSoup

from NID import Username, Password, Course

code_url = 'https://course.fcu.edu.tw/validateCode.aspx'
login_url = 'https://course.fcu.edu.tw/Login.aspx'

loginFind_payload = ['__EVENTARGUMENT', '__LASTFOCUS', '__VIEWSTATE', '__VIEWSTATEGENERATOR',
                     '__EVENTVALIDATION']

header = {
    'Connection': 'Keep-Alive',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:57.0) Gecko/20100101 Firefox/57.0'
}


def get_code(Session):
    return Session.get(code_url).cookies['CheckCode']


def get_login_payload(Session, NID, PASS):
    payload = dict()
    soup = BeautifulSoup(Session.get(login_url).text, 'html.parser')
    payload['__EVENTTARGET'] = 'ctl00$Login1$LoginButton'
    for each in loginFind_payload:
        try:
            payload[each] = soup.find('input', {'id': each}).get('value')
        except AttributeError:
            payload[each] = ''
    payload['ctl00$Login1$RadioButtonList1'] = 'zh-tw'
    payload['ctl00$Login1$UserName'] = NID
    payload['ctl00$Login1$Password'] = PASS
    payload['ctl00$Login1$vcode'] = get_code(Session)
    payload['ctl00$temp'] = ''

    return payload


def login(Session, NID, PASS):
    signin = Session.post(login_url, headers=header, data=get_login_payload(session, NID, PASS))
    flag = False
    if signin.text.__contains__('登入資訊'):
        flag = True
    return flag, signin


def course_find(Session, Sign_In, CourseID):
    soup = BeautifulSoup(Sign_In.text, 'html.parser')
    url = 'http://service' + Sign_In.url[14:17] + '.sds.fcu.edu.tw/' + soup.find('form', {'id': 'aspnetForm', 'method': 'post'}).get('action')
    payload = {'ctl00_ToolkitScriptManager1_HiddenField': '',
               'ctl00_MainContent_TabContainer1_ClientState': '{\"ActiveTabIndex\":2,\"TabState\":[true,true,true]}',
               '__EVENTTARGET': '',
               '__EVENTARGUMENT': '',
               '__LASTFOCUS': '',
               'ctl00_MainContent_TabContainer1_tabSelected_TabContainer2_ClientState': '{\"ActiveTabIndex\":0,\"TabState\":[true,true,true]}',
               '__VIEWSTATE': soup.find('input', {'id': '__VIEWSTATE'}).get('value'),
               '__VIEWSTATEGENERATOR': soup.find('input', {'id': '__VIEWSTATEGENERATOR'}).get('value'),
               '__EVENTVALIDATION': soup.find('input', {'id': '__EVENTVALIDATION'}).get('value'),
               'ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$ddlDegree': '1',
               'ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$ddlDept': '',
               'ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$ddlUnit': '',
               'ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$ddlClass': '',
               'ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$tbSubID': '',
               'ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$ddlWeek': '',
               'ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$ddlPeriod': '',
               'ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$tbCourseName': '',
               'ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$tbTeacherName': '',
               'ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$ddlSpecificSubjects': '1',
               'ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$cbShowSelected': 'on',
               'ctl00$MainContent$TabContainer1$tabSelected$tbSubID': CourseID,
               'ctl00$MainContent$TabContainer1$tabSelected$btnGetSub': '查詢',
               'ctl00$MainContent$TabContainer1$tabSelected$cpeWishList_ClientState': 'false'}
    result = Session.post(url, headers=header, data=payload)
    return result


def course_check(Session, Sign_In, Find):
    soup = BeautifulSoup(Find.text, 'html.parser')
    url = 'http://service' + Sign_In.url[14:17] + '.sds.fcu.edu.tw/' + soup.find('form', {'id': 'aspnetForm', 'method': 'post'}).get('action')
    payload = {'ctl00_ToolkitScriptManager1_HiddenField': '',
               'ctl00_MainContent_TabContainer1_ClientState': '{\"ActiveTabIndex\":2,\"TabState\":[true,true,true]}',
               '__EVENTTARGET': 'ctl00$MainContent$TabContainer1$tabSelected$gvToAdd',
               '__EVENTARGUMENT': 'selquota$0',
               '__LASTFOCUS': '',
               'ctl00_MainContent_TabContainer1_tabSelected_TabContainer2_ClientState': '{\"ActiveTabIndex\":0,\"TabState\":[true,true,true]}',
               '__VIEWSTATE': soup.find('input', {'id': '__VIEWSTATE'}).get('value'),
               '__VIEWSTATEGENERATOR': soup.find('input', {'id': '__VIEWSTATEGENERATOR'}).get('value'),
               '__EVENTVALIDATION': soup.find('input', {'id': '__EVENTVALIDATION'}).get('value'),
               'ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$ddlDegree': '1',
               'ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$ddlDept': '',
               'ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$ddlUnit': '',
               'ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$ddlClass': '',
               'ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$tbSubID': '',
               'ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$ddlWeek': '',
               'ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$ddlPeriod': '',
               'ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$tbCourseName': '',
               'ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$tbTeacherName': '',
               'ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$ddlSpecificSubjects': '1',
               'ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$cbShowSelected': 'on'
               }
    result = Session.post(url, headers=header, data=payload)
    return result


def course_add(Session, Sign_In, Check):
    soup = BeautifulSoup(Check.text, 'html.parser')
    url = 'http://service' + Sign_In.url[14:17] + '.sds.fcu.edu.tw/' + soup.find('form', {'id': 'aspnetForm',
                                                                                          'method': 'post'}).get(
        'action')
    payload = {'ctl00_ToolkitScriptManager1_HiddenField': '',
               'ctl00_MainContent_TabContainer1_ClientState': '{\"ActiveTabIndex\":2,\"TabState\":[true,true,true]}',
               '__EVENTTARGET': 'ctl00$MainContent$TabContainer1$tabSelected$gvToAdd',
               '__EVENTARGUMENT': 'addCourse$0',
               '__LASTFOCUS': '',
               'ctl00_MainContent_TabContainer1_tabSelected_TabContainer2_ClientState': '{\"ActiveTabIndex\":0,\"TabState\":[true,true,true]}',
               '__VIEWSTATE': soup.find('input', {'id': '__VIEWSTATE'}).get('value'),
               '__VIEWSTATEGENERATOR': soup.find('input', {'id': '__VIEWSTATEGENERATOR'}).get('value'),
               '__EVENTVALIDATION': soup.find('input', {'id': '__EVENTVALIDATION'}).get('value'),
               'ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$ddlDegree': '1',
               'ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$ddlDept': '',
               'ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$ddlUnit': '',
               'ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$ddlClass': '',
               'ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$tbSubID': '',
               'ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$ddlWeek': '',
               'ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$ddlPeriod': '',
               'ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$tbCourseName': '',
               'ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$tbTeacherName': '',
               'ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$ddlSpecificSubjects': '1',
               'ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$cbShowSelected': 'on'
               }
    result = Session.post(url, headers=header, data=payload)
    return result


def get_people(input_string):
    people = re.match(r'(\d+)\D*(\d+)', re.search(r'(?<=alert\(\'已登記人數 / 開放人數：).*(?=\'\))', input_string).group())
    current_p = people.group(1)
    max_p = people.group(2)
    return current_p, max_p


if __name__ == '__main__':
    try:
        session = requests.session()
        flag, sign_in = login(session, Username, Password)
        if not flag:
            print('*** Login failed...')
            sys.exit(0)
        else:
            print('*** Login Success ***')
            while len(Course) > 0:
                for each in Course:
                    try:
                        find = course_find(session, sign_in, each)
                        check = course_check(session, sign_in, find)
                        current_p, max_p = get_people(check.text)
                        print('Course: ', each, ' -- ', 'Current: ', current_p, ' / ', 'Max: ', max_p, '', sep='')
                        if int(current_p) < int(max_p):
                            print('Course: ', each, ' -- ', 'Adding', sep='')
                            result = course_add(session, sign_in, check)
                            if result.text.__contains__('加選成功'):
                                print('Course: ', each, ' -- ', 'Success', sep='')
                                Course.remove(each)
                            elif result.text.__contains__('科目重覆'):
                                print('Course: ', each, ' -- ', 'Repeated', sep='')
                                Course.remove(each)
                            else:
                                print('Course: ', each, ' -- ', 'Failed', sep='')
                        else:
                            print('Full')
                    except AttributeError:
                        print('Course: ', each, ' -- ', 'Already added', sep='')
                        Course.remove(each)
                    time.sleep(1)
        print('End...')
    except Exception:
        print('Error.')
