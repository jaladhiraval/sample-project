import json
import requests
import csv
import configparser
import sys


def login(base_url, api_login, api_password):
    print("Getting token...")
    data_get = {'username': api_login,
                'password': api_password,
                'loginMode': 1}
    r = requests.post(base_url, data=data_get)
    if r.ok:
        authToken = r.headers['AuthToken']
        cookies = dict(r.cookies)
        print("Token: " + authToken)
        return authToken
    else:
        print("HTTP %i - %s, Message %s" % (r.status_code, r.reason, r.text))


def get_sessions(base_url, auth_token, cookies):
    print("Checking session...")
    header_gs = {'AuthToken': auth_token,
                 'Accept': 'application/json'}
    r = requests.get(base_url + "sessions", headers=header_gs, cookies=cookies)
    if r.ok:
        print("Authenticated...")
        print(r)
        print("HTTP %i - %s, Message %s" % (r.status_code, r.reason, r.text))
    else:
        print("HTTP %i - %s, Message %s" % (r.status_code, r.reason, r.text))


def get_account_info(associates):
    if associates != "":
        api_url = '<url>/v1/associates/?PageSize=100&personNumber=%s' % (associates)
    else:
        print("Invalid arguments, Please provide valid Person Number")
        return None

    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        return json.loads(response.content.decode('utf-8'))
    else:
        print("response returned with error %s" % (str(response.content)))
        return None


headers = {
    'toolkit-token': "",
    'accept': "application/json",
    'Cache-Control': "no-cache",
}


# config = configparser.ConfigParser()
# config.read('associate.ini')
# sections = config.sections()

if len(sys.argv) != 2:
    print("Usage: python api.py file_name_with_path")
    sys.exit(1)

associate_ids = ""
if sys.argv[1] != "":
    with open(sys.argv[1]) as csv_file:

        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column name is {", ".join(row)}')
                line_count += 1
            else:
                associate_ids = row[0] + "," + associate_ids
                line_count += 1
        associate_ids = associate_ids[0:-1]
        print(f'associate are {associate_ids}')

account_info = get_account_info(associate_ids)

if account_info is not None:

    csv_file = open('CompletionReportAssociate.csv', 'w')
    writer = csv.writer(csv_file, delimiter=',')
    fieldnames = ['firstName', 'lastName','lineOfBusiness', 'facilityAddress', 'exceptionsURI', 'isJointVentureAssociate', 'countriesURI', 'facilityCountryCode', 'displayCostCenter', 'isLOA', 'URI', 'personNumber', 'costCenter',
                  'ctoDisplayName', 'accountsURI', 'gisReputationScore', 'latestHireDate', 'timeZone', 'CAI', 'hasExceptions', 'facilityURI', 'groupsURI', 'jobCode', 'isExceptionalLOA', 'facilityID', 'location', 'isMyWork',
                  'isBoardMember', 'jobCodeName', 'displayName', 'isTerminated', 'tenDotHierarchy', 'hireDate', 'cioDisplayName', 'numberOfTeamMembers', 'lastName', 'managerURI', 'managerEmail', 'managerDisplayName',
                  'workSummaryURI', 'numberOfDirectReports', 'displayTimeZoneLong', 'lastUpdated', 'hrBand', 'tagsURI', 'isActiveWorkEmail', 'displayTimeZone', 'mailDrop', 'isContractor', 'gisReputationHistoryURI',
                  'legalEntity', 'isActive','lastTransferDate', 'lastTransferFrom','isRegulated', 'emailMTA', 'emailServerURI', 'emailDatabase','contractEndDate','contractingVendor','lastDateIPChanged', 'informationWallClassification',
                  'phoneNumber', 'lastDeviceNameSeen', 'primaryDomain', 'lastIPAddressSeen', 'homeSpace', 'assessmentsURI', 'networkID', 'workEmail', 'hostAffinities', 'workEmailDataSource','isBloombergUser', 'isSPOC', 'middleName',
                  'lastJobCodeChangeDate', 'lastJobCode','preferredName','loaStartDate','preferredTelepresence']
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()
    for k in account_info['data']:
        writer.writerow(k)
    csv_file.close()
else:
    print('[!] Request Failed')
