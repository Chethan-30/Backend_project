from flask import Flask, render_template, request
import psycopg2

app = Flask(__name__)

def getconn():
  return psycopg2.connect(host="10.17.50.87",database="group_4",user="group_4",password="scBdTqWSD3c1We")


@app.route('/')
def index():
    return render_template('mainpage1.html')

@app.route('/notfound',methods=['POST'])
def handle_exit():
    return render_template('mainpage1.html')




@app.route('/mainpage1', methods=['POST'])
def page_choose():
    request1=request.form.get('b1')

    f=open("req.txt",'w')
    f.write(request1)
    f.close()
    
    if(request1=='24'):
      conn=getconn()
      cur = conn.cursor()
      cur.execute('SELECT DISTINCT Types_of_symptoms.name FROM Types_of_symptoms')
      results = cur.fetchall()
      temp=[]
      for i in range(0,len(results)):
         temp.append(results[i][0])
        
      return render_template('query_24.html',length=len(temp),result=temp)


    if(request1=='25'):
      conn=getconn()
      cur = conn.cursor()
      cur.execute('SELECT DISTINCT Types_of_symptoms.name FROM Types_of_symptoms')
      results = cur.fetchall()
      temp=[]
      for i in range(0,len(results)):
         temp.append(results[i][0])

      return render_template('query_25.html',length=len(temp),result=temp)

    if(request1=='29'):
        print('yessdssdsf')
        return render_template('insert.html')

    if(request1=='18'):
        return render_template('mpg3.html')      
    
    return render_template('mpg2.html')


@app.route('/', methods=['POST'])
def rtv():
    request1 = request.form.get('input33')
    gr=request1
    f=open("req.txt",'w')
    f.write(request1)
    f.close()
    # print('this is my query and it is succesfully retrieved',request1)

    return render_template('mpg2.html')


@app.route('/query_25', methods=['POST'])
def get_25_input():
    
    requests=[]
    requests.append(request.form.get('input1'))
    requests.append(request.form.get('input2'))
    requests.append(request.form.get('input3'))
    requests.append(request.form.get('input4'))
    requests.append(request.form.get('input5'))
    requests.append(request.form.get('input6'))

    rlist='('
    num_of_symptoms=0
    for i in range(0,6):
     if(requests[i]!='none' and requests[i]!=None):
       num_of_symptoms=num_of_symptoms+1 
       rlist+="'"
       rlist+=requests[i]
       rlist+="'"
       rlist+=','
        
    rlist=rlist[:-1]
    rlist+=')'
    if(rlist=='()'):
        rlist=""
    print(rlist)
    print(num_of_symptoms)

    conn=getconn()
    cur = conn.cursor()
  
    cur.execute("SELECT DISTINCT Diseases.name FROM Diseases JOIN Has_symptoms ON Diseases.id = Has_symptoms.Disease_id JOIN Types_of_symptoms ON Has_symptoms.symptom_id = Types_of_symptoms.id WHERE Types_of_symptoms.name IN" +rlist+"GROUP BY Diseases.id, Diseases.name HAVING COUNT(DISTINCT Types_of_symptoms.name) ="+str(num_of_symptoms)+";"
 )
 
    results = cur.fetchall()
    if(len(results)==0):
        return render_template('notfound.html')
    temp=[]
    for i in range(0,len(results)):
        temp.append(results[i][0])
    cur.close()
    conn.close() 

    # # print('this is my query and it is succesfully retrieved',request1)

    return render_template('query_25_render.html',length=len(temp),result=temp)



@app.route('/query_24', methods=['POST'])
def get_24_input():
    
    requests=[]
    requests.append(request.form.get('input1'))
    requests.append(request.form.get('input2'))
    requests.append(request.form.get('input3'))
    requests.append(request.form.get('input4'))
    requests.append(request.form.get('input5'))
    requests.append(request.form.get('input6'))

    rlist='('

    for i in range(0,6):
     if(requests[i]!='none' and requests[i]!=None): 
       rlist+="'"
       rlist+=requests[i]
       rlist+="'"
       rlist+=','
        
    rlist=rlist[:-1]
    rlist+=')'
    if(rlist=='()'):
        rlist=""
    print(rlist)

    conn=getconn()
    cur = conn.cursor()
  
    cur.execute("SELECT DISTINCT Diseases.name FROM Diseases WHERE Diseases.id IN ( SELECT Has_symptoms.Disease_id FROM Has_symptoms WHERE Has_symptoms.symptom_id IN (SELECT Types_of_symptoms.id FROM Types_of_symptoms WHERE Types_of_symptoms.name in "+rlist+"));"
 )
 
    results = cur.fetchall()
    if(len(results)==0):
        return render_template('notfound.html')
    temp=[]
    for i in range(0,len(results)):
        temp.append(results[i][0])
    cur.close()
    conn.close() 

    # # print('this is my query and it is succesfully retrieved',request1)

    return render_template('query_24_render.html',length=len(temp),result=temp)
    

