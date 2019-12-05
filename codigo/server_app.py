import socket
import boto3
HOST = '127.0.0.1'
import pickle
import psycopg2
              # Endereco IP do Servidor
PORT = 5002          # Porta que o Servidor esta
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
orig = (HOST, PORT)
tcp.bind(orig)
tcp.listen(1)
reko_client = boto3.client('rekognition','us-east-1')
rds_client = boto3.client('rds','sa-east-1')
rds = rds_client.describe_db_instances()

port = rds['DBInstances'][0]['Endpoint']['Port']
adress = rds['DBInstances'][0]['Endpoint']['Address']
Username = rds['DBInstances'][0]['MasterUsername']
DBName = rds['DBInstances'][0]['DBName']
print(DBName, Username, adress,port)
postgre = psycopg2.connect(dbname=DBName, user=Username,password=Username,host=adress,port=port)
cur = postgre.cursor()
#cur.execute("CREATE TABLE PEAPLE (USERNAME VARCHAR(50) PRIMARY KEY, PASSWORD VARCHAR(50));");
#cur.execute("CREATE TABLE INFO (USERNAME VARCHAR(50), IDINFO SERIAL, SENTIMENTO VARCHAR(40), SMILE BOOL, PRIMARY KEY(USERNAME,IDINFO), FOREIGN KEY(USERNAME) REFERENCES PEAPLE(USERNAME));")
#postgre.commit()


print("Conected in database")
s3_bucket = 'ufcquixada'

while True:
    con, cliente = tcp.accept()
    print ('Concetado por', cliente)
    
    while True:
        msg = con.recv(4096)
        if not msg:
            
            break
        #print(msg)
        instruction = msg.decode()
        command , parameter, extra = instruction.split('-')
        
        #Analisar Imagem
        if(command == '1'):
            file_name = parameter
            img = {
                    'S3Object':{
                    'Bucket': s3_bucket, 'Name': file_name
                    }
                }
            response = reko_client.detect_faces(Image=img, Attributes=['ALL'])
            print(len(response['FaceDetails']) )
            if(len(response['FaceDetails']) == 1):
                username=extra
                sex = response['FaceDetails'][0]['Gender']['Value']
                confidenceSex = response['FaceDetails'][0]['Gender']['Confidence']
                #print(self.response)
            
                AgeL = response['FaceDetails'][0]['AgeRange']['Low']
                AgeH = response['FaceDetails'][0]['AgeRange']['High']
                
                print(response)
                best_sentimento = 0
                indice = 0
                name_sentimento = ''                
                for i in range(len(response['FaceDetails'][0]['Emotions'])):
                    if(response['FaceDetails'][0]['Emotions'][i]['Confidence'] > best_sentimento):
                        indice = i
                        best_sentimento = response['FaceDetails'][0]['Emotions'][i]['Confidence']

                sentimento = response['FaceDetails'][0]['Emotions'][indice]['Type']
                
                confidenceSmile = response['FaceDetails'][0]['Smile']['Confidence']
                #eyeg = response['FaceDetails'][0]['Eyeglasses']['Value']
                eyegConf = response['FaceDetails'][0]['Eyeglasses']['Confidence']
                #mustache = response['FaceDetails'][0]['Mustache']['Mustache']
                mustacheConf = response['FaceDetails'][0]['Mustache']['Confidence']
                #eyeOpen = response['FaceDetails'][0]['EyesOpen']['Value']
                eyeOpenConf = response['FaceDetails'][0]['EyesOpen']['Confidence']
               
                
                sorrindo = ''
                if(response['FaceDetails'][0]['Smile']['Value']):
                    sorrindo = 'Yes'
                else:
                    sorrindo = 'No'
                
                eyeg = ''
                if(response['FaceDetails'][0]['Eyeglasses']['Value']):
                    eyeg = 'Yes'
                else:
                    eyeg = 'No'
                
                
                mustache = ''
                if(response['FaceDetails'][0]['Mustache']['Value']):
                    mustache = 'Yes'
                else:
                    mustache = 'No'
                    
                eyeOpen = ''
                if(response['FaceDetails'][0]['EyesOpen']['Value']):
                    eyeOpen = 'Yes'
                else:
                    eyeOpen = 'No'
                
                
                
                
                
                width = response['FaceDetails'][0]['BoundingBox']['Width']
                height = response['FaceDetails'][0]['BoundingBox']['Height']
                top = response['FaceDetails'][0]['BoundingBox']['Top']
                left = response['FaceDetails'][0]['BoundingBox']['Left']
                
                send_value = {'Eyeglasses':eyeg,'EyeglassesConf':eyegConf,'Mustache':mustache,'MustacheConf':mustacheConf,'EyeOpen':eyeOpen,'EyeOpenConf':eyeOpenConf,'Sex': sex,'ConfS':confidenceSex, 'AgeL': AgeL, 'AgeH': AgeH,'Sent':sentimento,'ConfSe':best_sentimento,'Smile':sorrindo,'ConfSmile':confidenceSmile,'Width':width,'Height':height,'Top':top,'Left':left}
                
                if(sorrindo == 'Yes'):    
                    cur.execute("INSERT INTO INFO VALUES(%s,DEFAULT,%s,TRUE)",(username,sentimento))
                else:
                    cur.execute("INSERT INTO INFO VALUES(%s,DEFAULT,%s,FALSE)",(username,sentimento))

                postgre.commit()
                
                con.send(pickle.dumps(send_value))
                
                
                
                
            else:
                con.send(pickle.dumps(''))
        
        #Login
        elif(command == '2'):
            username = parameter
            
        #print(msg)
            cur.execute("SELECT * FROM PEAPLE WHERE USERNAME = %s",(username,))
            result_user = cur.fetchall()
        
            #user not exist
            if(len(result_user) != 1):
                con.send('1'.encode())
            else:
                con.send('2'.encode())
                print(result_user[0][1])
                print("2")
                msg = con.recv(4096)
                if not msg:
            
                    break
                password = msg.decode()
                print(password)
                if(username == result_user[0][0] and password == result_user[0][1]):
                    print("3")
                    con.send('3'.encode())
                else:
                    print("4")
                    con.send('4'.encode())
                    
        
        elif(command == '3'):
            username = parameter
            
            
        #print(msg)
            cur.execute("SELECT * FROM PEAPLE WHERE USERNAME = %s",(username,))
            result_user = cur.fetchall()
        
            #user not exist
            if(len(result_user) != 0):
                con.send('1'.encode())
            else:
                con.send('2'.encode())
                print("2")
                msg = con.recv(4096)
                if not msg:
            
                    break
                password = msg.decode()
                print(password)
                cur.execute("INSERT INTO PEAPLE VALUES(%s,%s)",(username,password))
                postgre.commit()
                
                #if(username == result_user[0][0] and password == result_user[0][1]):
                 #   print("3")
                con.send('3'.encode())
                #else:
                 #   print("4")
                  #  con.send('4'.encode())
        
        elif(command == '4'):
            username = parameter
            cur.execute("SELECT * FROM INFO WHERE USERNAME = %s",(username,))
            result_info = cur.fetchall()
            if(len(result_info) != 0):
                print(result_info)
            print("send")
            con.send(pickle.dumps(result_info))


            
    con.close()
