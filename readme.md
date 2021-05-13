#故障分析知识图谱demo
###文件
1.app.py是整个系统的主入口  
2.templates文件夹是HTML的页面  
  knowledgegraph.html是图谱展示页面  
3.static文件夹存放css和js,是页面的样式和效果的文件   
4.neo_db文件夹是知识图谱构建模块  
 config.py配置参数  
 query_graph.py是知识图谱的查询  


###部署步骤  
1.按照所需的库，执行pip install -r requirement.txt  
2.安装好neo4j图数据库，导入数据。修改neo_db目录下config.py,设置图数据库的账号和密码。  
3.运行python app.py,浏览器打开localhost:5000即可查看