@app.route('/mpg3',methods=['POST'])
def q_18():
      
      r1=request.form.get('search2')
      r2=request.form.get('search3')
      conn=getconn()
      cur = conn.cursor()
      cur.execute("SELECT Has_Medicine.Dosage FROM Has_Medicine WHERE Has_Medicine.Medicine_id=(SELECT Medicine.id FROM Medicine WHERE Medicine.name="+"'"+r1+"'"+" limit 1) AND Has_Medicine.Disease_id=(SELECT Diseases.id FROM Diseases WHERE Diseases.name="+"'"+r2+"'"+" limit 1);"
      )
      results = cur.fetchall()
      if(len(results)==0):
          return render_template('notfound.html')
      temp=[]
      temp=list(results[0])
    #   temp.append(request2)
      cur.close()
      conn.close()          
      return   render_template('query_18.html',result=temp,med=r1,dis=r2)




@app.route('/insert',methods=['POST'])
def insert_data():
    requests=[]
    string='in'
    for i in range(1,19):
        temp="'"+str(request.form.get(string+str(i)))+"'"
        requests.append(temp)
    max_ranges=[]
    conn=getconn()
    cur = conn.cursor() 
    cur.execute("select id from Diseases order by id desc limit 1;")
    res=cur.fetchall()
    max_ranges.append(int(res[0][0])+1)
    cur.execute("select id from Medicine order by id desc limit 1;")
    res=cur.fetchall()
    max_ranges.append(int(res[0][0])+1)
    cur.execute("select id from Vaccines order by id desc limit 1;")
    res=cur.fetchall()
    max_ranges.append(int(res[0][0])+1)
    cur.execute("select id from types_of_tests order by id desc limit 1;")
    res=cur.fetchall()
    max_ranges.append(int(res[0][0])+1)
    cur.execute("select id from transmission_modes order by id desc limit 1;")
    res=cur.fetchall()
    max_ranges.append(int(res[0][0])+1)
    cur.execute("select id from types_of_symptoms order by id desc limit 1;")
    res=cur.fetchall()
    max_ranges.append(int(res[0][0])+1)
    cur.execute("select prevention_id from Prevention order by prevention_id desc limit 1;")
    res=cur.fetchall()
    max_ranges.append(int(res[0][0])+1)
    cur.execute("select id from treatment order by id desc limit 1;")
    res=cur.fetchall()
    max_ranges.append(int(res[0][0])+1)
    print("INSERT INTO Diseases VALUES("+str(max_ranges[0])+","+requests[0]+","+requests[1]+","+requests[2]+","+requests[3]+");")
    cur.execute("INSERT INTO Diseases VALUES("+str(max_ranges[0])+","+requests[0]+","+requests[1]+","+requests[2]+","+requests[3]+");")
    cur.execute("INSERT INTO treatment VALUES("+str(max_ranges[7])+","+requests[4]+","+requests[5]+","+requests[6]+");")
    cur.execute("INSERT INTO prevention VALUES("+str(max_ranges[0])+","+str(max_ranges[6])+","+requests[7]+");")
    cur.execute("INSERT INTO Medicine VALUES("+str(max_ranges[1])+","+requests[8]+","+requests[9]+","+requests[10]+");")
    cur.execute("INSERT INTO types_of_tests VALUES("+str(max_ranges[3])+","+requests[11]+","+requests[12]+");")
    cur.execute("INSERT INTO types_of_symptoms VALUES("+str(max_ranges[5])+","+requests[13]+");")
    cur.execute("INSERT INTO Vaccines VALUES("+str(max_ranges[2])+","+requests[14]+");")
    cur.execute("INSERT INTO transmission_modes  VALUES("+str(max_ranges[4])+","+requests[15]+","+requests[16]+");")
    cur.execute("INSERT INTO has_medicine VALUES("+str(max_ranges[0])+","+str(max_ranges[1])+","+requests[17]+");")
    cur.execute("INSERT INTO has_treatment VALUES("+str(max_ranges[0])+","+str(max_ranges[7])+");")
    cur.execute("INSERT INTO has_vaccine VALUES("+str(max_ranges[0])+","+str(max_ranges[2])+");")
    cur.execute("INSERT INTO has_symptoms VALUES("+str(max_ranges[0])+","+str(max_ranges[5])+");")
    cur.execute("INSERT INTO modes_of_transmission VALUES("+str(max_ranges[0])+","+str(max_ranges[4])+");")
    cur.execute("INSERT INTO identification_test VALUES("+str(max_ranges[0])+","+str(max_ranges[3])+");")
    conn.commit()
    cur.close()
    conn.close() 

    for i in range(0,18):
        print(requests[i])

    return render_template('thankyou.html')    



