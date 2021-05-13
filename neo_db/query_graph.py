# coding=utf-8
from neo_db.config import graph
import codecs
import os
import json
import base64
from functools import reduce

#查询最小维修单元信息
def query_unit(unit):
    data = graph.run(
        "MATCH (error)-[r:cause]-(),(unit)-[:hasError]->(error) WHERE unit.name='%s' RETURN error.alarm,error.name,error.phenomenon,error.solution,r.error_phenomenon,unit.name,unit.belong,unit.info" % (
                unit))
    data = list(data)
    print(data)
    return get_json_data_unit(data)


def query(name):
    if name == 'knowledge_graph':
        data = graph.run(
            "MATCH (error1)-[r1]->(error2),(unit1)-[:hasError]->(error1),(unit2)-[:hasError]->(error2),(unit1)-[r2]-(unit2) return unit1.name,unit1.belong,unit1.info,r2.status,r2.relation,unit2.name,unit2.belong,unit2.info,r1.error_phenomenon"
        )
        data = list(data)
        # print(data)
        return get_json_data1(data)
    else:
        data = graph.run(
            "MATCH (error1)-[r1]->(error2),(unit1)-[:hasError]->(error1),(unit2)-[:hasError]->(error2),(unit1)-[r2]->(unit2) WHERE r1.error_phenomenon=~'%s' RETURN error1.name,error1.alarm,error1.phenomenon,error1.solution,r1.error_phenomenon,error2.name,error2.alarm,error2.phenomenon,error2.solution,unit1.name,unit1.info,unit1.category,unit1.belong,r2.relation,unit2.name,unit2.info,unit2.belong,unit2.category" % (
                        name + '.*'))
        data = list(data)
        print(data)
        return get_json_data(data)


def get_json_data1(data):
    json_data = {'data': [], "links": [],"phenomenon":[]}

    # dataitemstyle = {}
    # dataitemstyle['color'] = '#2a5caa'
    # datatooltip={}
    # datatooltip['formatter']=JScode("""function(x){ return x.data.des;}""")
    for i in data:
        path = i['r1.error_phenomenon']
        path = (path.split('-', 1))
        json_data['phenomenon'].append(path[0])

    run_function = lambda x, y: x if y in x else x + [y]
    json_data['phenomenon'] = reduce(run_function, [[], ] + json_data['phenomenon'])
    for i in data:
        data_item = {}
        data_item['name'] = i['unit1.name']
        # data_item['itemStyle'] = dataitemstyle

        data_item['des'] = i['unit1.info'] + '\nbelong:' + i['unit1.belong']
        data_item['category']=i['unit1.belong']
        # datatooltip = {}
        # datatooltip['formatter'] = i['unit1.info']+'\n belong:'+i['unit1.belong']
        # data_item['tooltip'] = datatooltip
        # data_item['fixed']=True
        json_data['data'].append(data_item)
    for i in data:
        data_item = {}
        data_item['name'] = i['unit2.name']
        # data_item['itemStyle'] = dataitemstyle

        data_item['des'] = i['unit2.info'] + '\nbelong:' + i['unit2.belong']
        # datatooltip = {}
        # datatooltip['formatter'] = i['unit2.info']+'\n belong:'+i['unit2.belong']
        # data_item['tooltip'] = datatooltip
        # data_item['fixed'] = True
        data_item['category'] = i['unit2.belong']
        json_data['data'].append(data_item)

    run_function = lambda x, y: x if y in x else x + [y]
    json_data['data'] = reduce(run_function, [[], ] + json_data['data'])
    # linklinestyle = {}
    # linklinestyle['color'] = '#6e7074'
    for i in data:

        if i['unit2.name'] != 'ZC应用软件':
            link_item = {}
            link_item['source'] = i['unit2.name']

            link_item['target'] = i['unit1.name']
            link_item['value'] = i['r2.status']
            json_data['links'].append(link_item)
        if i['unit1.name'] != 'ZC应用软件':
            link_item = {}
            link_item['source'] = i['unit1.name']

            link_item['target'] = i['unit2.name']
            link_item['value'] = i['r2.status']
            # link_item['lineStyle'] = linklinestyle
            json_data['links'].append(link_item)

    run_function = lambda x, y: x if y in x else x + [y]
    json_data['links'] = reduce(run_function, [[], ] + json_data['links'])
    print('jsondata', json_data)
    print('len', len(json_data['data']))

    return json_data


