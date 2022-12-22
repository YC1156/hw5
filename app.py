from flask import Flask, render_template, jsonify,redirect,url_for, request
import pandas as pd
from six.moves import urllib
import requests
import json


app = Flask(__name__)
 
@app.route("/")
def index():
    return render_template('indexNoAI.html')
@app.route("/AI_LR")
def AI1():
    return render_template('indexAI.html')
@app.route("/AI_SVC")
def AI2():
    return render_template('indexAI2.html')
# @app.route("/NoAI")
# def NoAI():
#     return render_template('indexNoAI.html')
@app.route("/getData")
def getData():
    myserver ="localhost"
    myuser="test123"
    mypassword="test123"
    mydb="aiotdb"
    
    debug =0
    from  pandas import DataFrame as df
    import pandas as pd                     # 引用套件並縮寫為 pd
    import numpy as np

    import pymysql.cursors
    #db = mysql.connector.connect(host="140.120.15.45",user="toto321", passwd="12345678", db="lightdb")
    #conn = mysql.connector.connect(host=myserver,user=myuser, passwd=mypassword, db=mydb)
    conn = pymysql.connect(host=myserver,user=myuser, passwd=mypassword, db=mydb)

    c = conn.cursor()
    if debug:
        input("pause.. conn.cursor() ok.......")

    #====== 執行 MySQL 查詢指令 ======#
    c.execute("SELECT * FROM sensors")

    #====== 取回所有查詢結果 ======#
    results = c.fetchall()
    print(type(results))
    print(results[:10])
    if debug:
        input("pause ....select ok..........")

    test_df = df(list(results),columns=['id','time','value','temp','humi','status'])

    print(test_df.head(10))
    result = test_df.to_dict(orient='records')
    seq = [[item['id'], item['time'], item['value'], item['temp'], item['humi'], item['status']] for item in result]
    return jsonify(seq)
    ######### cursor close, conn close
    c.close()
    conn.close()
    
@app.route("/LR")
def getPredictLR():
    #==== step 1: setup variable ===========
    myserver ="localhost"
    myuser="test123"
    mypassword="test123"
    mydb="aiotdb"
    
    debug =0
    from  pandas import DataFrame as df
    import pandas as pd                     # 引用套件並縮寫為 pd
    import numpy as np

    #step 2: load model  #讀取Model###
    import pickle
    import gzip
    with gzip.open('./myModel.pgz', 'r') as f:
        model = pickle.load(f)

    # step 3:　get test data from database        
    

    import pymysql.cursors
    #db = mysql.connector.connect(host="140.120.15.45",user="toto321", passwd="12345678", db="lightdb")
    #conn = mysql.connector.connect(host=myserver,user=myuser, passwd=mypassword, db=mydb)
    conn = pymysql.connect(host=myserver,user=myuser, passwd=mypassword, db=mydb)
    
    c = conn.cursor()
    if debug:
        input("pause.. conn.cursor() ok.......")
    
    #====== 執行 MySQL 查詢指令 ======#
    c.execute("SELECT * FROM sensors")
    
    #====== 取回所有查詢結果 ======#
    results = c.fetchall()
    print(type(results))
    print(results[:10])
    if debug:
        input("pause ....select ok..........")
    
    test_df = df(list(results),columns=['id','time','value','temp','humi','status'])
    
    print(test_df.head(10))
   

    
    testX=test_df['value'].values.reshape(-1,1)
    testY=model.predict(testX)
    print(model.score(testX,testY))
    
    test_df['status']=testY
    print(test_df.head(10))
    
    if debug:
        input("pause.. now show correct one above.......")
    

 
    
    #########################################
    '''
    ##Example 1 ## write back mysql ###############
    threshold =100
    c.execute('update light set status=0 where value>'+str(threshold))
    conn.commit()
    #results = c.fetchall()
    #print(type(results))
    #print(results[:10])
    input("pause ....update ok..........")
    '''
    
    
    ##Example 2 ## write back mysql ###############
    ## make all status =0
    c.execute('update sensors set status=0 where true')
    
    ## choose status ==1 have their id available
    id_list=list(test_df[test_df['status']==1].id)
    print(id_list)
                
    for _id in id_list:
        #print('update light set status=1 where id=='+str(_id))
        c.execute('update sensors set status=1 where id='+str(_id))
    
    conn.commit()
    
   
    result = test_df.to_dict(orient='records')
    seq = [[item['id'], item['time'], item['value'], item['temp'], item['humi'], item['status']] for item in result]
    return jsonify(seq)

