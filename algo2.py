import re

def get_sources():
    f = open("restaurants/restaurant1_restaurant2_goldstandard.rdf", "r")
    sources1=[]
    sources2=[]
    restau = []
    for l in f:
        if 'restaurant1' in l :
            sources1.append(l[l.index('=')+2:][:-4])
        if 'restaurant2' in l :
            sources2.append(l[l.index('=')+2:][:-4])
    for i in sources1:
        restau.append((i[i.index('-') + 1:],i[i.index('-') + 1:]))

    return sources1,sources2,restau

sources1, sources2, restau=get_sources()

def get_data_from_sources1(sources1):
    data1=[]
    for s in sources1:
        with open("restaurants/restaurant1.rdf", "r") as f1:
            for l in f1:
                if s in l and l[l.index(s)+len(s)]=='\"':
                    obj={}
                    has_address=next(f1)
                    obj['has_address']=has_address[has_address.index('=')+2:][:-4]
                    category=next(f1)
                    obj['category']=category[category.find('category>')+len('category>'):category.rfind('</')]
                    phone_number = next(f1)
                    obj['phone_number'] = phone_number[phone_number.find('phone_number>') + len('phone_number>'):phone_number.rfind('</')]
                    name = next(f1)
                    obj['name'] = name[name.find('name>') + len('name>'):name.rfind('</')]
                    data1.append({s.split('-')[1]:obj})

    for i in range(len(data1)):
        with open("restaurants/restaurant1.rdf", "r") as f1:
            for l in f1:
                has_address=data1[i]['Restaurant' + str(i)]['has_address']
                if has_address in l and l[l.index(has_address)+len(has_address)]=='\"':
                    is_in_city=next(f1)
                    if 'is_in_city' in is_in_city:
                        data1[i]['Restaurant' + str(i)]['is_in_city']=is_in_city[is_in_city.index('=')+2:][:-4]
                        street=next(f1)
                        data1[i]['Restaurant' + str(i)]['street']=street[street.find('street>') + len('street>'):street.rfind('</')]

    for i in range(len(data1)):
        with open("restaurants/restaurant1.rdf", "r") as f1:
            for l in f1:
                is_in_city = data1[i]['Restaurant' + str(i)]['is_in_city']
                if is_in_city in l and l[l.index(is_in_city) + len(is_in_city)] == '\"':
                    city_name = next(f1)
                    if 'name>' in city_name:
                        data1[i]['Restaurant' + str(i)]['city_name'] = city_name[city_name.find('name>') + len('name>'):city_name.rfind('</')]
    return data1


def get_data_from_sources2(sources2):
    data2=[]
    for s in sources2:
        with open("restaurants/restaurant2.rdf", "r") as f1:
            for l in f1:
                if s in l and l[l.index(s)+len(s)]=='\"':
                    obj={}
                    has_address=next(f1)
                    obj['has_address']=has_address[has_address.index('=')+2:][:-4]
                    has_category=next(f1)
                    obj['has_category']=has_category[has_category.index('=')+2:][:-4]
                    phone_number = next(f1)
                    obj['phone_number'] = phone_number[phone_number.find('phone_number>') + len('phone_number>'):phone_number.rfind('</')]
                    name = next(f1)
                    obj['name'] = name[name.find('name>') + len('name>'):name.rfind('</')]
                    data2.append({s.split('-')[1]:obj})

    for i in range(len(data2)):
        with open("restaurants/restaurant2.rdf", "r") as f1:
            for l in f1:
                if 'Restaurant' + str(i) in data2[i].keys():
                    has_address=data2[i]['Restaurant' + str(i)]['has_address']
                    if has_address in l and l[l.index(has_address)+len(has_address)]=='\"':
                        city=next(f1)
                        if 'city>' in city:
                            data2[i]['Restaurant' + str(i)]['city']=city[city.find('city>') + len('city>'):city.rfind('</')]
                            street=next(f1)
                            data2[i]['Restaurant' + str(i)]['street']=street[street.find('street>') + len('street>'):street.rfind('</')]

    for i in range(len(data2)):
        with open("restaurants/restaurant2.rdf", "r") as f1:
            for l in f1:
                if 'Restaurant' + str(i) in data2[i].keys():
                    has_category = data2[i]['Restaurant' + str(i)]['has_category']
                    if has_category in l and l[l.index(has_category) + len(has_category)] == '\"':
                        category_name = next(f1)
                        if 'name>' in category_name:
                            data2[i]['Restaurant' + str(i)]['category_name'] = category_name[category_name.find('name>') + len('name>'):category_name.rfind('</')]
    return data2


def get_idx1_idx2(data1,data2):
    idx1=[]
    for i in data1:
        for j in i.keys():
            for k in i[j].keys():
                idx1.append({i[j][k]:{j:k}})
    idx2=[]
    for i in data2:
        for j in i.keys():
            for k in i[j].keys():
                idx2.append({i[j][k]:{j:k}})
    return idx1,idx2


def first_step():

    data1=get_data_from_sources1(sources1)
    data2=get_data_from_sources2(sources2)
    return get_idx1_idx2(data1,data2)

rest1, rest2 = first_step()


def get_keys(list1, list2):
    res = []
    for i in list1:
        res.append(list(i.keys())[0])
    for i in list2:
        res.append(list(i.keys())[0])
    return list(set(res))


def algo2():
    items = get_keys(rest1, rest2)
    resdix = {}
    for i in items:
        i = re.sub('/', '-', i)
        for j in rest1:
            if re.sub('/', '-', list(j.keys())[0]) == i:
                for k in rest2:
                    if re.sub('/', '-', list(k.keys())[0]) == i:
                        dic1 = j[list(j.keys())[0]]
                        dic2 = k[list(k.keys())[0]]
                        key1 = list(dic1.keys())[0]
                        key2 = list(dic2.keys())[0]
                        if key1!=key2:
                            print(1)
                        if (key1, key2) in list(resdix.keys()):
                            if ((dic1[key1], dic2[key2]) not in resdix[(key1, key2)]):
                                resdix[(key1, key2)].append((dic1[key1], dic2[key2]))
                        elif (key2, key1) in list(resdix.keys()):
                            resdix[(key2, key1)].append((dic2[key2], dic1[key1]))
                        else:
                            resdix[(key1, key2)] = [(dic1[key1], dic2[key2])]
    return resdix




resdix=algo2()
print(resdix)

def quality(r,Lplus):

    Lddprim=[];
    for i in list(resdix.keys()):

        bool=True
        for x in r:
            if x not in resdix[i]:
                bool=False
        if bool==True:
            Lddprim.append(i)
    n=len(Lplus)
    inter=[]
    x=len(Lddprim)
    for i in Lddprim:
        if i in Lplus:
            inter.append(i)
    m=len(inter)
    recall=0
    prec=0
    if n!=0:
        recall=m/n
    if x!=0:
        prec=m/x
    return recall,prec

print(quality([('name', 'name')],restau))
print(quality([('city_name', 'city')],restau))
print(quality([('city_name', 'city'),('name', 'name')],restau))
print(quality([('phone_number', 'phone_number')],restau))
print(quality([('city_name', 'city'),('phone_number', 'phone_number')],restau))
print(quality([('city_name', 'city'),('name', 'name'),('phone_number', 'phone_number')],restau))
print(quality([('name', 'name'),('phone_number', 'phone_number')],restau))