@app.route('/mpg2', methods=['POST'])
def req2():
    request2=request.form.get('search2')
    f=open('req.txt','r')
    gr=f.readline()
    f.close()

    if(gr=='1'):
        conn=getconn()
        cur = conn.cursor()
        cur.execute('''SELECT  DISTINCT ON (Diseases.name) Diseases.name ,Diseases.born_country,Diseases.born_year,Diseases.mortality_rate
        FROM Diseases 
        WHERE Diseases.name='''+"'"+request2+"'"+";")
        results = cur.fetchall()
        if(len(results)==0):
          return render_template('notfound.html')
        cur.close()
        conn.close()        
        return render_template('query_1.html',result=list(results[0]))

    if(gr=='2'):
      conn=getconn()
      cur = conn.cursor()
      cur.execute('''SELECT DISTINCT Diseases.name 
      FROM Diseases 
      WHERE name LIKE '''+"'"+request2[0]+"%'"+"order by Diseases.name asc;")
      results = cur.fetchall()
      if(len(results)==0):
          return render_template('notfound.html')
      temp=[]
      temp.append(request2[0])
      temp.append(len(results))
      for i in range(0,len(results)):
         temp.append(results[i][0])
      cur.close()
      conn.close()                   
      return  render_template('query_2.html',result=temp)
       
    if(gr=='3'):
        conn=getconn()
        cur = conn.cursor()
        cur.execute('''SELECT Treatment.name,Treatment.type ,Treatment.description
        FROM Treatment
        WHERE Treatment.id IN (
        SELECT Has_Treatment.Treatment_id 
        FROM Has_Treatment 
        WHERE Has_Treatment.Disease_id IN (
        SELECT Diseases.id 
        FROM Diseases 
        WHERE Diseases.name='''+"'"+request2+"'"+"));")
        results = cur.fetchall()
        if(len(results)==0):
          return render_template('notfound.html')
        temp=list(results[0])
        temp.append(request2)
        cur.close()
        conn.close()                   
        return  render_template('query_3.html',result=temp)
    
    if(gr=='4'):
        conn=getconn()
        cur = conn.cursor()
        cur.execute('''SELECT Prevention.description 
        FROM Prevention
        WHERE Prevention.Disease_id IN (
        SELECT Diseases.id 
        FROM Diseases
        WHERE Diseases.name='''+"'"+request2+"'"+");")
        results = cur.fetchall()
        if(len(results)==0):
          return render_template('notfound.html')
        temp=list(results[0])
        temp.append(request2)
        cur.close()
        conn.close()                   
        return  render_template('query_4.html',result=temp)

    if(gr=='5'):
      conn=getconn()
      cur = conn.cursor()
      cur.execute('''SELECT Medicine.name,Medicine.prescription ,Medicine.side_effects
      FROM Medicine 
      WHERE Medicine.id IN (
      SELECT Has_Medicine.Medicine_id 
      FROM Has_Medicine 
      WHERE Has_Medicine.Disease_id IN (
      SELECT Diseases.id 
      FROM Diseases 
      WHERE Diseases.name='''+"'"+request2+"'"+"));")
      results = cur.fetchall()
      if(len(results)==0):
          return render_template('notfound.html')
      temp=list(results[0])
      temp.append(request2)
      cur.close()
      conn.close()      
      return render_template('query_5.html',result=temp)
    
    if(gr=='6'):
      conn=getconn()
      cur = conn.cursor()
      cur.execute('''SELECT Types_of_tests.name,Types_of_tests.description
      FROM Types_of_tests
      WHERE Types_of_tests.id IN (
      SELECT Identification_test.test_id 
      FROM Identification_test 
      WHERE Identification_test.Disease_id IN (
      SELECT Diseases.id 
      FROM Diseases 
      WHERE Diseases.name='''+"'"+request2+"'"+"));")

      results = cur.fetchall()
      if(len(results)==0):
          return render_template('notfound.html')
      temp=list(results[0])
      temp.append(request2)
      cur.close()
      conn.close()          
      return  render_template('query_6.html',result=temp)
    
    if(gr=='7'):
      conn=getconn()
      cur = conn.cursor()
      cur.execute('''SELECT Types_of_symptoms.name
      FROM Types_of_symptoms
      WHERE Types_of_symptoms.id IN (
      SELECT Has_symptoms.symptom_id 
      FROM Has_symptoms 
      WHERE Has_symptoms.Disease_id IN (
      SELECT Diseases.id 
      FROM Diseases 
      WHERE Diseases.name='''+"'"+request2+"'"+"));")
      results = cur.fetchall()
      if(len(results)==0):
          return render_template('notfound.html')
      temp=[]
      temp.append(request2)
      temp.append(len(results))
      for i in range(0,len(results)):
         temp.append(results[i][0])
      cur.close()
      conn.close()          
      return  render_template('query_7.html',result=temp)
       
    
    if(gr=='8'):
      conn=getconn()
      cur = conn.cursor()
      cur.execute('''SELECT Vaccines.name
      FROM Vaccines
      WHERE Vaccines.id IN (
      SELECT Has_Vaccine.Vaccine_id 
      FROM Has_Vaccine 
      WHERE Has_Vaccine.Disease_id IN (
      SELECT Diseases.id 
      FROM Diseases 
      WHERE Diseases.name='''+"'"+request2+"'"+"));")
      results = cur.fetchall()
      if(len(results)==0):
          return render_template('notfound.html')
      temp=[]
      temp.append(request2)
      temp.append(len(results))

      print(results)
      for i in range(0,len(results)):
         temp.append(results[i][0])
      print(temp)
      cur.close()
      conn.close()          
      return  render_template('query_8.html',result=temp,length=len(temp))

    
    if(gr=='9'):
      conn=getconn()
      cur = conn.cursor()
      cur.execute('''SELECT Transmission_modes.name ,Transmission_modes.description
      FROM Transmission_modes
      WHERE Transmission_modes.id IN (
      SELECT Modes_of_Transmission.Transmission_id
      FROM Modes_of_Transmission 
      WHERE Modes_of_Transmission.Disease_id IN (
      SELECT Diseases.id 
      FROM Diseases 
      WHERE Diseases.name='''+"'"+request2+"'"+"));")
      results = cur.fetchall()
      if(len(results)==0):
          return render_template('notfound.html')
      temp=[]
      temp=list(results[0])
      temp.append(request2)

      cur.close()
      conn.close()          
      return  render_template('query_9.html',result=temp)

    
    if(gr=='10'):
      conn=getconn()
      cur = conn.cursor()
      cur.execute('''SELECT DISTINCT Treatment.name 
      FROM Treatment 
      WHERE name LIKE '''+"'"+request2[0]+"%'"+" order by Treatment.name asc;")
      results = cur.fetchall()
      if(len(results)==0):
          return render_template('notfound.html')
      temp=[]
      temp.append(request2[0])
      temp.append(len(results))
      for i in range(0,len(results)):
         temp.append(results[i][0])
      cur.close()
      conn.close()                   
      return  render_template('query_10.html',result=temp)
      
    
    if(gr=='11'):
      conn=getconn()
      cur = conn.cursor()
      cur.execute('''SELECT DISTINCT Transmission_modes.name 
FROM Transmission_modes 
WHERE name LIKE '''+"'"+request2[0]+"%'"+" order by Transmission_modes.name asc;")
      results = cur.fetchall()
      if(len(results)==0):
          return render_template('notfound.html')
      temp=[]
      temp.append(request2[0])
      temp.append(len(results))
      for i in range(0,len(results)):
         temp.append(results[i][0])
      cur.close()
      conn.close()                   
      return  render_template('query_11.html',result=temp)
    
    if(gr=='12'):
      conn=getconn()
      cur = conn.cursor()
      cur.execute('''SELECT DISTINCT Medicine.name 
FROM Medicine 
WHERE name LIKE '''+"'"+request2[0]+"%'"+" order by Medicine.name asc;")
      results = cur.fetchall()
      if(len(results)==0):
          return render_template('notfound.html')
      temp=[]
      temp.append(request2[0])
      temp.append(len(results))
      for i in range(0,len(results)):
         temp.append(results[i][0])
      cur.close()
      conn.close()                   
      return  render_template('query_12.html',result=temp)
    
    if(gr=='13'):
      conn=getconn()
      cur = conn.cursor()
      cur.execute('''SELECT DISTINCT Vaccines.name 
FROM Vaccines 
WHERE name LIKE '''+"'"+request2[0]+"%'"+" order by Vaccines.name asc;")
      results = cur.fetchall()
      if(len(results)==0):
          return render_template('notfound.html')
      temp=[]
      temp.append(request2[0])
      temp.append(len(results))
      for i in range(0,len(results)):
         temp.append(results[i][0])
      cur.close()
      conn.close()                   
      return  render_template('query_13.html',result=temp)
    
    if(gr=='14'):
      conn=getconn()
      cur = conn.cursor()
      cur.execute('''SELECT DISTINCT Types_of_tests.name 
FROM Types_of_tests 
WHERE name LIKE '''+"'"+request2[0]+"%'"+" order by Types_of_tests.name  asc;")
      results = cur.fetchall()
      if(len(results)==0):
          return render_template('notfound.html')
      temp=[]
      temp.append(request2[0])
      temp.append(len(results))
      for i in range(0,len(results)):
         temp.append(results[i][0])
      cur.close()
      conn.close()                   
      return  render_template('query_14.html',result=temp)
    
    if(gr=='15'):
      conn=getconn()
      cur = conn.cursor()
      cur.execute('''SELECT DISTINCT Types_of_symptoms.name 
FROM Types_of_symptoms 
WHERE name LIKE '''+"'"+request2[0]+"%'"+" order by Types_of_symptoms.name asc;")
      results = cur.fetchall()
      if(len(results)==0):
          return render_template('notfound.html')
      temp=[]
      temp.append(request2[0])
      temp.append(len(results))
      for i in range(0,len(results)):
         temp.append(results[i][0])
      cur.close()
      conn.close()                   
      return  render_template('query_15.html',result=temp)
    
    if(gr=='16'):
      conn=getconn()
      cur = conn.cursor()
      cur.execute('''SELECT Treatment.name,Treatment.type ,Treatment.description
FROM Treatment
WHERE Treatment.name='''+"'"+request2+"'"+";")
      results = cur.fetchall()
      if(len(results)==0):
          return render_template('notfound.html')
      temp=[]
      temp=list(results[0])
      temp.append(request2)

      cur.close()
      conn.close()          
      return  render_template('query_16.html',result=temp)
    
    
    if(gr=='17'):
      conn=getconn()
      cur = conn.cursor()
      cur.execute('''SELECT Types_of_tests.name,Types_of_tests.description
FROM Types_of_tests
WHERE Types_of_tests.name='''+"'"+request2+"'"+";")
      results = cur.fetchall()
      if(len(results)==0):
          return render_template('notfound.html')
      temp=[]
      temp=list(results[0])
      temp.append(request2)

      cur.close()
      conn.close()          
      return  render_template('query_17.html',result=temp)
   
  # pending::::::: 
    # if(gr=='18'):
    #   conn=getconn()
    #   cur = conn.cursor()
    #   cur.execute('''SELECT Has_Medicine.Dosage
    #   FROM Has_Medicine
    #   WHERE Has_Medicine.Medicine_id=(
    #   SELECT Medicine.id 
    #   FROM Medicine
    #   WHERE Medicine.name='medicine_name'
    #   )
    #   AND Has_Medicine.Disease_id=(
    #   SELECT Diseases.id
    #   FROM Diseases
    #   WHERE Diseases.name='disease_name'
    #   );''')
    #   results = cur.fetchall()
    #   if(len(results)==0):
    #       return render_template('notfound.html')
    #   temp=[]
    #   temp=list(results[0])
    #   temp.append(request2)
    #   cur.close()
    #   conn.close()          
    #   return   render_template('query_18.html')
    
    #DONE
    if(gr=='19'):
      conn=getconn()
      cur = conn.cursor()
      cur.execute('''
      SELECT DISTINCT Diseases.name
      FROM Diseases
      WHERE Diseases.id IN(
      SELECT Has_Medicine.Disease_id
      FROM Has_Medicine
      WHERE Has_Medicine.Medicine_id IN(
      SELECT Medicine.id
      FROM Medicine
      WHERE Medicine.name='''+"'"+request2+"'"+"));")
      results = cur.fetchall()
      if(len(results)==0):
          return render_template('notfound.html')
      temp=[]
      temp.append(request2)
      temp.append(len(results))
      for i in range(0,len(results)):
         temp.append(results[i][0])

      cur.close()
      conn.close()          
      return render_template('query_19.html',result=temp)
    
    
    #DONE
    if(gr=='20'):
      conn=getconn()
      cur = conn.cursor()
      cur.execute('''SELECT DISTINCT Diseases.name
      FROM Diseases
      WHERE Diseases.id IN(
      SELECT Has_Treatment.Disease_id
      FROM Has_Treatment
      WHERE Has_Treatment.Treatment_id IN(
      SELECT Treatment.id
      FROM Treatment
      WHERE Treatment.name='''+"'"+request2+"'"+"));")
      results = cur.fetchall()
      if(len(results)==0):
          return render_template('notfound.html')
      temp=[]
      temp.append(request2)
      temp.append(len(results))
      for i in range(0,len(results)):
         temp.append(results[i][0])
      cur.close()
      conn.close()          
      return  render_template('query_20.html',result=temp)
    
    
    # DONE
    if(gr=='21'):
      conn=getconn()
      cur = conn.cursor()
      cur.execute('''SELECT DISTINCT Diseases.name
        FROM Diseases
        WHERE Diseases.id IN(
        SELECT Modes_of_Transmission.Disease_id
        FROM Modes_of_Transmission
        WHERE Modes_of_Transmission.Transmission_id IN(
        SELECT Transmission_modes.id
        FROM Transmission_modes
        WHERE Transmission_modes.name='''+"'"+request2+"'"+"));")
      results = cur.fetchall()
      if(len(results)==0):
          return render_template('notfound.html')
      temp=[]
      temp.append(request2)
      temp.append(len(results))
      for i in range(0,len(results)):
         temp.append(results[i][0])
      cur.close()
      conn.close()          
      return  render_template('query_21.html',result=temp)
    
    #DONE
    if(gr=='22'):
      conn=getconn()
      cur = conn.cursor()
      cur.execute('''SELECT DISTINCT Diseases.name
          FROM Diseases
          WHERE Diseases.id IN(
        SELECT Has_Vaccine.Disease_id
        FROM Has_Vaccine
        WHERE Has_Vaccine.Vaccine_id IN(
        SELECT Vaccines.id
        FROM Vaccines
        WHERE Vaccines.name='''+"'"+request2+"'"+"));")
      results = cur.fetchall()
      if(len(results)==0):
          return render_template('notfound.html')
      temp=[]
      temp.append(request2)
      temp.append(len(results))
      for i in range(0,len(results)):
         temp.append(results[i][0])
      cur.close()
      conn.close()          
      return render_template('query_22.html',result=temp)
    
    
    #DONE
    if(gr=='23'):
      conn=getconn()
      cur = conn.cursor()
      cur.execute('''SELECT DISTINCT Diseases.name
      FROM Diseases
      WHERE Diseases.id IN(
      SELECT Identification_test.Disease_id
      FROM Identification_test
      WHERE Identification_test.test_id IN(
      SELECT Types_of_tests.id
      FROM Types_of_tests
      WHERE Types_of_tests.name='''+"'"+request2+"'"+"));"
      )
      results = cur.fetchall()
      if(len(results)==0):
          return render_template('notfound.html')
      temp=[]
      temp.append(request2)
      temp.append(len(results))
      for i in range(0,len(results)):
         temp.append(results[i][0])
      cur.close()
      conn.close()          
      return  render_template('query_23.html',result=temp)
    
    
    
    # #PENDING
    # if(gr=='24'):
    #   conn=getconn()
    #   cur = conn.cursor()
    #   cur.execute('SELECT DISTINCT Types_of_symptoms.name FROM Types_of_symptoms')
    #   results = cur.fetchall()
    #   temp=[]
    #   for i in range(0,len(results)):
    #      temp.append(results[i][0])

    #   # if(len(results)==0):
    #   #     return render_template('notfound.html')
    #   # temp=[]
    #   # temp=list(results[0])
    #   # temp.append(request2)
    #   # cur.close()
    #   # conn.close()          
    #   return render_template('query_24.html',length=len(temp),result=temp)
    
    
    # #PENDING
    # if(gr=='25'):
    #   conn=getconn()
    #   cur = conn.cursor()
    #   cur.execute('SELECT DISTINCT Types_of_symptoms.name FROM Types_of_symptoms')
    #   results = cur.fetchall()
    #   temp=[]
    #   for i in range(0,len(results)):
    #      temp.append(results[i][0])

    #   # if(len(results)==0):
    #   #     return render_template('notfound.html')
    #   # temp=[]
    #   # temp=list(results[0])
    #   # temp.append(request2)
    #   # cur.close()
    #   # conn.close()          
    #   return render_template('query_25.html',length=len(temp),result=temp)
    
    
    #PENDING
    if(gr=='26'):
      conn=getconn()
      cur = conn.cursor()
      cur.execute('''SELECT Transmission_modes.name ,Transmission_modes.description
      FROM Transmission_modes
      WHERE Transmission_modes.id IN (
      SELECT Modes_of_Transmission.Transmission_id
      FROM Modes_of_Transmission 
      WHERE Modes_of_Transmission.Disease_id IN (
      SELECT Diseases.id 
      FROM Diseases 
      WHERE Diseases.name='''+"'"+request2+"'"+"));")
      results = cur.fetchall()
      if(len(results)==0):
          return render_template('notfound.html')
      temp=[]
      temp=list(results[0])
      temp.append(request2)
      cur.close()
      conn.close()          
      return render_template('query_26.html')
    
    
    #Pending
    if(gr=='27'):
      conn=getconn()
      cur = conn.cursor()
      cur.execute('''SELECT Transmission_modes.name ,Transmission_modes.description
      FROM Transmission_modes
      WHERE Transmission_modes.id IN (
      SELECT Modes_of_Transmission.Transmission_id
      FROM Modes_of_Transmission 
      WHERE Modes_of_Transmission.Disease_id IN (
      SELECT Diseases.id 
      FROM Diseases 
      WHERE Diseases.name='''+"'"+request2+"'"+"));")
      results = cur.fetchall()
      if(len(results)==0):
          return render_template('notfound.html')
      temp=[]
      temp=list(results[0])
      temp.append(request2)
      cur.close()
      conn.close()          
      return   render_template('query_27.html')
    
    
    
    #DONE
    if(gr=='28'):
      conn=getconn()
      cur = conn.cursor()
      cur.execute('''
      SELECT DISTINCT ON (Diseases.name) Diseases.name,Diseases.born_country,Diseases.born_year,Diseases.mortality_rate,Types_of_symptoms.name as symptoms_name,Medicine.name as medicine_name,Medicine.prescription as medicine_prescription,Medicine.side_effects as medicine_side_effects,Has_Medicine.Dosage as medicine_dosage,Treatment.name as treatment_name,Treatment.type as treatment_type,Treatment.description as treatment_description,Vaccines.name as Vaccine_name,Types_of_tests.name as test_name,Types_of_tests.description as test_description,Transmission_modes.name as modes_name,Transmission_modes.description as modes_description ,Prevention.description as Prevention
      FROM Diseases
      JOIN Has_symptoms ON Diseases.id = Has_symptoms.Disease_id
      JOIN Types_of_symptoms ON Has_symptoms.symptom_id = Types_of_symptoms.id
      JOIN Has_Medicine ON Diseases.id=Has_Medicine.Disease_id
      JOIN Medicine ON Has_Medicine.Medicine_id=Medicine.id
      JOIN Has_Treatment ON Diseases.id=Has_Treatment.Disease_id
      JOIN Treatment ON Has_Treatment.Treatment_id=Treatment.id
      JOIN Has_Vaccine ON Diseases.id=Has_Vaccine.Disease_id
      JOIN Vaccines ON Has_Vaccine.Vaccine_id=Vaccines.id
      JOIN Identification_test ON Diseases.id=Identification_test.Disease_id
      JOIN Types_of_tests ON Identification_test.test_id=Types_of_tests.id
      JOIN Modes_of_Transmission ON Diseases.id=Modes_of_Transmission.Disease_id
      JOIN Transmission_modes ON Modes_of_Transmission.Transmission_id=Transmission_modes.id
      JOIN Prevention ON Diseases.id=Prevention.Disease_id
      WHERE Diseases.name='''+"'"+request2+"'"+";")
      
      results = cur.fetchall()
      if(len(results)==0):
          return render_template('notfound.html')
      temp=[]
      temp=list(results[0])
      if(temp[0]=='covid-19'):
                       temp[8]='covishield'
                       temp[9]='covaccine'
      temp.append(request2)
      cur.close()
      conn.close()          
      return   render_template('query_28.html',result=temp)

    return render_template('mainpage1.html')



