### 请调用handle_json.py


## json_processing.py 是类的形式，未测试。

### 使用示例

'''python
with open('data.json') as f:
data = f.read()
processor = JSONProcessor(data)
pens_list = processor.get_pens_list()
modules = processor.cut_redundancy().get_modules_with_interfaces()
lines = processor.get_lines_with_interfaces()
'''