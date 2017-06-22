from django.db import connections

from utils.password_gen import encrypt_password


class CallSumoLegacyDB:

    connection = None

    def __init__(self, connection_db='callsumo_legacy'):
        self.connection = connections['callsumo_legacy'] \
            if not self.connection else self.connection
        self.connection.autocommit = False
        # self.connection.isolation_level = None

    def _generic_exists_query(self, table, lookup_field, value):

        # Open cursor
        with self.connection.cursor() as cursor:

            # Generic query made up using table, lookup field and value
            query = """SELECT * FROM %s""" % (table,)
            query += """ where {}=""".format(lookup_field,)
            query += """%s"""

            # Execute select query
            cursor.execute(
                query,
                [value]
            )

            record = cursor.fetchone()

            return True if record else False

        return

    def _generic_where_query(self, select_query, from_query, where_query, values, extra=None):

        # Open cursor
        with self.connection.cursor() as cursor:

            try:
                # Generic query made up using table, lookup field and value
                query = """SELECT * FROM %s""" % (from_query,)
                query += """ WHERE {}""".format(where_query,)
                query += """ {} """.format(extra,) if extra else ''

                # Execute select query
                cursor.execute(
                    query,
                    values
                )
                result = cursor.fetchall()

                # Get query fields
                fields = list(map(
                    lambda x: x[0],
                    cursor.description
                ))

                data = [
                    dict(
                        zip(
                            fields,
                            row
                        )
                    ) for row in result
                ]

                return data if data else None
            except Exception as error:
                print(error)

        return

    def _generic_insert(self, table, fields, values):

        inserted_record_id = None

        # Open cursor
        with self.connection.cursor() as cursor:

            try:
                # Begin transaction

                # set generic query string
                query = """INSERT INTO %s (%s) VALUES (%s)""" % (
                    table,
                    ', '.join(fields),
                    ', '.join(['%s'] * len(values))
                )

                # Execute select query
                cursor.execute(
                    query,
                    values
                )

                # Get record inserted ID
                inserted_record_id = cursor.lastrowid

                # Commit
                # cursor.execute("commit")

            except Exception as error:
                # Rollback
                cursor.execute("rollback")

                # Close cursor
                cursor.close()

                # Print errors
                print("Can't insert into table %s due to: %s" % (table, str(error)))
                print(locals())

                # Raise error again
                raise error

        return inserted_record_id

    def sikka_practice_exists(self, sikka_client_id):

        exists = self._generic_exists_query(
            'sikka_practice',
            'sikka_client_id',
            sikka_client_id
        )

        return exists

    def ctm_practice_exists(self, ctm_account_id):

        exists = self._generic_exists_query(
            'ctm_practice',
            'ctm_account_id',
            ctm_account_id
        )

        return exists

    def user_login_exists(self, email):

        exists = self._generic_exists_query(
            'user',
            'email',
            email
        )
        return exists

    def insert_caller_id_user(self, email, password):

        # Get hashed password
        hashed_password = encrypt_password(password)

        # Table fields to insert
        fields = [
            'email',
            'password'
        ]

        # Values to insert
        values = [
            email,
            hashed_password
        ]

        # Table to insert
        table = 'user'

        inserted_id = self._generic_insert(table, fields, values)

        return inserted_id

    def insert_client(self, owner, name):

        # Table fields to insert
        fields = [
            'owner_name',
            'business_name'
        ]

        # Values to insert
        values = [
            owner,
            name
        ]

        # Table to insert
        table = 'client'

        # Insert
        inserted_id = self._generic_insert(table, fields, values)

        return inserted_id

    def insert_ctm_practice(self, ctm_account_id):

        # Table fields to insert
        fields = [
            'ctm_account_id',
        ]

        # Values to insert
        values = [
            ctm_account_id,
        ]

        # Table to insert
        table = 'ctm_practice'

        # Insert
        inserted_id = self._generic_insert(table, fields, values)

        return inserted_id

    def insert_practice(self, dwn_client_id, practice_name, ctm_account_id, calls_type='CTM'):

        # Table fields to insert
        fields = [
            'dwn_client_id',
            'practice_name',
            'ctm_account_id',
            'calls_type'
        ]

        # Values to insert
        values = [
            dwn_client_id,
            practice_name,
            ctm_account_id,
            calls_type
        ]

        # Table to insert
        table = 'practice'

        # Insert
        inserted_id = self._generic_insert(table, fields, values)

        return inserted_id

    def insert_practice_role(self, role_id, dwn_practice_id):

        # Table fields to insert
        fields = [
            'role_id',
            'dwn_practice_id',
        ]

        # Values to insert
        values = [
            role_id,
            dwn_practice_id
        ]

        # Table to insert
        table = 'practice_role'

        # Insert
        inserted_id = self._generic_insert(table, fields, values)

        return inserted_id

    def insert_sikka_practice(self, dwn_practice_id, sikka_client_id, sikka_source_key,
                              sikka_practice_id=1):

        # Table fields to insert
        fields = [
            'dwn_practice_id',
            'sikka_client_id',
            'sikka_source_key',
            'sikka_practice_id',
        ]

        # Values to insert
        values = [
            dwn_practice_id,
            sikka_client_id,
            sikka_source_key,
            sikka_practice_id
        ]

        # Table to insert
        table = 'sikka_practice'

        # Insert
        inserted_id = self._generic_insert(table, fields, values)

        return inserted_id

    def add_new_client(self, data):

        cursor = self.connection.cursor()

        try:

            cursor.execute("begin")
            # Insert client record
            client_id = self.insert_client(
                data.get('owner_name'),
                data.get('business_name'),
            )

            # Insert ctm practice record
            self.insert_ctm_practice(
                data.get('ctm_account_id'),
            )

            # Insert practice record
            dwn_practice_id = self.insert_practice(
                client_id,
                data.get('ctm_name'),
                data.get('ctm_account_id'),
            )

            # Insert role record
            self.insert_practice_role(
                3,
                dwn_practice_id,
            )

            # Insert role record
            self.insert_practice_role(
                4,
                dwn_practice_id,
            )

            # Insert sikka practice record
            self.insert_sikka_practice(
                dwn_practice_id,
                data.get('sikka_client_id'),
                data.get('sikka_source_key'),
            )

            # Insert user caller id
            self.insert_caller_id_user(
                data.get('email'),
                data.get('password')
            )

            cursor.execute("commit")
            cursor.close()
        except Exception as error:
            cursor.execute("rollback")
            print("Can't insert into table due to: %s" % (error, ))
            raise error

    def get_new_patients_by_created_date(self, start_date, end_date, ctm_account_id):

        select_query = "*"
        from_query = 'patient'
        values = {
            'start_date': start_date,
            'end_date': end_date,
            'ctm_account_id': ctm_account_id
        }
        where_query = '   DATE(first_visit) >= %(start_date)s '
        where_query += 'AND DATE(first_visit) <= %(end_date)s '
        # where_query += 'AND (DATE(first_visit) = DATE(dwn_date_added) OR first_visit is NULL)'
        where_query += """
            AND patient.dwn_practice_id = (
                SELECT practice.dwn_practice_id
                FROM practice where practice.ctm_account_id=%(ctm_account_id)s
            )
        """

        new_patients = self._generic_where_query(
            select_query,
            from_query,
            where_query,
            values
        )

        return new_patients

    def get_practice_by_ctm_account(self, ctm_account_id):
        select_query = "*"
        from_query = 'practice'
        values = {
            'ctm_account_id': ctm_account_id
        }

        where_query = 'ctm_account_id=%(ctm_account_id)s'
        practice_response = self._generic_where_query(
            select_query,
            from_query,
            where_query,
            values
        )

        return practice_response.pop() if practice_response else None

    def get_numbers_from_practice(self, ctm_account_id):

        practice = self.get_practice_by_ctm_account(ctm_account_id)
        select_query = "phone_number"
        from_query = 'phone_list'
        values = {
            'dwn_practice_id': practice.get('dwn_practice_id')
        }
        # extra = "ORDER BY classify_date DESC LIMIT 1"

        where_query = 'dwn_practice_id=%(dwn_practice_id)s'
        numbers = self._generic_where_query(
            select_query,
            from_query,
            where_query,
            values,
            # extra
        )

        return numbers