# # #   here i will use the database code to make my website interactive:
# #     conn = psycopg2.connect(
# #     host="10.17.50.87",
# #     database="group_4",
# #     user="group_4",
# #     password="1234")

# #     # Create a cursor object
# #     cur = conn.cursor()

#     # Execute a SQL query
#         # query 28
# #     cur.execute('''
# # SELECT DISTINCT ON (Diseases.name) Diseases.name,Diseases.born_country,Diseases.born_year,Diseases.mortality_rate,Types_of_symptoms.name as symptoms_name,Medicine.name as medicine_name,Medicine.prescription as medicine_prescription,Medicine.side_effects as medicine_side_effects,Has_Medicine.Dosage as medicine_dosage,Treatment.name as treatment_name,Treatment.type as treatment_type,Treatment.description as treatment_description,Vaccines.name as Vaccine_name,Types_of_tests.name as test_name,Types_of_tests.description as test_description,Transmission_modes.name as modes_name,Transmission_modes.description as modes_description ,Prevention.description as Prevention
# # FROM Diseases
# # JOIN Has_symptoms ON Diseases.id = Has_symptoms.Disease_id
# # JOIN Types_of_symptoms ON Has_symptoms.symptom_id = Types_of_symptoms.id
# # JOIN Has_Medicine ON Diseases.id=Has_Medicine.Disease_id
# # JOIN Medicine ON Has_Medicine.Medicine_id=Medicine.id
# # JOIN Has_Treatment ON Diseases.id=Has_Treatment.Disease_id
# # JOIN Treatment ON Has_Treatment.Treatment_id=Treatment.id
# # JOIN Has_Vaccine ON Diseases.id=Has_Vaccine.Disease_id
# # JOIN Vaccines ON Has_Vaccine.Vaccine_id=Vaccines.id
# # JOIN Identification_test ON Diseases.id=Identification_test.Disease_id
# # JOIN Types_of_tests ON Identification_test.test_id=Types_of_tests.id
# # JOIN Modes_of_Transmission ON Diseases.id=Modes_of_Transmission.Disease_id
# # JOIN Transmission_modes ON Modes_of_Transmission.Transmission_id=Transmission_modes.id
# # JOIN Prevention ON Diseases.id=Prevention.Disease_id
# # WHERE Diseases.name='''+"'"+query+"'"+";")

