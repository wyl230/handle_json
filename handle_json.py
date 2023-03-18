import json 

def get_json_string(data):
    return json.load(data)

def get_pens_list(json_string):
    return json_string['pens']

def cut_redundancy(pens_list):
    # 后端需要恢复画布，所以前端传过来画布的所有信息。但是处理连接关系的时候不需要部分信息，这里去掉不需要的部分
    for i in pens_list:
        try:
            i.pop('x')
            i.pop('y')
            i.pop('width')
            i.pop('height')
            i.pop('lineWidth')
            i.pop('lineHeight')
            i.pop('fontSize')
            i.pop('rotate') # line类型不包含rotate属性
        except:
            pass
    return pens_list

def get_all_id():
    return [i['id'] for i in pens_list]

def get_modules_with_interfaces(pens_list):
    modules = {}
    for pen in pens_list:
        try:
            pen['children'] # 含有children属性的为模型
            modules[pen['id']] = []

            # print('含有的所有接口如下:')
            for child_id in pen['children']:
                child = filter(lambda x: x['id'] == child_id, pens_list)
                for i in child: # 符合条件的理论上只有一个
                    modules[pen['id']].append(i)
        except:
            pass

def get_lines_with_interfaces(pens_list):
    lines = {}
    # print('所有连线，给出了哪两个接口相连')
    for pen in filter(lambda pen:pen['name'] == 'line', pens_list):
        # print(pen)
        lines[pen['id']] = []
        print('该连线连接的两个接口的id')
        for anchor in pen['anchors']:
            try:
                id = anchor['connectTo']
                lines[pen['id']].append(id)
            except:
                pass
            
