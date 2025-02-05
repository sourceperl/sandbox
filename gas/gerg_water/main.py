from GERG_WATER import get_dew_point_c, get_humidity_mg

print(f'humidity: {get_humidity_mg(dew_point_c=-10, p_bara=50):.0f} mg/nm3')
print(f'temperature: {get_dew_point_c(hum_mg=45.0, p_bara=50):.0f} °C')