# # query 23

# #     cur.execute('''SELECT DISTINCT Diseases.name
# # FROM Diseases
# # WHERE Diseases.id IN(
# #     SELECT Identification_test.Disease_id
# #     FROM Identification_test
# #     WHERE Identification_test.test_id IN(
# #         SELECT Types_of_tests.id
# #         FROM Types_of_tests
# #         WHERE Types_of_tests.name='''+"'"+query+"'"+"));"
# #         )


# #query 20
#     cur.execute('''SELECT DISTINCT Diseases.name
# FROM Diseases
# WHERE Diseases.id IN(
#     SELECT Has_Treatment.Disease_id
#     FROM Has_Treatment
#     WHERE Has_Treatment.Treatment_id IN(
#         SELECT Treatment.id
#         FROM Treatment
#         WHERE Treatment.name='''+"'"+query+"'"+"));")

# #query 19
#     cur.execute('''
#     SELECT DISTINCT Diseases.name
# FROM Diseases
# WHERE Diseases.id IN(
#     SELECT Has_Medicine.Disease_id
#     FROM Has_Medicine
#     WHERE Has_Medicine.Medicine_id IN(
#         SELECT Medicine.id
#         FROM Medicine
#         WHERE Medicine.name='''+"'"+query+"'"+"));")



