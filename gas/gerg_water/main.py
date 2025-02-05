from GERG_WATER import get_dew_point_c, get_vol_humidity

print(f'teneur en eau: {get_vol_humidity(dew_point_c=-10, p_bara=50):.01f} mg/nm3')
print(f'point de rosée: {get_dew_point_c(vol_hum_mg=45.0, p_bara=50):.01f} °C')
