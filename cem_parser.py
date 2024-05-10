import struct, logging


Measurement_Unit = {
    0: "None",
    1: "KV\u2393",
    2: "V\u2393",
    3: "mV\u2393",
    4:	"A\u2393",
    5:	"mA\u2393",
    6:	"\u03bcA\u2393",
    7:	"KV~",
    8:	"V~",
    9:	"mV~",
    10:	"A~",
    11:	"mA~",
    12:	"\u03bcA~",
    13:	"kV AC+DC",
    14:	"V AC+DC",
    15:	"mV AC+DC",
    16:	"A AC+DC",
    17:	"mA AC+DC",
    18:	"\u03bcA AC+DC",
    19:	"MHz",
    20:	"KHz",
    21:	"Hz",
    22:	"M\u03a9",
    23:	"K\u03a9",
    24:	"\u03a9",
    25:	"F",
    26:	"mF",
    27:	"uF",
    28:	"nF",
    29:	"pF",
    30:	"%",
    31:	"S",
    32:	"@",
    33:	"E",
    34:	"\u00b0C",
    35:	"\u00b0F",
    36:	"K",
    37:	"VFD",
    38:	"m/s",
    39:	"km/h",
    40:	"ft/min",
    41:	"MPH",
    42:	"knots",
    43:	"%RH",
    44:	"dBA",
    45:	"dBC",
    46:	"kPa",
    47:	"ms",
    48:	"Lux",
    49:	"Fc",
    50:	"CMM",
    51:	"CFM",
    52:	"cm\u00b2",
    53:	"ft\u00b2",
    54:	"in\u00b2",
    55:	"KW/h",
    56:	"PF",
    57:	"THD",
    58:	"||||",
    59:	"KW",
    60:	"kVA",
    61:	"%TPM",
    62:	"ppm",
    63:	"mg/m3",
    64:	"CD",
    65:	"bar",
    66:	"on/in",
    67:	"psi",
    68:	"inHg",
    69:	"mbar",
    70:	"mmHg",
    71:	"kg/cm2",
    72:	"inH2o",
    73:	"ftH2o",
    74:	"cmH2o",
    75:	"g",
    76:	"in/s",
    77:	"mm/s",
    78:	"pa",
    79:	"kPa",
    80:	"inWG",
    81:	"mmWG",
    82:	"RPM",
    83:	"Closure_angle",
    84:	"DP",
    85:	"WP",
    86:	"mHg",
    87:	"mH2o",
    88:	"m\u03a9",
    89:	"m",
    90:	"km",
    91:	"ft",
    92:	"kft",
    93:	"kVar",
    94:	"c",
    95:	"i",
    96:	"\u03c6",
    97:	"kWh",
    98:	"kVarh",
    99:	"kVAh",
    100:	"dPF",
    101:	"Thd",
    102:	"uA",
    103:	"mA",
    104:	"A",
    105:	"kA",
    106:	"uV",
    107:	"mV",
    108:	"V",
    109:	"kV",
    110:	"hPa",
    111:	"%",
}

Fun_Mark = {
    0: "",	
    1:	"Auto",
    2:	"Rel",
    3:	"Max",
    4:	"Min",
    5:	"Pmax",
    6:	"Pmin",
    7:	"G",
    8:	"H",
    9:	"I",
    10:	"J",
    11:	"Time",
    12:	"Biao",
    13:	"Diode",
    14:	"OnOff",
    15:	"Fast",
    16:	"Slow",
    17:	"AVG",
    18:	"PASS",
    19:	"FAIL",
    20:	"2DIS",
    21:	"4DIS",
    22:	"4CYL",
    23:	"5CYL",
    24:	"Type K",
    25:	"Temp",
    26:	"Vel",
    27:	"Light",
    28:	"Hum",
    29:	"Flow",
    30:	"Area",
    31:	"T Temp",
    32:	"IR Temp",
    33:	"L",
    34:	"A",
    35:	"B",
    36:	"Dif",
    37:	"INRUSH",
    38:	"Harmonic",
    39:	"THD",
    40:	"NX",
    41:	"||||",
    42:	"\u03bb",
    43:	"CO/CO2",
    44:	"\u03bb",
    45:	"O\u2082",
    46:	"Co",
    47:	"CO\u2082",
    48:	"Natural gas",
    49:	"LPG",
}

