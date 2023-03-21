#!/usr/bin/python
# -*- coding: UTF-8 -*-
import os
import re
import xml.etree.cElementTree as et
import zipfile
import shutil
import hashlib


workpath = f"{os.path.dirname(__file__)}/.."

addons_xml = et.Element('addons')

# 匹配所有需要处理的kodi插件
for pluginname in os.listdir(workpath):
    if re.search('[停止更新]|video.vid|bangumi|cine|reallive', pluginname):
        # 跳过停止更新的项目
        pass
    elif re.search('metadata.*', pluginname) or re.search('plugin.*', pluginname) or re.search('service.*', pluginname):
        # 读取xml获取版本
        parser = et.parse(f"{workpath}/{pluginname}/addon.xml")
        root = parser.getroot()
        version = root.attrib['version']
        # 创建repo
        basepath = f"{workpath}/repo/{pluginname}/"
        if not os.path.exists(basepath):
            os.makedirs(basepath)
        # 压缩
        zippath = basepath + str(pluginname) + '-' + version + '.zip'
        f = zipfile.ZipFile(zippath, 'w', zipfile.ZIP_DEFLATED)
        for dirpath, dirnames, filenames in os.walk(f'{workpath}/{pluginname}'):
            # 这一句很重要，不replace的话，就从根目录开始复制
            fpath = dirpath.replace(f'{workpath}/', '')
            fpath = fpath and fpath + os.sep or ''  # 这句话理解我也点郁闷，实现当前文件夹以及包含的所有文件的压缩
            for filename in filenames:
                f.write(os.path.join(dirpath, filename), fpath+filename)
        print(f'{pluginname} 压缩成功')
        f.close()
        # 拷贝icon
        shutil.copy(f'{workpath}/{str(pluginname)}/icon.png', f'{basepath}icon.png')

        # 合并xml
        addons_xml.append(root)
# 输出addons.xml
tree = et.ElementTree(addons_xml)
tree.write(f'{workpath}/addons.xml', "UTF-8", xml_declaration=True)
with open(f'{workpath}/addons.xml', 'r') as f:
    m2 = hashlib.md5()
    text = f.read()
    m2.update(text.encode())
with open(f'{workpath}/addons.xml.md5', 'w') as f: # 如果filename不存在会自动创建， 'w'表示写数据，写之前会清空文件中的原有数据！
    f.write(m2.hexdigest())
    f.close()
