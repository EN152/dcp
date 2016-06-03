class Categorys(object):
    CATEGORY_TYPES = (('1', 'Lebensmittel'),
				('2', 'Infrastruktur'),
				('3', 'Werkzeug'),
				('4', 'Medizin'),
				('5', 'Sonstiges'))

    def stringToCategoryTypeAsNumber(category):
        if category == 'Lebensmittel':
        	return 1
        if category == 'Infrastruktur':
        	return 2
        if category == 'Werkzeug':
        	return 3
        if category == 'Medizin':
        	return 4
        # Default
        return 5
    
    def getCategoryGlyphiconAsString(category):
        if category == '1':
        	return "glyphicon glyphicon-cutlery"
        if category == '2':
        	return "glyphicon glyphicon-home"
        if category == '3':
        	return "glyphicon glyphicon-wrench"
        if category == '4':
        	return "glyphicon glyphicon-plus"
           # Default
        return "glyphicon glyphicon-question-sign"
    
    def getCategoryNameAsString(category):
    	if category == '1':
    		return "Lebensmittel"
    	if category == '2':
    		return "Infrastruktur"
    	if category == '3':
    		return "Werkzeuge"
    	if category == '4':
    		return "Medikamente"
    	# Default
    	return "Sonstiges"
    
    def getCategoryListAsGlyphiconString():
    	list = []
    	list.append("glyphicon glyphicon-cutlery")
    	list.append("glyphicon glyphicon-home")
    	list.append("glyphicon glyphicon-wrench")
    	list.append("glyphicon glyphicon-plus")
    	list.append("glyphicon glyphicon-question-sign")
    	return list
    
    def getCategoryListAsNameString():
    	list = []
    	list.append("Lebensmittel")
    	list.append("Infrastruktur")
    	list.append("Werkzeuge")
    	list.append("Medikamente")
    	list.append("Sonstige")
    	return list