# #query 18
#     cur.execute('''SELECT Has_Medicine.Dosage
# FROM Has_Medicine
# WHERE Has_Medicine.Medicine_id=(
#     SELECT Medicine.id 
#     FROM Medicine
#     WHERE Medicine.name='medicine_name'
# )
# AND Has_Medicine.Disease_id=(
#     SELECT Diseases.id
#     FROM Diseases
#     WHERE Diseases.name='disease_name'
# );''')


# #query 9
#     cur.execute('''SELECT Transmission_modes.name ,Transmission_modes.description
# FROM Transmission_modes
# WHERE Transmission_modes.id IN (
#     SELECT Modes_of_Transmission.Transmission_id
#     FROM Modes_of_Transmission 
#     WHERE Modes_of_Transmission.Disease_id IN (
#         SELECT Diseases.id 
#         FROM Diseases 
#         WHERE Diseases.name='''+"'"+query+"'"+"));")

# #query 8
#     cur.execute('''SELECT Vaccines.name
# FROM Vaccines
# WHERE Vaccines.id IN (
#     SELECT Has_Vaccine.Vaccine_id 
#     FROM Has_Vaccine 
#     WHERE Has_Vaccine.Disease_id IN (
#         SELECT Diseases.id 
#         FROM Diseases 
#         WHERE Diseases.name='''+"'"+query+"'"+"));")
# #query 7
#     cur.execute('''SELECT Types_of_symptoms.name
# FROM Types_of_symptoms
# WHERE Types_of_symptoms.id IN (
#     SELECT Has_symptoms.symptom_id 
#     FROM Has_symptoms 
#     WHERE Has_symptoms.Disease_id IN (
#         SELECT Diseases.id 
#         FROM Diseases 
#         WHERE Diseases.name='''+"'"+query+"'"+"));")
# #query 6
#     cur.execute('''SELECT Types_of_tests.name,Types_of_tests.description
# FROM Types_of_tests
# WHERE Types_of_tests.id IN (
#     SELECT Identification_test.test_id 
#     FROM Identification_test 
#     WHERE Identification_test.Disease_id IN (
#         SELECT Diseases.id 
#         FROM Diseases 
#         WHERE Diseases.name='''+"'"+query+"'"+"));")

