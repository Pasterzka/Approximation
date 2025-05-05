import xml.etree.ElementTree as ET
import csv

gpx_file = "Data/GPX/Giro d'Italia 2025 - Stage 21_ Roma - Roma.gpx"
csv_file = 'Data/CSV/trasa1.csv'

tree = ET.parse(gpx_file)
root = tree.getroot()

# GPX może mieć różne przestrzenie nazw
ns = {'default': 'http://www.topografix.com/GPX/1/1'}

with open(csv_file, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['latitude', 'longitude', 'elevation', 'time'])

    for trkpt in root.findall('.//default:trkpt', ns):
        lat = trkpt.attrib['lat']
        lon = trkpt.attrib['lon']
        ele = trkpt.find('default:ele', ns)
        time = trkpt.find('default:time', ns)

        writer.writerow([
            lat,
            lon,
            ele.text if ele is not None else '',
            time.text if time is not None else ''
        ])
