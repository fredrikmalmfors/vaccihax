import requests
import traceback
import json
import bs4

def push_notification(title, message, link):

    res = requests.post('https://api.pushover.net/1/messages.json', data={
        'title': title,
        'message': message,
        'user': '<<REMOVED>>',
        'token': '<<REMOVED>>',
        'url': link
    })

    ocs = json.loads(res.text)

    if ocs['status'] == 1:
        print('Notification successful')
    else:
        print('Could not send notification...')
        print(ocs)


def omtanken():

    print(' ')
    print('---------- OMTANKEN')

    # Step 1: Fetch available locations
    url = 'https://omtanken.se/api/bookings/covid19-phase4-locations/'
    try:
        res = requests.get(url, timeout=5, headers= {'Authorization': 'Token <<REMOVED>>'})
    except Exception as e:
        print(e)
        # traceback.print_stack()
        return

    if res.status_code != 200:
        print(res.status_code)
        # print('Error')
        # print(res)
        return

    locs = json.loads(res.text)


    # Step 2: Fetch times for each location
    for loc in locs:
        _id = loc['id']
        name = loc['name']

        if name == 'Test':
            continue

        url = f'https://omtanken.se/api/bookings/appointments/other/?bookingType=covid19-fas4&location={_id}'
        try:
            res = requests.get(url, timeout=2, headers= {'Authorization': 'Token <<REMOVED>>'})
        except Exception as e:
            print(e)
            # traceback.print_stack()
            continue

        if res.status_code != 200:
            print(res.status_code)
            # print('Error')
            # print(res)
            continue

        res_data = json.loads(res.text)

        link = 'https://omtanken.se/boka-tid/covid19-fas4/medtanken/'

        if len(res_data['times']) > 0:

            first = res_data['times'][0]
            date = first['start'][0:10]

            push_notification('OMTANKEN ' + name, date, link)

            print('👑', date, name, '👑')
            print('     ', link)
        
        else:
            print('-', name)

def capio():

    print(' ')
    print('---------- CAPIO / Patient.nu')

    spots = [
        {'id': 'b1d9530d-74bd-11eb-b72c-c1de16d3e1eb', 'name': 'Kvillebäcken'},
        # {'id': 'f2076616-74c3-11eb-b72c-c1de16d3e1eb', 'name': 'Selma'},
        # {'id': '404caed5-74c7-11eb-b72c-c1de16d3e1eb', 'name': 'Amhult'},
        # {'id': '8c008954-74c8-11eb-b72c-c1de16d3e1eb', 'name': 'Axess'},
        # {'id': '338dab69-ab30-11eb-a8eb-fa163e329242', 'name': 'Gårda'},
        # {'id': '1422d5a0-74bf-11eb-b72c-c1de16d3e1eb', 'name': 'Lundby'},
        # {'id': '56708b7f-6c11-11eb-b72c-c1de16d3e1eb', 'name': 'Mölndal'},
        {'id': '2c61fd19-74ba-11eb-b72c-c1de16d3e1eb', 'name': 'Angered'},
        # {'id': 'dc841111-74ca-11eb-b72c-c1de16d3e1eb', 'name': 'Hovås'},

        {'id': '9926e9dd-a824-11eb-a8eb-fa163e329242', 'name': '[Egen] Carlanderska'},

        {'id': 'a5acef14-9dba-11eb-a8eb-fa163e329242', 'name': 'Distriksläkarna Kviberg'},
        {'id': '92adacb2-a27c-11eb-a8eb-fa163e329242', 'name': 'Distriksläkarna Mölndal'},

        # FEL: FÖR PRC :(
        {'id': 'b24e2b1b-b225-11eb-91e2-fa163e329242', 'name': 'Medipart Partille'},   

        # Legehuset
        {'id': '72bef32a-b715-11eb-91e2-fa163e329242', 'name': 'Legehuset: Hammarkullen'},
        {'id': '64d1591b-b718-11eb-91e2-fa163e329242', 'name': 'Legehuset: Heden'},
        {'id': '1047469d-b717-11eb-91e2-fa163e329242', 'name': 'Legehuset: Biskopsgården'}
    ]

    for spot in spots:
        # url = 'https://patient.nu/portal/public/gettimes/07399d52-74bb-11eb-b72c-c1de16d3e1eb?start=2021-04-26&end=2021-12-31&_=1620684073979'

        id_ = spot['id']
        name = spot['name']

        url = f'https://patient.nu/portal/public/gettimes/{id_}?start=2021-04-26&end=2021-12-31'
        
        try:
            res = requests.get(url, timeout=3)
        except Exception as e:
            print(e)
            # traceback.print_stack()
            continue

        if res.status_code != 200:
            print(res.status_code)
            # print('Error')
            # print(res)
            continue

        try:
            slots = json.loads(res.text)
        except Exception:
            print('NOPE')
            # pprint.pprint(res.text)
            continue

        good_slot = None
        for slot in slots:
            if 'Bokad' not in slot['title']:
                good_slot = slot
                break

        if good_slot:
            link = f'https://patient.nu/portal/public/calendar/{id_}'
            date = good_slot['start'][0:10]
            push_notification('CAPIO ' + name, date, link)
            print('👑', date, name, '👑')
            print('     ', link)
        else:
            print('-', name)


