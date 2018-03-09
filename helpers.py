def helperTest():
	testString = "this is the helper test function"
	return testString

def flattenjson( b, delim ):
    val = {}
    for i in b.keys():
        if isinstance( b[i], dict ):
            get = flattenjson( b[i], delim )
            for j in get.keys():
                val[ i + delim + j ] = get[j]
        else:
            val[i] = b[i]

    return val

def utf8ify(d):
    return dict((k.encode('utf-8'), v.encode('utf-8')) for k, v in d.iteritems())