def get_json_data(data):
    json_data = {'data': [], "links": [], "table_data": []}

    # dataitemstyle = {}
    # dataitemstyle['color'] = '#2a5caa'
    for i in data:
        data_item = {}
        data_item['name'] = i['unit1.name']
        # data_item['des']=i['error1.name']+'alarm:'+i['error1.alarm']+'phenomenon:'+i['error1.phenomenon']+'solution:'+i['error1.solution']
        data_item['des'] = i['unit1.info'] + '\n belong:' + i['unit1.belong']
        # datatooltip = {}
        # datatooltip['formatter'] = i['unit1.info']+'\n belong:'+i['unit1.belong']
        # data_item['tooltip'] = datatooltip
        data_item['alarm'] = i['error1.alarm']
        data_item['error_name'] = i['error1.name']
        data_item['phenomenon'] = i['error1.phenomenon']
        data_item['solution'] = i['error1.solution']
        data_item['unit_category'] = i['unit1.info']
        data_item['belong'] = i['unit1.belong']
        # data_item['itemStyle'] = dataitemstyle
        data_item['category'] = i['unit1.belong']
        json_data['data'].append(data_item)
    for i in data:
        data_item = {}
        data_item['name'] = i['unit2.name']
        # data_item['des'] = i['error2.name'] + 'alarm:' + i['error2.alarm'] + 'phenomenon:' + i['error2.phenomenon'] + 'solution:' + i['error2.solution']
        data_item['des'] = i['unit2.info'] + '\n belong:' + i['unit2.belong']
        # datatooltip = {}
        # datatooltip['formatter'] = i['unit2.info']+'\n belong:'+i['unit2.belong']
        # data_item['tooltip'] = datatooltip
        data_item['alarm'] = i['error2.alarm']
        data_item['error_name'] = i['error2.name']
        data_item['phenomenon'] = i['error2.phenomenon']
        data_item['solution'] = i['error2.solution']
        # data_item['itemStyle'] = dataitemstyle
        data_item['category'] = i['unit2.belong']
        data_item['unit_category'] = i['unit2.info']
        data_item['belong'] = i['unit2.belong']
        json_data['data'].append(data_item)

    run_function = lambda x, y: x if y in x else x + [y]
    json_data['data'] = reduce(run_function, [[], ] + json_data['data'])

    for i in data:
        # 判断链路
        path = i['r1.error_phenomenon']
        path = (path.split('-', 1))
        print(path)

        # if i['r2.relation'] == '双向':
        #     link_item = {}
        #     link_item['source'] = i['unit2.name']
        #
        #     link_item['target'] = i['unit1.name']
        #     link_item['value'] = path[0]
        #     if path[1] == '1':
        #         linklinestyle = {}
        #         linklinestyle['color'] = 'red'
        #     else:
        #         linklinestyle = {}
        #         linklinestyle['color'] = 'black'
        #     link_item['lineStyle'] = linklinestyle
        #     json_data['links'].append(link_item)

        # 需要重写，写一个颜色列表，随机选择
        if len(path) == 1:
            linklinestyle = {}
            linklinestyle['color'] = 'red'

        elif path[1] == '1':
            linklinestyle = {}
            linklinestyle['color'] = 'red'
        else:
            linklinestyle = {}
            linklinestyle['color'] = 'black'

        link_item = {}

        link_item['source'] = i['unit1.name']

        link_item['target'] = i['unit2.name']
        link_item['value'] = path[0]
        link_item['lineStyle'] = linklinestyle
        json_data['links'].append(link_item)

    all_links = []
    # 用于存放表格数据,即每条路的节点分开存储[[],[]...]
    table_data = []
    for i in data:
        all_links.append(i['r1.error_phenomenon'])
    all_links = list(set(all_links))
    all_links = sorted(all_links)

    for path_id in range(len(all_links)):
        # 定义一个列表存放第path_id路径的所有节点信息
        path_id_nodes = []
        for i in data:
            if i['r1.error_phenomenon'] == all_links[path_id]:
                # 查询出的每条结果，都往path_id_nodes里添加头尾两个实体
                head_node_info = {}
                tail_node_info = {}
                head_node_info['node_name'] = i['unit1.name']
                head_node_info['fault_name'] = i['error1.name']
                head_node_info['fault_phenomenon'] = i['error1.phenomenon']
                head_node_info['fault_alarm'] = i['error1.alarm']
                head_node_info['fault_solution'] = i['error1.solution']
                head_node_info['unit_belong'] = i['unit1.belong']
                head_node_info['unit_category'] = i['unit1.info']
                path_id_nodes.append(head_node_info)
                tail_node_info['node_name'] = i['unit2.name']
                tail_node_info['fault_name'] = i['error2.name']
                tail_node_info['fault_phenomenon'] = i['error2.phenomenon']
                tail_node_info['fault_alarm'] = i['error2.alarm']
                tail_node_info['fault_solution'] = i['error2.solution']
                tail_node_info['unit_belong'] = i['unit2.belong']
                tail_node_info['unit_category'] = i['unit2.info']
                path_id_nodes.append(tail_node_info)
        run_function = lambda x, y: x if y in x else x + [y]
        path_id_nodes = reduce(run_function, [[], ] + path_id_nodes)
        table_data.append(path_id_nodes)
        # print(table_data)
    json_data['table_data'] = table_data

    #展示链路节点排序设置：
    showlinks=['TRU车载无线单元','无线网交换机网','ATP网卡板CPU程序','ATP软件','ZC应用平台']
    table_data_sort=[]
    print('testlen',len(json_data['table_data']))
    if len(json_data['table_data'])>1:
        for i in range(5):
            for j in range(5):
                if json_data['table_data'][0][j]['node_name']==showlinks[i]:
                    table_data_sort.append(json_data['table_data'][0][j])
                    break
        json_data['table_data'][0]=table_data_sort


    print('jsondata', json_data)

    return json_data