def vaccina():

    print(' ')
    print('---------- VACCINA')

    spots = [
        {'id': '30629', 'name': 'Vädursgatan 5'},
        {'id': '30630', 'name': 'Partille'},
    ]

    for spot in spots:
        id_ = spot['id']
        name = spot['name']

        url = f'https://apibk.cliento.com/api/v2/partner/cliento/<<REMOVED>>/resources/slots?fromDate=2021-05-10&srvIds={id_}&toDate=2021-10-31'

        try:
            res = requests.get(url)
        except Exception as e:
            print(e)
            traceback.print_stack()
            return
        res_data = json.loads(res.text)
        slots = res_data['resourceSlots']

        if len(slots) > 0:
            link = 'https://www.vaccina.se/covidvaccin/vastra-gotaland/tidsbokning/#/calendar'
            push_notification('VACCINA ' + name, 'unknown', link)
            print('👑', 'unknown', name, '👑')
            print('     ', link)
        else:
            print('-', name)


def altan():

    print(' ')
    print('---------- ALTAN')

    spots = [
        {'id': '470', 'name': 'Backaplan'},
        {'id': '603', 'name': 'Hälsa Hemma'},
    ]

    for spot in spots:

        id_ = spot['id']
        name = spot['name']

        url = f'https://patientbokningonline.atlan.se/?do=GetTimes&klid={id_}&=&start=1620597600&end=1633985520'

        try:
            res = requests.get(url)
        except Exception as e:
            print(e)
            traceback.print_stack()
            return
        res_data = json.loads(res.text)

        if res_data != None:
            link = f'https://patientbokningonline.atlan.se/?klid={id_}#'
            push_notification('ALTAN ' + name, 'unknown', link)
            print('👑', 'unknown', name, '👑')
            print('     ', link)
        else:
            print('-', name)

def mitt_vaccin():

    url = 'https://booking-api.mittvaccin.se/clinique'

    try:
        res = requests.get(url)
    except Exception as e:
        print(e)
        traceback.print_stack()
        return

    res_data = json.loads(res.text)

    hej = [(poc['id'] + '      ' + poc['name'] + ' <---> ' + poc['address']) for poc in res_data if poc['city'] == 'Linköping']

    for ey in hej:
        print(ey)