# #query 5
#     cur.execute('''SELECT Medicine.name,Medicine.prescription ,Medicine.side_effects
# FROM Medicine
# WHERE Medicine.id IN (
#     SELECT Has_Medicine.Medicine_id 
#     FROM Has_Medicine 
#     WHERE Has_Medicine.Disease_id IN (
#         SELECT Diseases.id 
#         FROM Diseases 
#         WHERE Diseases.name='''+"'"+query+"'"+"));")

# #query 4
#     cur.execute('''SELECT Prevention.description 
# FROM Prevention
# WHERE Prevention.Disease_id IN (
#     SELECT Diseases.id 
#     FROM Diseases
#     WHERE Diseases.name='''+"'"+query+"'"+");")

# #query 3
#     cur.execute('''SELECT Treatment.name,Treatment.type ,Treatment.description
# FROM Treatment
# WHERE Treatment.id IN (
#     SELECT Has_Treatment.Treatment_id 
#     FROM Has_Treatment 
#     WHERE Has_Treatment.Disease_id IN (
#         SELECT Diseases.id 
#         FROM Diseases 
#         WHERE Diseases.name='''+"'"+query+"'"+"));")
# #query 1
#     cur.execute('''SELECT  DISTINCT ON (Diseases.name) Diseases.name ,Diseases.born_country,Diseases.born_year,Diseases.mortality_rate
# FROM Diseases
# WHERE Diseases.name='''+"'"+query+"'"+";")
    
    # Fetch the results
    # results = cur.fetchall()
    # re2=results[3]
    # print(type(results))

# Close the cursor and connection
    
    

    # Perform search operation here and return results
    # a=render_template('query_20.html',result=re2)
    # print(results)
    # return render_template("mpg2.html")

if __name__ == '__main__':
    app.run(debug=True)