@app.route("/SVC")
def getPredictSVC():
    #==== step 1: setup variable ===========
    myserver ="localhost"
    myuser="test123"
    mypassword="test123"
    mydb="aiotdb"
    
    debug =0
    from  pandas import DataFrame as df
    import pandas as pd                     # 引用套件並縮寫為 pd
    import numpy as np

    #step 2: load model  #讀取Model###
    import pickle
    import gzip
    with gzip.open('./mySVCModel.pgz', 'r') as f:
        model = pickle.load(f)

    # step 3:　get test data from database        
    

    import pymysql.cursors
    #db = mysql.connector.connect(host="140.120.15.45",user="toto321", passwd="12345678", db="lightdb")
    #conn = mysql.connector.connect(host=myserver,user=myuser, passwd=mypassword, db=mydb)
    conn = pymysql.connect(host=myserver,user=myuser, passwd=mypassword, db=mydb)
    
    c = conn.cursor()
    if debug:
        input("pause.. conn.cursor() ok.......")
    
    #====== 執行 MySQL 查詢指令 ======#
    c.execute("SELECT * FROM sensors")
    
    #====== 取回所有查詢結果 ======#
    results = c.fetchall()
    print(type(results))
    print(results[:10])
    if debug:
        input("pause ....select ok..........")
    
    test_df = df(list(results),columns=['id','time','value','temp','humi','status'])
    
    print(test_df.head(10))
   

    
    testX=test_df['value'].values.reshape(-1,1)
    testY=model.predict(testX)
    print(model.score(testX,testY))
    
    test_df['status']=testY
    print(test_df.head(10))
    
    if debug:
        input("pause.. now show correct one above.......")
    

 
    
    #########################################
    '''
    ##Example 1 ## write back mysql ###############
    threshold =100
    c.execute('update light set status=0 where value>'+str(threshold))
    conn.commit()
    #results = c.fetchall()
    #print(type(results))
    #print(results[:10])
    input("pause ....update ok..........")
    '''
    
    
    ##Example 2 ## write back mysql ###############
    ## make all status =0
    c.execute('update sensors set status=0 where true')
    
    ## choose status ==1 have their id available
    id_list=list(test_df[test_df['status']==1].id)
    print(id_list)
                
    for _id in id_list:
        #print('update light set status=1 where id=='+str(_id))
        c.execute('update sensors set status=1 where id='+str(_id))
    
    conn.commit()
    
   
    result = test_df.to_dict(orient='records')
    seq = [[item['id'], item['time'], item['value'], item['temp'], item['humi'], item['status']] for item in result]
    return jsonify(seq)

@app.route("/random")
def random():
    debug =0
    # return redirect(requests.referrer or url_for('index')) 
    myserver ="localhost"
    myuser="test123"
    mypassword="test123"
    mydb="aiotdb"
    import pymysql.cursors
    #db = mysql.connector.connect(host="140.120.15.45",user="toto321", passwd="12345678", db="lightdb")
    #conn = mysql.connector.connect(host=myserver,user=myuser, passwd=mypassword, db=mydb)
    conn = pymysql.connect(host=myserver,user=myuser, passwd=mypassword, db=mydb)
    
    c = conn.cursor()
    if debug:
        input("pause.. conn.cursor() ok.......")
    c.execute('update sensors set status=RAND() where true')
    conn.commit()
    
    # return redirect(request.referrer or url_for('index')) 
    return redirect(url_for('index')) 
    

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True,port="8080")