def kronan():

    print(' ')
    print('---------- KRONAN')

    # 166 allum partille

    locs = [
        {'id': 2071, 'name': 'Partille Arena'}, # Ej kronan?
        {'id': 2078, 'name': 'Wieselgrensplatsen'},
        {'id': 2087, 'name': 'Kungsportsplatsen'},
        {'id': 2090, 'name': 'Torslanda'},
        {'id': 2091, 'name': 'Hisingsbacka'},
        {'id': 2092, 'name': 'Eriksbergs Köpcenter'},
        {'id': 2094, 'name': 'Partille'},
        {'id': 2095, 'name': 'Mölnlycke'}
    ]

    for loc in locs:
        id_ = loc['id']
        name = loc['name']

        # Yo, maybe i should check here that appointment types are actually available... right?
        url = f'https://booking-api.mittvaccin.se/clinique/{id_}/appointmentTypes'

        try:
            res = requests.get(url, timeout=5)
        except Exception as e:
            print(e)
            # traceback.print_stack()
            return

        if res.status_code != 200:
            # print(res.status_code)
            print('Error', name)
            # print(res)
            continue

        types = json.loads(res.text)

        if len(types) == 0:
            while len(name) < 30:
                name += ' '

            print('-', name, '(no appointment types)')
            continue

        appointment_type = types[0]['id']

        url = f'https://booking-api.mittvaccin.se/clinique/{id_}/appointments/{appointment_type}/slots/210517-210930'

        try:
            res = requests.get(url)
        except Exception as e:
            print(e)
            traceback.print_stack()
            return

        res_data = json.loads(res.text)

        link = f'https://bokning.mittvaccin.se/klinik/{id_}/bokning2'

        done = False

        for dte in res_data:
            slots = dte['slots']
            for slot in slots:
                avail = slot['available']
                if avail:
                    bad = dte['date']
                    good_date = '20' + bad[0:2] + '-' + bad[2:4] + '-' + bad[4:6]
                    push_notification('KRONAN ' + name, good_date, link)
                    print('👑', good_date, name, '👑')
                    print('     ', link)
                    done = True
                    break
            
            if done:
                break

        if not done:
            print('-', name)


def vclakarhuset():

    print(' ')
    print('---------- Vårdcentralen Läkarhuset')

    url = 'https://vclakarhuset-webtidbok.b3care.se/PrepareBooking.do?fromDate=2021-05-13&toDate2021-07-31&time=1620898106751&slotPosition=0&doaction=&id=&oldSlot=&asynjaEventId=&bookingNo=&companyClientNo=0&employeeId=&endTime=&startTime=&=&=on&internalComment=&department=&emailConfirm=&email=&lastName=&firstName=&tel=&civicRegNo=&toDate=2021-07-31&fromDate=2021-05-13&fromTime=&serviceType=&=Alla&=undefined'

    try:
        res = requests.get(url)
    except Exception as e:
        print(e)
        traceback.print_stack()
        return

    if res.status_code != 200:
        print(res.status_code)
        print('Error')
        print(res)

    if 'Inga lediga tider tillgängliga för valda sökalternativ' not in res.text:
        link = 'https://vclakarhuset-webtidbok.b3care.se/?company_client_no=0'
        push_notification('Vårdcentralen Läkarhuset', 'unknown', link)
        print('👑', 'unknown', 'Vårdcentralen Läkarhuset', '👑')
        print('     ', link)
    else:
        print('-', 'Vårdcentralen Läkarhuset')

