import usaddress

def tokenizeAddress(address):
    """
    take an address string and return a tuple of tokenized 
    house number, street name and unit number
    """
    addrTup = usaddress.tag(address)

    errorDict = dict(addrTup[0])
    houseNumber = ''
    if 'AddressNumber' in addrTup[0]:
        houseNumber += errorDict.pop('AddressNumber')
        houseNumber += ' '
    if 'AddressNumberSuffix' in addrTup[0]:
        houseNumber += errorDict.pop('AddressNumberSuffix')
    houseNumber = houseNumber.rstrip()
 
    street = ''
    for key in addrTup[0].keys():
        if key in ('StreetNamePreDirectional', 'StreetNamePreModifer',
                   'StreetNamePreType', 'StreetName',
                   'StreetNamePostDirectional', 'StreetNamePostModifer',
                   'StreetNamePostType'):
            street += errorDict.pop(key) + ' '
    street = street.rstrip()

    unitNumber = ''
    if 'OccupancyType' in addrTup[0]:
        unitNumber += errorDict.pop('OccupancyType')
        unitNumber += ' '
    if 'OccupancyIdentifier' in addrTup[0]:
        unitNumber += errorDict.pop('OccupancyIdentifier')
    unitNumber = unitNumber.rstrip().replace(', ', ',')
    
    if len(errorDict) > 0:
        errors = ''
        for k, v in errorDict.items():
            errors += 'key: ' + k + ' and value: ' + v + '\n'
        print('watch out for the extra stuff:\n' + errors)

    return (houseNumber, street, unitNumber)
