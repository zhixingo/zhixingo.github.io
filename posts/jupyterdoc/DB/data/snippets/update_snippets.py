import json
import config
import pprint

### 该脚本配合jupyter插件snippets使用，允许增加和更新（统称为update，如果name不存在，则为新增ADD，否则为修改CHANGE）以及删除（delete）插件预设的代码段
'''格式（新建一个名为config.py的文本文件，以字典形式写入，并交付给变量snippets_config，具体请参阅./config.py示例）：
{
  'update':[
    {'name':<name1>,'code':<code1>},
    {'name':<name2>,'code':<code2>},
    ...
  ],
  'delete':[
    <name1>,<name2>,...
  ]
}
注意，请勿同时对某一name进行update和delete，这既不符合现实，也将导致错误，因为字典中元素的顺序是不定的，没人知道是先update还是先delete，尽管你写的顺序是update在delete前，但这不是决定因素
另设置变量execute，其值为True则执行配置，否则不执行，默认为True
'''

snippets_path=r'E:\myworld\anaconda\share\jupyter\nbextensions\snippets\snippets.json'

if config.execute:
    with open(snippets_path,'r',encoding='utf-8') as f:
        old_config=json.load(f)
    print('**旧配置**')
    pprint.pprint(old_config)
    for op,records in config.snippets_config.items():
        for record in records:
            if op=='update':
                print('更新：%s'%(record['name']))
                if record['name'] not in [i['name'] for i in old_config['snippets']]: #ADD
                    old_config['snippets'].append(record)
                else: #CHANGE
                    for i,e in enumerate(old_config['snippets']):
                        if record['name']==e['name']:
                            old_config['snippets'][i]['code']=record['code']
            elif op=='delete':
                print('删除：%s'%(record))
                for i,e in enumerate(old_config['snippets']):
                    if record==e['name']:
                        old_config['snippets'].pop(i)
    print('**新配置**')
    pprint.pprint(old_config)
    with open(snippets_path,'w',encoding='utf-8') as f:
        json.dump(old_config,f,ensure_ascii=False,indent=4,separators=(',',': ')) #参数说明请见高级/文档/json模块.md
else:
    print('当前已关闭配置修改')