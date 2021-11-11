import re
import pandas as pd
import os
from pyvis.network import Network

global choices
global save_data_path
global  path_main_folder
global  start_file_path
global start_file
choices = ['.html', '.jsp']



def read_text_file(file_path):
    with open(file_path,encoding="ISO-8859-1") as f:
        return (f.read())

def Enquiry(index):
    if len(index) == 0:
        return 0
    else:
        return 1

def callvalues(save_data_path, path_main_folder, start_file_path, start_file):
    save_data_path = (save_data_path)
    path_main_folder = (path_main_folder)
    start_file_path = (start_file_path)
    start_file = (start_file)

    return save_data_path, path_main_folder, start_file_path, start_file




def starting_page(start_file_path,start_file):
  
  #initialize starting file

  
  df_ls10 = [ ]#for storing first pages .jsp
  jsps = [ ]

  

  aya = read_text_file(start_file_path) #reading the files
  for  x in aya.split('\n'):
    match = re.search(r'[A-Za-z0-9.\_]+[.](?:jsp|html)', x) #regex
    if match:
      jsps.append(match.group()) # .jsp picked from the page is stored in jsps
      df_ls10.append({"file":start_file,"link":match.group()}) #file = initial file name
  #adding df_ls into a dataframe
  df_file_link=pd.DataFrame(df_ls10)
  df_file_link = df_file_link.drop_duplicates()
  return [jsps,df_file_link]




def Traversing(jsps,dataframe,path_main_folder):
  
  jsps_main = [ ]
  jsps_final = [ ]
  #jsps list is appended into jsps_main
  for  z in jsps:
    jsps_main.append(z)
  for i in jsps_main  :     
    if i.endswith(tuple(choices)):
        for root, dirs , files in os.walk(path_main_folder):
            for root, dirs , files in os.walk(path_main_folder):
                if i in files:
                  if i not in jsps_final:#checking if files are repeating or not                        
                    files_my = (os.path.join(root,i))
                    for line in open(files_my, encoding='windows-1252'):            
                      li=line.strip()
        
                      if line.startswith('/*'):
                        None
        
                      elif line.endswith('*/'):
                        None
        
                      elif line.startswith('//'):
                        continue
        
                      elif "/*" in line:
                        if line.index('/*')>0:
                          al = line.split('/*')
                          line = al[0]
                          aya2 = (line.rstrip())
                    
                      elif "*/" in line:
                        if line.index('*/')<(len(line)-1):
                          al = line.split('*/')
                          line = al[1]
                          aya2 = (line.rstrip())
                  
                      else:
                        aya2 = (line.rstrip()) 
                      jsps_final.append(i)  #once the files are read those are added into jsps_final
                        
                      for  y in aya2.split('\n'):
                        match2 = re.search(r'[A-Za-z0-9.\_]+[.](?:jsp|html)', y)
                        if match2:
                          jsps_main.append(match2.group())
                          if not dataframe['file'].str.contains(match2.group()).any():   #checking if the regex in not in to dataframe 
                            if not dataframe['link'].str.contains(match2.group()).any():
                              dataframe=dataframe.append({'file': i, 'link': match2.group()}, ignore_index=True)#if the regex (.jsp) not in the dataframe it is added into the column
        

  return dataframe
            
        
def all_files(path_main_folder):
  #dataframe of all files in the folder
  df_ls2 = [ ]
  for root, dirs , files in os.walk(path_main_folder):
    for file in files:
      if file.endswith(tuple(choices)):
          df_ls2.append({"Page":file})
      
  df_1=pd.DataFrame(df_ls2)
  files_in_folder = df_1.drop_duplicates()
  return files_in_folder       
      

def check_orphan(csv_path, df_file_link, files_in_folder, start_file):
  data = pd.read_csv(csv_path)
  col_names =  ['file' , "link"]
  df_3  = pd.DataFrame(columns = col_names )


  data_Link = (data['file']) # links col  in 1st csv 
  df_Page = (files_in_folder["Page"])     #page col in all files csv
  data_File = (data['link']) #files col in 1st csv

  for i in df_Page:
    index = (data.link[data.link == i ].index.tolist())
    if Enquiry(index):
      continue
    elif i == start_file:
      continue
    else:
        df_file_link = df_file_link.append({'file': i, 'link': "orphan"}, ignore_index=True)
        df_3 = df_3.append({'file': i,'link' : "orphan"}, ignore_index=True)
  
  return df_3,df_file_link


def pyvis_graph(csv_path,save_name_html):
  got_net = Network(height='750px', width='100%', bgcolor='	#F0FFF0	', font_color='black' ,notebook = True, directed=False,)
  # set the physics layout of the network
  got_net.hrepulsion()
  #create a directory with name of application, E:/
  got_data = pd.read_csv(csv_path)

  sources = got_data['file']
  targets = got_data['link']
  # weights = got_data['Weight']

  edge_data = zip(sources, targets,) #weights)

  for e in edge_data:
      src = e[0]
      dst = e[1]
      # w = e[2]

      if dst== "orphan":
        got_net.add_node(src, src, title=src , size = [150] ,color =  ' #FFBF00' ,group = 2 )
        got_net.add_node(dst, dst, title=dst , size = [120] , color ='	#FF7F7F',group = 2 )
        got_net.add_edge(src, dst, size = [100], color = '#add8e6')

      else:
        got_net.add_node(src, src, title=src , size = [150] ,color =  '#1C9B8E'  , group = 1,shadow = True)
        got_net.add_node(dst, dst, title=dst , size = [120] , color ='#87CEEB', group = 1,shadow = True)
        got_net.add_edge(src, dst, size = [100], color = '#7EC8E3')


      

  neighbor_map = got_net.get_adj_list()

  # add neighbor data to node hover data
  for node in got_net.nodes:
      node['title'] += ' Neighbors:<br>' + '<br>'.join(neighbor_map[node['id']])
      node['value'] = len(neighbor_map[node['id']])
  got_net.show_buttons(filter_=['physics'])
  got_net.show(save_name_html)






# =============================================================================
# CALLING FUNCTION
# =============================================================================

def final_call(save_data_path, path_main_folder, start_file_path, start_file):
    save_data_path, path_main_folder, start_file_path, start_file = callvalues(save_data_path, path_main_folder ,start_file_path,start_file)
    jsps,df_file_link = starting_page(start_file_path ,start_file) #start_file_path , start_file
    df_file_link = Traversing(jsps,df_file_link,path_main_folder) #jsps, dataframe, path_main_folder
    df_file_link.to_csv(save_data_path + '/files_link.csv')
    files_in_folder = all_files(path_main_folder)   #path_main_folder
    df_3,df_file_link = check_orphan(save_data_path + '/files_link.csv',df_file_link,files_in_folder,start_file) #csv_path, df_file_link, files_in_folder,start_file
    df_file_link.to_csv(save_data_path + '/files_link.csv') #path to save csv
    df_3.to_csv(save_data_path + '/orphan.csv') #path to save csv
    pyvis_graph(save_data_path + '/files_link.csv',save_data_path +"/files_link.html") #csv_path,save_name_html
    pyvis_graph(save_data_path + '/orphan.csv', save_data_path +"/orphan.html") #csv_path,save_name_html








