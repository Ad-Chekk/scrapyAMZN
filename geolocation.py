import geoip2.database

# Path to the GeoLite2 database file
reader = geoip2.database.Reader('GeoLite2-City.mmdb')

# Example IP address
ip_address = '35.211.122.109'
try:
    response = reader.city(ip_address)

    print(f"IP Address: {ip_address}")
    print(f"Country: {response.country.name}")
    print(f"Region: {response.subdivisions.most_specific.name}")
    print(f"City: {response.city.name}")
    print(f"Location: {response.location.latitude}, {response.location.longitude}")

except geoip2.errors.GeoIP2Error as e:
    print(f"Error: {e}")

finally:
    reader.close()
