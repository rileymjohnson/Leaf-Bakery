appetizers = getRemakeDonut("appetizers")
        soups = getRemakeDonut("soups")
        salads = getRemakeDonut("salads")
        kids = getRemakeDonut("kids")
        entrees = getRemakeDonut("entrees")
        breads = getRemakeDonut("breads")
        drinks = getRemakeDonut("drinks")
        desserts = getRemakeDonut("desserts")
        out = 0
        for i in appetizers:
            out += i['mon']
            out += i['tue']
            out += i['wed']
            out += i['thu']
            out += i['fri']
            out += i['sat']
            out += i['sun']
        for i in soups:
            out += i['mon']
            out += i['tue']
            out += i['wed']
            out += i['thu']
            out += i['fri']
            out += i['sat']
            out += i['sun']
        for i in salads:
            out += i['mon']
            out += i['tue']
            out += i['wed']
            out += i['thu']
            out += i['fri']
            out += i['sat']
            out += i['sun']
        for i in kids:
            out += i['mon']
            out += i['tue']
            out += i['wed']
            out += i['thu']
            out += i['fri']
            out += i['sat']
            out += i['sun']
        for i in entrees:
            out += i['mon']
            out += i['tue']
            out += i['wed']
            out += i['thu']
            out += i['fri']
            out += i['sat']
            out += i['sun']
        for i in breads:
            out += i['mon']
            out += i['tue']
            out += i['wed']
            out += i['thu']
            out += i['fri']
            out += i['sat']
            out += i['sun']
        for i in drinks:
            out += i['mon']
            out += i['tue']
            out += i['wed']
            out += i['thu']
            out += i['fri']
            out += i['sat']
            out += i['sun']
        for i in desserts:
            out += i['mon']
            out += i['tue']
            out += i['wed']
            out += i['thu']
            out += i['fri']
            out += i['sat']
            out += i['sun']


            if adminIsIn():
        types = ["appetizers", "soups", "salads", "kids", "entrees", "breads", "drinks", "desserts"]
        t = request.args['t']
        for i in types:
            if i == t:
                ar = []
                n = []
                names = []
                for i in getItemInfo(t):
                    n.append(str(int(i['id'])))
                    ar.append(int(i['mon']) + int(i['tue']) + int(i['wed']) + int(i['thu']) + int(i['fri']) + int(i['sat']) + int(i['sun']))
                for j in n:
                    names.append(getItemName(j, t))
                return render_template("admin/baritem.html", names=names, ar=ar)
        return render_template('errorpages/error.html', error="404", desc="Page Not Found"), 404
    else:
        return redirect("/admin")