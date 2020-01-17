from .apis import produce, farmer

def get(conn):
    returndata = dict()
    response = produce.stream(conn)
    counter = 0
    for i in response:
        data = dict(i)
        tempdata = dict()
        tempdata['produceid'] = data['PRODUCEID']
        tempdata['farmername'] = farmer.getNameFromId(conn, data['FARMERUSERID'])
        tempdata['producename'] = data['producename']
        tempdata['availableqty'] = data['AVAILABLEQUANTITY']
        tempdata['cost'] = data['cost']
        tempdata['description'] = data['DESCRIPTION']
        tempdata['qualityreview'] = data['QUALITY_REVIEW']
        tempdata['notimebought'] = data['NO_TIMES_BOUGHT']
        returndata[counter] = tempdata
        counter += 1
    return returndata

def length(conn):
    returndata = {}
    returndata['length'] = produce.totalToStream(conn)
    return returndata
