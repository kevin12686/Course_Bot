import sys
import requests
import time
from bs4 import BeautifulSoup

from NID import NID, PASS

code_url = 'https://course.fcu.edu.tw/validateCode.aspx'
login_url = 'https://course.fcu.edu.tw/Login.aspx'

loginFind_payload = ['__EVENTARGUMENT', '__LASTFOCUS', '__VIEWSTATE', '__VIEWSTATEGENERATOR',
                     '__EVENTVALIDATION']

commonFind_payload = ['ctl00_ToolkitScriptManager1_HiddenField', 'ctl00_MainContent_TabContainer1_ClientState',
                      '__LASTFOCUS', 'ctl00_MainContent_TabContainer1_tabSelected_TabContainer2_ClientState',
                      '__VIEWSTATE', '__VIEWSTATEGENERATOR', '__EVENTVALIDATION', '__EVENTARGUMENT']

header = {
    'Connection': 'Keep-Alive',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate, sdch',
    'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.6,en;q=0.4',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
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


def get_common_payload(Sign_In, CourseID):
    soup = BeautifulSoup(Sign_In.text, 'html.parser')
    payload = dict()
    payload['ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$ddlDegree'] = '1'
    payload['ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$ddlDept'] = ''
    payload['ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$ddlUnit'] = ''
    payload['ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$ddlClass'] = ''
    payload['ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$cbOtherCondition1'] = 'on'
    payload['ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$tbSubID'] = CourseID
    payload['ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$ddlWeek'] = ''
    payload['ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$ddlPeriod'] = ''
    payload['ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$tbCourseName'] = ''
    payload['ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$tbTeacherName'] = ''
    payload['ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$ddlSpecificSubjects'] = '1'
    payload['ctl00$MainContent$TabContainer1$tabCourseSearch$wcCourseSearch$cbShowSelected'] = 'on'
    for each in commonFind_payload:
        try:
            payload[each] = soup.find('input', {'id': each}).get('value')
        except AttributeError:
            payload[each] = ''
    return payload


def check_course(Session, Sign_In, CourseID):
    soup = BeautifulSoup(Sign_In.text, 'html.parser')
    URL = 'http://service111.sds.fcu.edu.tw/' + soup.find('form', {'id': 'aspnetForm', 'method': 'post'}).get('action')
    payload = get_common_payload(Sign_In, CourseID)
    payload['__EVENTTARGET'] = soup.find('input', {'value': '登記人數'}).get('id')
    sign_in = Session.post(URL, headers=header, data=payload)
    return sign_in


if __name__ == '__main__':
    session = requests.session()
    flag, sign_in = login(session, NID, PASS)
    if not flag:
        print('*** Login failed...')
        sys.exit(0)
    else:
        print('*** Login Success')