def min_doktor():

    print(' ')
    print('---------- Min Doktor')

    url = 'https://api.mindoktor.se/api/v1/covid-mass-vaccination/domains-with-available-times'

    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json;charset=UTF-8',
        'Origin': 'https://www.mindoktor.se',
        'Accept-Language': 'en-gb',
        'Host': 'api.mindoktor.se',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15',
        'Referer': 'https://www.mindoktor.se/boka/valj-region/',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'X-Requested-With': 'XMLHttpRequest'
    }

    try:
        res = requests.get(url, headers=headers)
    except Exception as e:
        print(e)
        # traceback.print_stack()
        return

    if res.status_code != 200:
        # print(res.status_code)
        print('Error')
        # print(res)

    result = json.loads(res.text)

    # pprint.pprint(result)

    if result['data']:
        spots = result['data']
        if len(spots):
            try:
                spot = next(spot for spot in spots if spot["domainSlug"] == "mdkliniken-nordstan")
            except Exception:
                print('Cant find Nordstan')
            available_times = spot["availability"]["dosage1"]["availableTimes"]
            if available_times > 0:
                link = 'https://www.mindoktor.se/boka/valj-region'
                push_notification('Min Doktor Nordstan', 'unknown', link)
                print('👑', 'unknown', 'Nordstan', '👑')
                print('     ', link)
            elif available_times == 0:
                print('-', 'Nordstan')
            else:
                print('what')
    
    else:
        print('Odd response...')

def previa():

    print(' ')
    print('---------- Previa')

    url = f'https://se.visibacare.com/api/Client/v2/units/3531/Timeslots?conditionId=4196&fromDate=2021-06-29&toDate=2021-08-29&fromTime=00:00:53&toTime=23:59:53&localityType=all'

    try:
        res = requests.get(url, timeout=2)
    except Exception as e:
        print(e)
        traceback.print_stack()
        return

    if res.status_code != 200:
        # print(res.status_code)
        print('Error')
        # print(res)

    result = json.loads(res.text)

    if 'Data' in result.keys():
        if result['Data']:
            for elem in result['Data']:
                print(elem['Start'])
            link = 'https://se.visibacare.com/previa/vaccination-covid-19/vgr/ew'
            push_notification('Previa', 'unknown', link)
            print('👑', 'unknown', 'Previa', '👑')
            print('     ', link)
        else:
            print('-', 'Previa')
    
    else:
        print('Odd response...')


def vgr():

    print(' ')
    print('---------- 1177 (public)')
    
    url = f'https://www.vgregion.se/ov/vaccinationstider/bokningsbara-tider/'

    try:
        res = requests.get(url)
    except Exception as e:
        print(e)
        traceback.print_stack()
        return

    soup = bs4.BeautifulSoup(res.text, features="html.parser")

    a = soup.select('#main-content > div.row.content-area-wrapper > div.block.display-option-100.mottagningbookabletimeslistblock > div > div')[0]

    a = [b for b in a if not isinstance(b, bs4.element.NavigableString)]

    del a[0]

    if len(a):
        pass
        # print(f'Found {str(len(a))} slots:')
    else:
        print('...empty')

    """
    Example title:

    Falköping: Bräcke diakoni Centralhälsan

    """

    cities_to_take = [
        'Göteborg',
        'Mölndal',
        'Partille'
    ]

    dont_care_about = []

    for place in a:
        try:
            title = place.find('h3').string
            city = title.split(':')[0]
        except AttributeError:
            try:
                title = place.find('p').string
                print(title)
            except AttributeError:
                print('Ok now someting really went wrong.')
                print(place)
            break
        if city in cities_to_take:
            link = place.find('a')['href']
            print('👑', str(title), '👑')
            print('     ', link)
            push_notification('1177 ' + str(title), 'unknown', link)
        else:
            dont_care_about.append(city)
    
    # print('Dont care about:')
    # print(*dont_care_about, sep=', ')


from datetime import datetime
import random
import time

if __name__ == '__main__':

    while True:
        # Prep
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print(' ')
        print('---', current_time, '---')

        # 1177
        vgr()

        # RUN
        previa()
        min_doktor()
        omtanken()
        capio()
        vaccina()
        altan()
        kronan()
        vclakarhuset()
        mitt_vaccin()

        # Countdown
        print(' ')
        seconds_to_wait = random.randint(10, 60)
        for i in range(seconds_to_wait):
            seconds_left = seconds_to_wait - i
            print("\r", end='')
            print(f'Next fetch in {seconds_left:02d} seconds', end='', flush=True)
            time.sleep(1)
        print(' ')

