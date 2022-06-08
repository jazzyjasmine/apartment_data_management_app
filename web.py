from bottle import route, run, template, post, get, request, abort
import sqlite3

conn = sqlite3.connect('app.db')

DISPLAY_ROW_COUNT_LIMIT = 20

APARTMENT_COLUMN_NAMES = [
    'apartment_id',
    'apartment_name',
    'laundry_type',
    'parking_type',
    'landlord_id',
    'official_website',
    'street_address',
    'city',
    'state',
    'zipcode',
    'landlord_name'
]

LAUNDRY_TYPE_DECODE = {
    1: 'onsite laundry',
    2: 'in-unit laundry',
    3: 'NULL'
}

LAUNDRY_TYPE_SET_NULL_CODE = 3
LAUNDRY_TYPE_NO_CHANGE_CODE = 4

PARKING_TYPE_DECODE = {
    1: 'street parking',
    2: 'city-run parking',
    3: 'apartment-run parking',
    4: 'NULL'
}

PARKING_TYPE_SET_NULL_CODE = 4
PARKING_TYPE_NO_CHANGE_CODE = 5

FLOORPLAN_COLUMN_NAMES = [
    'apartment_id',
    'floor_plan_id',
    'floor_plan_type',
    'floor_plan_area',
    'price',
    'leasing_period'
]

FLOORPLAN_TYPE_DECODE = {
    1: 'studio',
    2: '1b1b',
    3: '2b2b',
    4: '2b1b',
    5: '3b2b'
}

USA_STATE_ABBREVS = {
    'AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC', 'DE', 'FL', 'GA',
    'HI', 'IA', 'ID', 'IL', 'IN', 'KS', 'KY', 'LA', 'MA', 'MD', 'ME',
    'MI', 'MN', 'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ', 'NM',
    'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX',
    'UT', 'VA', 'VT', 'WA', 'WI', 'WV', 'WY'
}


@get('/')
def get_homepage():
    return template('homepage')


@post('/')
def display_apartments():
    apartment_name = request.forms.get('aptName')
    street_address = request.forms.get('strAddress')  # empty input is an empty string

    db_response = None
    if not apartment_name and not street_address:
        try:
            db_response = conn.execute('''
            select
            apartment.*,
            landlord_name
            from apartment left join landlord using (landlord_id)
            order by apartment_id desc''').fetchall()
        except sqlite3.Error as e:
            abort(500, str(e))
    elif not apartment_name:
        try:
            db_response = conn.execute('''
            select
            apartment.*,
            landlord_name
            from apartment left join landlord using (landlord_id)
            where address like ?
            order by apartment_id desc''', [f'%{street_address}%']).fetchall()
        except sqlite3.Error as e:
            abort(500, str(e))
    elif not street_address:
        try:
            db_response = conn.execute('''
            select
            apartment.*,
            landlord_name
            from apartment left join landlord using (landlord_id)
            where apartment_name = ?
            order by apartment_id desc''', [apartment_name]).fetchall()
        except sqlite3.Error as e:
            abort(500, str(e))
    else:
        try:
            db_response = conn.execute('''
            select
            apartment.*,
            landlord_name
            from apartment left join landlord using (landlord_id)
            where apartment_name = ? and address like ?
            order by apartment_id desc''', [apartment_name, f'%{street_address}%']).fetchall()
        except sqlite3.Error as e:
            abort(500, str(e))

    apartments = []
    for apartment_data in db_response:
        apartments.append(dict(zip(APARTMENT_COLUMN_NAMES, apartment_data)))

    if len(apartments) > DISPLAY_ROW_COUNT_LIMIT:
        apartments = apartments[:DISPLAY_ROW_COUNT_LIMIT]

    return template('search_apartment_results', apartments=apartments)


