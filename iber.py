"""Module providing REST API access to i-DE"""

from datetime import datetime

from deprecated.classic import deprecated

try:
    from requests import Session
except ImportError as exc:
    raise RuntimeError("Iber requires requests module") from exc

from exception import LoginException, ResponseException, NoResponseException, \
    SelectContractException, SessionException


class Iber:
    """ Class to get information from i-DE"""

    __domain = "https://www.i-de.es"
    __login_url = __domain + "/consumidores/rest/loginNew/login"
    __logout_url = __domain + "/consumidores/rest/loginNew/logOut"
    __watthourmeter_url = __domain + \
        "/consumidores/rest/escenarioNew/obtenerMedicionOnline/24"
    __icp_status_url = __domain + "/consumidores/rest/rearmeICP/consultarEstado"
    __contracts_url = __domain + "/consumidores/rest/cto/listaCtos/"
    __contract_detail_url = __domain + "/consumidores/rest/detalleCto/detalle/"
    __contract_selection_url = __domain + "/consumidores/rest/cto/seleccion/"
    __obtener_escenarios_url = __domain + \
        "/consumidores/rest/escenarioNew/obtenerEscenariosRest/"
    __obtener_escenario_url = __domain + \
        "/consumidores/rest/escenarioNew/refrescarEscenario/"
    __guardar_escenario_url = __domain + (
        "/consumidores/rest/escenarioNew/confirmarMedicionOnLine/{}/1/{}")
    __borrar_escenario_url = __domain + \
        "/consumidores/rest/escenarioNew/borrarEscenario/"
    __obtener_periodo_url = __domain + (
        "/consumidores/rest/consumoNew/obtenerDatosConsumoPeriodo/"
        "fechaInicio/{}00:00:00/fechaFinal/{}00:00:00/")
    # date format: 07-11-2020 - that's 7 Nov 2020
    __obtener_dia_url = __domain + (
        "/consumidores/rest/consumoNew/obtenerDatosConsumoDH/{}/{}/horas/USU/")
    # date format: 07-11-2020 - that's 7 Nov 2020
    __obtener_periodo_generacion_url = __domain + (
        "/consumidores/rest/consumoNew/obtenerDatosGeneracionPeriodo/"
        "fechaInicio/{}00:00:00/fechaFinal/{}00:00:00/")
    # date format: 07-11-2020 - that's 7 Nov 2020

    __user_agent = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
                    " (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36")

    __headers = {
        'User-Agent': __user_agent,
        'accept': "application/json, text/plain, */*",
        'content-type': "application/json; charset=UTF-8",
        'cache-control': "no-cache"
    }

    def __init__(self, session=None):
        """Iber class __init__ method."""
        self.__session = session

    def login(self, user, password, session=Session()):
        """Creates session with your credentials"""
        self.__session = session
        blank_login_data = ("[\"{}\",\"{}\",null,\"Linux -\",\"PC\","
                            "\"Chrome 77.0.3865.90\",\"0\",\"\",\"s\"]")
        login_data = blank_login_data.format(user, password)
        response = self.__session.request("POST",
                                          self.__login_url, data=login_data, headers=self.__headers)
        print('Login: ', response.text)
        if response.status_code != 200:
            self.__session = None
            raise ResponseException(response.status_code)
        json_response = response.json()
        if json_response["success"] != "true":
            self.__session = None
            raise LoginException(user)

    def __check_session(self):
        if not self.__session:
            raise SessionException()

    def measurement(self):
        """Returns a measurement from the powermeter."""
        self.__check_session()
        response = self.__session.request(
            "GET", self.__watthourmeter_url, headers=self.__headers)
        if response.status_code != 200:
            raise ResponseException(response.status_code)
        if not response.text:
            raise NoResponseException
        json_response = response.json()
        return {
            "id": json_response['codSolicitudTGT'],
            "meter": json_response["valLecturaContador"],
            "consumption": json_response['valMagnitud'],
            "icp": json_response['valInterruptor'],
            "raw_response": json_response
        }

    def current_kilowatt_hour_read(self):
        """Returns the current read of the electricity meter."""
        return self.measurement()["meter"]

    def current_power_consumption(self):
        """Returns your current power consumption."""
        return self.measurement()['consumption']

    @deprecated("Use 'current_power_consumption' method instead")
    def watthourmeter(self):
        """Returns your current power consumption."""
        return self.current_power_consumption()

    def icpstatus(self):
        """Returns the status of your ICP."""
        self.__check_session()
        response = self.__session.request(
            "POST", self.__icp_status_url, headers=self.__headers)
        if response.status_code != 200:
            raise ResponseException(response.status_code)
        if not response.text:
            raise NoResponseException
        json_response = response.json()
        if json_response["icp"] == "trueConectado":
            return True
        return False

    def contracts(self):
        """Returns the list of contracts"""
        self.__check_session()
        response = self.__session.request(
            "GET", self.__contracts_url, headers=self.__headers)
        if response.status_code != 200:
            raise ResponseException(response.status_code)
        if not response.text:
            raise NoResponseException
        json_response = response.json()
        if json_response["success"]:
            return json_response["contratos"]

    def contract(self):
        """Return a given contract"""
        self.__check_session()
        response = self.__session.request(
            "GET", self.__contract_detail_url, headers=self.__headers)
        if response.status_code != 200:
            raise ResponseException(response.status_code)
        if not response.text:
            raise NoResponseException
        return response.json()

    def contractselect(self, id_contract):
        """Select a given contract """
        self.__check_session()
        response = self.__session.request("GET", self.__contract_selection_url + id_contract,
                                          headers=self.__headers)
        if response.status_code != 200:
            raise ResponseException(response.status_code)
        if not response.text:
            raise NoResponseException
        json_response = response.json()
        if not json_response["success"]:
            raise SelectContractException

    def scene_list(self):
        """Return the list of contracts"""
        self.__check_session()
        response = self.__session.request("GET", self.__obtener_escenarios_url,
                                          headers=self.__headers)
        if response.status_code != 200:
            raise ResponseException(response.status_code)
        if not response.text:
            raise NoResponseException
        json_response = response.json()
        return {
            "scene_names": json_response['y']['smps'],
            "raw_response": json_response
        }

    def scene_get(self, name):
        """Return a given scene"""
        self.__check_session()
        get_data = f"{{\"nomEscenario\":\"{name}\"}}"
        response = self.__session.request("POST", self.__obtener_escenario_url,
                                          data=get_data, headers=self.__headers)
        if response.status_code != 200:
            raise ResponseException(response.status_code)
        if not response.text:
            raise NoResponseException
        json_response = response.json()
        return {
            "name": json_response['nomEscenario'],
            "description": json_response['descripcion'],
            "consumption": json_response['numLcaInsta'],
            "raw_response": json_response
        }

    def scene_save(self, consumption, measurement_id, description):
        """Save scene"""
        self.__check_session()
        name = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        save_data = f"{{\"nomEscenario\":\"{name}\",\"descripcion\":\"{description}\"}}"
        response = self.__session.request(
            "POST", self.__guardar_escenario_url.format(
                consumption, measurement_id),
            data=save_data, headers=self.__headers)
        if response.status_code != 200:
            raise ResponseException(response.status_code)
        if not response.text:
            raise NoResponseException
        json_response = response.json()
        return {
            "name": json_response['nomEscenario'],
            "raw_response": json_response
        }

    def scene_delete(self, name):
        """Delete scene"""
        self.__check_session()
        delete_data = f"{{\"nomEscenario\":\"{name}\"}}"
        response = self.__session.request(
            "POST", self.__borrar_escenario_url,
            data=delete_data, headers=self.__headers)
        if response.status_code != 200:
            raise ResponseException(response.status_code)
        return True

    def _consumption_raw(self, start, end):
        self.__check_session()
        start_str = start.strftime('%d-%m-%Y')
        end_str = end.strftime('%d-%m-%Y')

        response = self.__session.request(
            "GET", self.__obtener_periodo_url.format(start_str, end_str),
            headers=self.__headers)
        if response.status_code != 200:
            raise ResponseException(response.status_code)
        if not response.text:
            raise NoResponseException
        print(response.text)
        return response.json()

    # Get consumption data from a time period
    #
    # start/end: datetime.date objects indicating the time period (both inclusive)
    # The supported time range seems to be (not documented)
    # from Jan 1 in the previous year and a max length of one year.
    #
    # Returns a list of consumptions starting a midnight on the start day
    # until 23:00 on the last day.
    # Each value is the hourly consumption in Wh.
    def consumption(self, start, end):
        """Get consumption by hours in kWh"""
        json = self._consumption_raw(start, end)
        values = []
        for x in json['y']['data'][0]:
            if x is None:
                values.append(None)
            else:
                values.append(float(x['valor']))
        return values

    def _consumption_day_raw(self, yesterday, day):
        self.__check_session()
        yesterday_str = yesterday.strftime('%d-%m-%Y')
        day_str = day.strftime('%d-%m-%Y')

        print('Request Consumption day raw:')
        print(self.__obtener_dia_url.format(yesterday_str, day_str))
        response = self.__session.request(
            "GET", self.__obtener_dia_url.format(yesterday_str, day_str),
            headers=self.__headers)
        if response.status_code != 200:
            raise ResponseException(response.status_code)
        if not response.text:
            raise NoResponseException
        print('Consumption day raw: ', response.text)
        return response.json()

    def consumption_day(self, yesterday, day):
        """Get consumption by hours in kWh"""
        json = self._consumption_day_raw(yesterday, day)
        values = []
        for x in json[0]['valores']:
            values.append(float(x))
        return values

    def _production_raw(self, start, end):
        self.__check_session()
        start_str = start.strftime('%d-%m-%Y')
        end_str = end.strftime('%d-%m-%Y')

        response = self.__session.request(
            "GET", self.__obtener_periodo_generacion_url.format(
                start_str, end_str),
            headers=self.__headers)
        if response.status_code != 200:
            raise ResponseException(response.status_code)
        if not response.text:
            raise NoResponseException
        return response.json()

    # Get production data from a time period
    #
    # start/end: datetime.date objects indicating the time period (both inclusive)
    # The supported time range seems to be (not documented) from Jan 1 in the previous
    # year and a max length of one year.
    #
    # Returns a list of productions starting a midnight on the start day until 23:00
    # on the last day. Each value is the hourly production in Wh.
    def production(self, start, end):
        """Get production"""
        json = self._production_raw(start, end)
        values = []
        for x in json['y']['data'][0]:
            if x is None:
                values.append(None)
            else:
                values.append(float(x['valor']))
        return values

    # Get total consumption in Wh (Watt-hour) over a time period
    #
    # start/end: datetime.date objects indicating the time period (both inclusive)
    def total_consumption(self, start, end):
        """Get total consumption"""
        return float(self._consumption_raw(start, end)['acumulado'])

    # Logout to make things right
    #
    def logout(self):
        """Logout"""
        self.__check_session()
        response = self.__session.request(
            "GET", self.__logout_url, headers=self.__headers)
        if response.status_code != 200:
            raise ResponseException(response.status_code)
        if not response.text:
            raise NoResponseException
        print(response.text)