CEM_START_BYTE = 0
#unknown byte
CEM_LENGTH_BYTE_1 = 2
CEM_LENGTH_BYTE_2 = 3
#unknown
CEM_GEAR_POSITION = 5
CEM_SHOW_COUNT = 6
CEM_DATA_COUNT = 7
CEM_DATA_SIZE = 8
CEM_HOLD_MARK = 9
CEM_USER_TYPE = 10
#unknown
CEM_DATA_START = 12

logger = logging.getLogger(__name__)

class measurement():
    def __init__(self, value, unit):
        self.value = value
        self.unit = unit
    def get_value(self):
        return self.value
    def get_unit(self):
        return self.unit

class cem_parser():
    def __init__(self):
        self.data = []
    
    def add_data(self, c):
        # check for the start character if it's the first
        if len(self.data) == 0 and c != 0xd5:
            return
        self.data.append(c)
    
    def parse_meter_frame(self):
        measurements = []
        if len(self.data) < 10:
            logger.info("invalid frame length")
            return measurements
        if self.data[CEM_START_BYTE] != 0xd5 or self.data[-1] != 0xd:
            logger.info("invlide start/end byte")
            return measurements
        
        logger.debug("parse: " + ''.join('{:02x}'.format(x) for x in self.data))

        length = (self.data[CEM_LENGTH_BYTE_1]<<8) | self.data[CEM_LENGTH_BYTE_2]
        gear = self.data[CEM_GEAR_POSITION]
        show_count = self.data[CEM_SHOW_COUNT]
        data_count = self.data[CEM_DATA_COUNT]
        data_size = self.data[CEM_DATA_SIZE]
        hold = self.data[CEM_HOLD_MARK]
        user_type = self.data[CEM_USER_TYPE]

        logger.debug(f"Got frame length {length}, gear: {gear}, show_count: {show_count}, data_count: {data_count},"
                    f" data_size: {data_size}, hold: {hold}, user_type: {user_type}")
        
        data_strings = []
        
        for i in range(data_count):
            data_start_idx = CEM_DATA_START + i*8
            #logger.info("get data from", ''.join('{:02x}'.format(x) for x in self.data[data_start_idx:data_start_idx+4]))
            value = struct.unpack('<f', bytearray(self.data[data_start_idx:data_start_idx+4]))
            point_count = self.data[CEM_DATA_START + i*8 + 4] #
            show_mark = self.data[CEM_DATA_START + i*8 + 5] #fun mark ->  
            show_unit = self.data[CEM_DATA_START + i*8 + 6] #unit
            other_unit = self.data[CEM_DATA_START + i*8 + 7] # ??

            val = ""
            if point_count == 0xe0:
                val = ""
            elif point_count == 0xe1:
                val = "----"
            elif point_count == 0xe2:
                val = "OL V"
            elif point_count == 0xe3:
                val = "outF"
            elif point_count == 0xf0:
                val = "-OL"
            elif point_count == 0xf1:
                val = "+OL"
            else:
                val = f"{value[0]:.0{point_count}f}"
   
            #logger.info(f"value: {val} {Measurement_Unit[show_unit]}, {Fun_Mark[show_mark]}")
            data_strings.append(f"{val} {Measurement_Unit[show_unit]},{Fun_Mark[show_mark]}")
            measurements.append(measurement(val, Measurement_Unit[show_unit]))
        logger.info("measure: " + ','.join(data_strings))
        return measurements
        

    def check_frame(self):
        #TODO remove length check, should not be needed
        #if len(self.data) == 21 or len(self.data) == 29 or len(self.data) == 37 :
        if len(self.data) >= 10 and self.data[0] == 0xd5 and self.data[-1] == 0x0d  :
            #logger.info("got frame:", ''.join(self.data))
            m = self.parse_meter_frame()
            self.data.clear()
            return m