@post('/apartments')
def add_apartment():
    input_apartment_name = request.forms.get('aptName')
    input_laundry_type = request.forms.get('laundryType')
    input_parking_type = request.forms.get('parkingType')
    input_landlord_id = request.forms.get('landlordID')
    input_official_website = request.forms.get('officialWebsite')
    input_street_address = request.forms.get('streetAddress')
    input_city = request.forms.get('city')
    input_state = request.forms.get('state')
    input_zipcode = request.forms.get('zipcode')

    if int(input_laundry_type) == LAUNDRY_TYPE_SET_NULL_CODE:
        input_laundry_type = 'NULL'

    if int(input_parking_type) == PARKING_TYPE_SET_NULL_CODE:
        input_parking_type = 'NULL'

    if not input_landlord_id:
        input_landlord_id = 'NULL'

    if not input_official_website:
        input_official_website = 'NULL'

    if input_state not in USA_STATE_ABBREVS:
        return user_input_error("Invalid input state.")

    if not input_zipcode.isdigit():
        return user_input_error("Invalid input zipcode. The zipcode should have 5 digits.")

    try:
        conn.execute('''
        insert into apartment values (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', [input_apartment_name,
              input_laundry_type,
              input_parking_type,
              input_landlord_id,
              input_official_website,
              input_street_address,
              input_city,
              input_state,
              input_zipcode])
        conn.commit()
    except sqlite3.Error as e:
        abort(500, str(e))

    return template('add_apartment_complete')


@get('/editApartment/<apartment_id>')
def view_and_edit_apartment(apartment_id):
    db_response = None
    try:
        db_response = conn.execute('''
            select
            apartment.*,
            landlord_name
            from apartment left join landlord using (landlord_id)
            where apartment_id = ?''', [apartment_id]).fetchall()
    except sqlite3.Error as e:
        abort(500, str(e))

    if not db_response:
        return user_input_error("Apartment ID does not exist.")

    apartment = dict(zip(APARTMENT_COLUMN_NAMES, db_response[0]))
    if apartment['laundry_type'] != 'NULL':
        apartment['laundry_type'] = LAUNDRY_TYPE_DECODE[int(apartment['laundry_type'])]
    if apartment['parking_type'] != 'NULL':
        apartment['parking_type'] = PARKING_TYPE_DECODE[int(apartment['parking_type'])]

    return template('update_apartment', apartment=apartment)


@post('/editApartment/<apartment_id>')
def update_apartment(apartment_id):
    input_apartment_name = request.forms.get('aptName')  # empty input is empty string
    input_laundry_type = int(request.forms.get('laundryType'))
    input_parking_type = int(request.forms.get('parkingType'))

    if not input_apartment_name:
        return user_input_error("Apartment Name can not be empty.")

    if input_laundry_type == LAUNDRY_TYPE_SET_NULL_CODE:
        input_laundry_type = LAUNDRY_TYPE_DECODE[LAUNDRY_TYPE_SET_NULL_CODE]
    if input_parking_type == PARKING_TYPE_SET_NULL_CODE:
        input_parking_type = PARKING_TYPE_DECODE[PARKING_TYPE_SET_NULL_CODE]

    if input_laundry_type == LAUNDRY_TYPE_NO_CHANGE_CODE and input_parking_type == PARKING_TYPE_NO_CHANGE_CODE:
        try:
            conn.execute('''
            update apartment
            set apartment_name = ?
            where apartment_id = ?
            ''', [input_apartment_name, apartment_id])
            conn.commit()
        except sqlite3.Error as e:
            abort(500, str(e))
    elif input_laundry_type == LAUNDRY_TYPE_NO_CHANGE_CODE:
        try:
            conn.execute('''
            update apartment
            set apartment_name = ?, 
                parking_type = ?
            where apartment_id = ?
            ''', [input_apartment_name, input_parking_type, apartment_id])
            conn.commit()
        except sqlite3.Error as e:
            abort(500, str(e))
    elif input_parking_type == PARKING_TYPE_NO_CHANGE_CODE:
        try:
            conn.execute('''
            update apartment
            set apartment_name = ?, 
                laundry_type = ?
            where apartment_id = ?
            ''', [input_apartment_name, input_laundry_type, apartment_id])
            conn.commit()
        except sqlite3.Error as e:
            abort(500, str(e))
    else:
        try:
            conn.execute('''
            update apartment
            set apartment_name = ?, 
                laundry_type = ?,
                parking_type = ?
            where apartment_id = ?
            ''', [input_apartment_name, input_laundry_type, input_parking_type, apartment_id])
            conn.commit()
        except sqlite3.Error as e:
            abort(500, str(e))

    return view_and_edit_apartment(apartment_id)


@route('/deleteApartment/<apartment_id>')
def delete_apartment(apartment_id: str):
    # check if valid apartment_id
    validate_apartment_id(apartment_id)

    # valid apartment_id
    delete_statements = f'''
        delete from apartment where apartment_id = {apartment_id};
        delete from user_apartment_wishlist where apartment_id = {apartment_id};
        delete from floor_plan where apartment_id = {apartment_id};
        delete from floor_plan_price where apartment_id = {apartment_id}; 
        '''
    try:
        conn.executescript(delete_statements)
        conn.commit()
    except sqlite3.Error as e:
        abort(500, str(e))

    return template('delete_apartment_complete', apartment_id=apartment_id)


@get('/floorplans/<apartment_id>')
def display_floorplans(apartment_id):
    validate_apartment_id(apartment_id)
    return template('floorplans', floorplans=get_floorplans_by_apartment_id(apartment_id))


@get('/addFloorplan/<apartment_id>')
def view_to_add_floorplan(apartment_id):
    validate_apartment_id(apartment_id)
    return template('add_floorplan', floorplans=get_floorplans_by_apartment_id(apartment_id), apartment_id=apartment_id)


@post('/addFloorplan/<apartment_id>')
def add_floorplan(apartment_id: str):
    input_floor_plan_type = int(request.forms.get('floorPlanType'))
    input_floor_plan_area = request.forms.get('floorPlanArea')  # could be empty; empty input is empty string
    input_price = request.forms.get('price')  # must not be empty
    input_leasing_period = request.forms.get('leasingPeriod')  # must not be empty

    # parse user input
    if not input_floor_plan_area:
        input_floor_plan_area = 'NULL'  # this variable is either 'NULL' or integer (string format)

    # modify database
    # check if floor plan already exists
    is_existed_fp, floor_plan_id = is_existed_floor_plan(apartment_id, input_floor_plan_type, input_floor_plan_area)
    # if not existed, insert into floor_plan table
    if not is_existed_fp:
        add_floor_plan_to_apartment(apartment_id, floor_plan_id, input_floor_plan_type, input_floor_plan_area)
    # check if price plan already exists
    is_existed_pp, price_plan_id = is_existed_price_plan(int(input_price), int(input_leasing_period))
    # if not existed, insert into price_plan table
    if not is_existed_pp:
        add_price_plan(input_price, input_leasing_period)

    # add to floor_plan_price table if needed
    add_floor_plan_price(apartment_id, floor_plan_id, price_plan_id)

    return view_to_add_floorplan(apartment_id)


def add_floor_plan_price(apartment_id, floor_plan_id, price_plan_id):
    try:
        conn.execute('''
        insert into floor_plan_price values (?, ?, ?)
        ''', [apartment_id, floor_plan_id, price_plan_id])
    except sqlite3.Error as e:
        if 'UNIQUE constraint failed' in str(e):
            return
        abort(500, str(e))


def add_floor_plan_to_apartment(apartment_id, floor_plan_id, floor_plan_type, floor_plan_area):
    try:
        conn.execute('''
        insert into floor_plan values (?, ?, ?, ?)
        ''', [apartment_id, floor_plan_id, floor_plan_type, floor_plan_area])
        conn.commit()
    except sqlite3.Error as e:
        abort(500, str(e))


def add_price_plan(price, leasing_period):
    try:
        conn.execute('''insert into price_plan values (?, ?, ?)''',
                     ['NULL', price, leasing_period])
        conn.commit()
    except sqlite3.Error as e:
        abort(500, str(e))


def is_existed_floor_plan(apartment_id: str, floor_plan_type: int, floor_plan_area: str):
    db_response = None
    try:
        db_response = conn.execute('''
        select
        floor_plan_id,
        floor_plan_type,
        floor_plan_area
        from floor_plan
        where apartment_id = ?
        order by floor_plan_id desc
        ''', [apartment_id]).fetchall()
    except sqlite3.Error as e:
        abort(500, str(e))

    if not db_response:
        return False, 1

    for floorplan in db_response:
        db_floor_plan_id = int(floorplan[0])
        db_floor_plan_type = int(floorplan[1])
        db_floor_plan_area = floorplan[2]
        if not db_floor_plan_area:
            db_floor_plan_area = 'NULL'
        if db_floor_plan_type == floor_plan_type and str(db_floor_plan_area) == floor_plan_area:
            return True, db_floor_plan_id

    max_db_floor_plan_id = int(db_response[0][0])

    return False, max_db_floor_plan_id + 1


def is_existed_price_plan(input_price: int, input_leasing_period: int):
    db_response = None
    try:
        db_response = conn.execute('''
        select
        price_plan_id,
        price,
        leasing_period
        from price_plan
        order by price_plan_id desc
        ''').fetchall()
    except sqlite3.Error as e:
        abort(500, str(e))

    if not db_response:
        return False, 1

    for price_plan in db_response:
        db_price_plan_id = int(price_plan[0])
        db_price = int(price_plan[1])
        db_leasing_period = int(price_plan[2])

        if db_price == input_price and db_leasing_period == input_leasing_period:
            return True, db_price_plan_id

    max_db_price_plan_id = int(db_response[0][0])

    return False, max_db_price_plan_id + 1


def user_input_error(message):
    return template('error',
                    status_code=400,
                    message=message)


def validate_apartment_id(apartment_id: str):
    db_response = None
    try:
        db_response = conn.execute("select apartment_id from apartment").fetchall()
    except sqlite3.Error as e:
        abort(500, str(e))
    valid_apartment_ids = {int(row[0]) for row in db_response}
    if int(apartment_id) not in valid_apartment_ids:
        return user_input_error("Apartment ID does not exist.")
    return None


def get_floorplans_by_apartment_id(apartment_id):
    db_response = None
    try:
        db_response = conn.execute('''
            select
            floor_plan.apartment_id,
            floor_plan.floor_plan_id,
            floor_plan_type,
            floor_plan_area,
            price,
            leasing_period
            from floor_plan
            left join floor_plan_price using (apartment_id, floor_plan_id)
            left join price_plan using (price_plan_id)
            where apartment_id = ?
            order by floor_plan.floor_plan_id desc
            ''', [apartment_id]).fetchall()
    except sqlite3.Error as e:
        abort(500, str(e))

    floorplans = []
    for floorplan in db_response:
        floorplans.append(dict(zip(FLOORPLAN_COLUMN_NAMES, floorplan)))

    if len(floorplans) > DISPLAY_ROW_COUNT_LIMIT:
        floorplans = floorplans[:DISPLAY_ROW_COUNT_LIMIT]

    # decode floor plan type
    for floorplan in floorplans:
        if floorplan['floor_plan_type'] != 'NULL':
            floorplan['floor_plan_type'] = FLOORPLAN_TYPE_DECODE[int(floorplan['floor_plan_type'])]

    return floorplans


run(host='localhost', port=8080, debug=True)
