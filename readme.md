**故障分析知识图谱demo**

**文件**

1.app.py：系统的入口  
2.templates  
3.static
4.neo_db
  config.py：数据库配置参数  
  query_graph.py：主程序  


**部署步骤**

1.按照所需的库，执行pip install -r requirement.txt  
2.安装好neo4j图数据库，导入数据
3.修改neo_db目录下config.py,设置图数据库的账号和密码  
4.运行python app.py,浏览器打开localhost:5000即可查看