def get_json_data_unit(data):
    json_data = {"unit_data": [],"error_data": [],"phenomenon":[]}

    for i in data:
        data_item = {}
        #获取不带标识的故障现象error_phenomenon
        path=i['r.error_phenomenon']
        path = (path.split('-', 1))
        path=path[0]
        data_item['phenomenon']=path
        json_data['phenomenon'].append(data_item)

    for i in data:


        data_item = {}
        data_item['error_name'] = i['error.name']
        data_item['error_alarm'] = i['error.alarm']
        data_item['error_phenomenon'] = i['error.phenomenon']
        data_item['error_solution'] = i['error.solution']
        json_data['error_data'].append(data_item)

    for i in data:

        data_item = {}
        data_item['unit_name'] = i['unit.name']
        data_item['unit_belong'] = i['unit.belong']
        data_item['unit_category'] = i['unit.info']
        json_data['unit_data'].append(data_item)

    run_function = lambda x, y: x if y in x else x + [y]
    json_data['unit_data'] = reduce(run_function, [[], ] + json_data['unit_data'])
    run_function = lambda x, y: x if y in x else x + [y]
    json_data['error_data'] = reduce(run_function, [[], ] + json_data['error_data'])
    run_function = lambda x, y: x if y in x else x + [y]
    json_data['phenomenon'] = reduce(run_function, [[], ] + json_data['phenomenon'])

    print('unit_jsondata', json_data)

    return json_data
# f = codecs.open('./static/test_data.json','w','utf-8')
# f.write(json.dumps(json_data,  ensure_ascii=False))
# def get_KGQA_answer(array):
#     print("1", array)
#     data_array = []
#     for i in range(len(array) - 2):
#         if i == 0:
#             name = array[0]
#             print("name", name)
#         else:
#             name = data_array[-1]['p.Name']
#
#         data = graph.run(
#             "match(p)-[r:%s{relation: '%s'}]->(n:Person{Name:'%s'}) return  p.Name,n.Name,r.relation,p.cate,n.cate" % (
#                 similar_words[array[i + 1]], similar_words[array[i + 1]], name)
#         )
#         print(
#             "match(p)-[r:%s{relation: '%s'}]->(n:Person{Name:'%s'}) return  p.Name,n.Name,r.relation,p.cate,n.cate" % (
#                 similar_words[array[i + 1]], similar_words[array[i + 1]], name))
#         data = list(data)
#         print("2", data)
#         data_array.extend(data)
#
#         print("===" * 36)
#     with open("./spider/images/" + "%s.jpg" % (str(data_array[-1]['p.Name'])), "rb") as image:
#         base64_data = base64.b64encode(image.read())
#         b = str(base64_data)
#
#     return [get_json_data(data_array), get_profile(str(data_array[-1]['p.Name'])), b.split("'")[1]]

#
# def get_answer_profile(name):
#     with open("./spider/images/" + "%s.jpg" % (str(name)), "rb") as image:
#         base64_data = base64.b64encode(image.read())
#         b = str(base64_data)
#     return [get_profile(str(name)), b.split("'")[1]]
