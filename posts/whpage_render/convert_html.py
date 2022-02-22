from lxml import etree
from copy import deepcopy
import re

'''
render origin html(no css) exported by Typora with specified html template.
muggledy 2021.10.16
'''

def addwrap(ele, wrapper, clss=None):
    wrapper_ele = wrapper if isinstance(wrapper, etree._Element) \
        else etree.Element(wrapper)
    wrapper_ele.insert(0, deepcopy(ele)) #don't know why need deepcopy here, otherwise, error
    if clss is not None:
        wrapper_ele = addcls(wrapper_ele, clss)
    return wrapper_ele

def addcls(ele, clss):
    ele = deepcopy(ele)
    ele.set('class', ' '.join(clss) \
        if isinstance(clss, (list,tuple)) else clss)
    return ele

def delwrap(ele): #ele should be the wrapper itself
    return deepcopy(ele.getchildren())

def replacewrap(ele, wrapper, clss=None): #ele should be the wrapper itself
    wrapper_ele = wrapper if isinstance(wrapper, etree._Element) \
        else etree.Element(wrapper)
    wrapper_ele.extend(ele.getchildren())
    wrapper_ele.text = ele.text
    if clss is not None:
        wrapper_ele = addcls(wrapper_ele, clss)
    return wrapper_ele

def delele(ele):
    return None

def appendele(ele, append, text=None):
    append_ele = append if isinstance(append, etree._Element) \
        else etree.Element(append)
    if text is not None:
        append_ele.text = text
    return append_ele

def anchorhx(ele):
    ele = deepcopy(ele)
    ele.set('id', (ele.text if ele.text is not None else '') + ''.join([ \
        tostring(_) for _ in ele.getchildren()]))
    return ele

def setproperty(ele, key, value):
    ele = deepcopy(ele)
    ele.set(key, value)
    return ele

def alter_eles(html, xpath, operation, inplace=True, \
               **kwargs):
    eles = html.xpath(xpath) if isinstance(xpath, str) else \
        (xpath if isinstance(xpath, (list,tuple)) else [xpath])
    if not inplace:
        ret = []
    for ele in eles:
        _ = operation(ele, **kwargs) #operation must be non-inplace, return the altered ele
        if not inplace:
            ret.append(_)
        else:
            if operation == delwrap: #special case, slightly different from replace
                ele_parent = ele.getparent()
                if ele.text is not None:
                    ele_parent.text = ele.text
                index = ele_parent.index(ele)
                ele_parent.remove(ele)
                for i,e in enumerate(_):
                    ele_parent.insert(index + i, e)
            elif operation == delele:
                ele.getparent().remove(ele)
            elif operation == appendele:
                ele.addnext(_)
            else:
                ele.getparent().replace(ele, _)
    if not inplace:
        return ret

def convert_html(file, template=None, contexts=None, \
                 filters=None, **kwargs):
    '''render origin html(no css) exported by Typora with specified 
       html template
       in addition, filters can be passed to modify the attribute 
       or value of the specified html tags(also can be located by class 
       or id), e.g. <span id="xxx">some text</span> can be converted to 
       <span id="xxx" class="yyy">some text</span>, an attribute named 
       yyy is added to html element xxx
       note that filters has order, e.g. filters=[filter0, filter1], so 
       filter1 is applied on the html etree that processed by filter0
       filters works before template(you can pass some calculated value 
       into contexts for rendering)
       see https://lxml.de/apidoc/lxml.etree.html
    '''
    html = file if isinstance(file, etree._ElementTree) \
        else etree.parse(file, etree.HTMLParser())
    if filters is not None:
        filters = filters if isinstance(filters, (list,tuple)) else [filters]
        for _filter in filters:
            alter_eles(html, _filter['xpath'], _filter['operation'], \
                inplace=True, \
                **{k:v for k,v in _filter.items() if k not in ['xpath', 'operation']})
    if template is not None and contexts is not None:
        contexts_vars = {}
        for k, (p, f) in contexts.items(): #variable_name, xpath, flag
            if f == 'value':
                s = p
            else:
                v = html.xpath(p)[0]
                if f == 'nowrapper':
                    s = (v.text if v.text is not None else '') + ''.join([ \
                        tostring(_) for _ in v.getchildren()])
                else:
                    s = tostring(v)
            contexts_vars[k] = s
        with open(template, 'r', encoding='utf-8') as f:
            rendered = f.read()
            for k, v in contexts_vars.items():
                rendered = re.sub(r'{% *?'+k+' *?%}', v, rendered)
            return singletag2double(rendered, kwargs.get('which'))
    return singletag2double(tostring(html), \
        kwargs.get('which'))

def singletag2double(html_str, which=None):
    which = which if isinstance(which, (list,tuple)) else [which]
    for _ in which:
        html_str = re.sub(r'<'+_+r' *?(.*?) *?/>', \
            r'<'+_+r'\1></'+_+r'>', html_str)
    return html_str

def tostring(ele):
    return etree.tostring(ele, encoding="utf-8").decode('utf-8')

if __name__ == '__main__':
    import os.path
    import time
    start_anchor = time.time()
    filename = 'demo.html'
    file = os.path.join(os.path.dirname(__file__), filename)
    html = etree.parse(file, etree.HTMLParser())
    header = alter_eles(html, '//h1', addwrap, inplace=False, wrapper='header')[0]
    alter_eles(header, '//h1', anchorhx, inplace=True)
    header = tostring(header)
    rendered = convert_html(html, filters=[
        {'xpath':'//pre/code', 'operation':replacewrap, 'wrapper':'div', 'clss':'code'}, \
        {'xpath':'//pre', 'operation':delwrap}, \
        {'xpath':'//table', 'operation':addwrap, 'wrapper':'div', 'clss':'table'}, \
        {'xpath':'//div[text()="[TOC]"]', 'operation':delele}, \
        {'xpath':'//p[./img]', 'operation':replacewrap, 'wrapper':'center'}, \
        {'xpath':'//h1', 'operation':delele}, \
        {'xpath':'//li[./input[@type="checkbox"]]/p', 'operation':addcls, 'clss':'inline'}, \
        {'xpath':'//li[./input[@type="checkbox"]]', 'operation':addcls, 'clss':'nostyle'}, \
        {'xpath':'//blockquote', 'operation':replacewrap, 'wrapper':'div', 'clss':'tip'}, \
        {'xpath':'//div[@class="tip"]/p', 'operation':delwrap}, \
        {'xpath':'//div[@mdtype="math_block"]', 'operation':addwrap, 'wrapper':'center'}, \
        #{'xpath':'//li/input[@type="checkbox"]', 'operation':setproperty, 'key':'disabled', 'value':'disabled'}, \
        {'xpath':'//video', 'operation':addwrap, 'wrapper':'center'}, \
        {'xpath':'//h2[1]', 'operation':appendele, 'append':'address', 'text':'2022.1.7 @muggledy'}, \
        {'xpath':'//*[local-name() = "h2" or local-name() = "h3" or local-name() = "h4" ' \
            'or local-name() = "h5" or local-name() = "h6"]', 'operation':anchorhx}], \
        template=os.path.join(os.path.dirname(__file__),'template'), \
        contexts={'header':[header,'value'], 'body':['//body','nowrapper'], 'title':['VANH WEB NOTE','value']}, \
        which=['video', 'iframe']
    )
    with open(os.path.join(os.path.dirname(__file__), f'rendered_{filename}'), 'w', encoding='utf-8') as f:
        f.write(rendered)
    print(f'[OK] Time consumes: {time.time()-start_anchor:.2f}s!')