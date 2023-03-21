import json

class JSONProcessor:
    def init(self, data):
        self.json_string = json.load(data)
        self.pens_list = self.json_string['pens']

    def cut_redundancy(self):
        # 后端需要恢复画布，所以前端传过来画布的所有信息。但是处理连接关系的时候不需要部分信息，这里去掉不需要的部分
        for i in self.pens_list:
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
        return self

    def get_all_id(self):
        return [i['id'] for i in self.pens_list]

    def get_modules(self): # 返回原始的模型列表 (惰性)
        return filter(lambda pen: 'children' in pen.keys(), self.pens_list)

    def get_modules_with_interfaces(self): # 返回模型字典，值为其拥有的的接口列表
        modules = {}
        for pen in self.get_modules():
            pen['children'] # 含有children属性的为模型
            modules[pen['id']] = []

            # print('含有的所有接口如下:')
            for child_id in pen['children']:
                child = filter(lambda x: x['id'] == child_id, self.pens_list)
                for i in child: # 符合条件的理论上只有一个
                    modules[pen['id']].append(i)
        return modules

    def get_lines(self): # 返回原始的连线(惰性)
        return filter(lambda pen: pen['name'] == 'line', self.pens_list)

    def get_lines_with_interfaces(self): # 返回连线（字典），值为其拥有的接口列表
        lines = {}
        # print('所有连线，给出了哪两个接口相连')
        for pen in filter(lambda pen:pen['name'] == 'line', self.pens_list):
            # print(pen)
            lines[pen['id']] = []
            # print('该连线连接的两个接口的id')
            for anchor in pen['anchors']:
                try:
                    id = anchor['connectTo']
                    lines[pen['id']].append(id)
                except:
                    pass
        return lines

    def get_pens_list(self):
        return self.pens_list

    def get_modules_with_pos(self, module): # useless
        x = module['x']
        y = module['y']
        width = module['width']
        height = module['height']
        return (x, y, width, height)

    def find_contained_modules(self): # 返回组件之间的关系: 硬件包含的组件，根据位置计算
        modules = self.get_modules()
        # 初始化包含关系字典
        contained_modules = {module['id']: [] for module in modules}

        # 遍历每个矩形并找到包含它的矩形
        for i, outer_rect in enumerate(modules):
            for j, inner_rect in enumerate(modules):
                # 不检查自身矩形
                if i == j:
                    continue

                # 如果inner_rect被outer_rect包含，则将inner_rect添加到outer_rect的包含列表中
                if (inner_rect['x'] >= outer_rect['x'] and
                        inner_rect['y'] >= outer_rect['y'] and
                        inner_rect['x'] + inner_rect['width'] <= outer_rect['x'] + outer_rect['width'] and
                        inner_rect['y'] + inner_rect['height'] <= outer_rect['y'] + outer_rect['height']):
                    contained_modules[outer_rect['id']].append(inner_rect['id'])

        return contained_modules

