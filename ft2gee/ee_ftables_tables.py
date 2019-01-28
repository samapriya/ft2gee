import ee
import re
import pendulum
import os
from os import walk
os.chdir(os.path.dirname(os.path.realpath(__file__)))
path=os.path.dirname(os.path.realpath(__file__))
# Initialize the client
ee.Initialize()

#Export function
def exportnow(collection,filename,filepath):
  filename=re.sub('[^A-Za-z0-9]+', '', filename)
  coll=ee.FeatureCollection('ft:'+collection)
  try:
      task = ee.batch.Export.table.toAsset(
          collection = coll,
          description = filename,
          assetId = filepath)
      task.start()
      print('Exporting: '+str(collection)+' to '+str(filepath))
      print('')
  except Exception as e:
    pass

#Function to access ftables in scripts and export to tables in EE
ftable=[]
def fexp(local,geepath):
    if ee.data.getInfo(geepath):
        print('Folder already exists.')
    else:
        print('Creating Folder')
        ee.data.createAsset({'type': ee.data.ASSET_TYPE_FOLDER}, geepath)
    for dirpath,_,filenames in os.walk(local):
        for f in filenames:
            if not dirpath.endswith('.git'):
                fname=os.path.abspath(os.path.join(dirpath, f))
                with open(fname) as f:
                    for line in f:
                        if "ee.FeatureCollection('ft:" in line:
                            try:
                                id=(line.split('ft:')[1].split("'")[0])
                                name=(line.split('var')[1].split("=")[0])
                                name=str(re.sub('[^A-Za-z0-9]+', '', name))
                                filepath=geepath+'/'+str(re.sub('[^A-Za-z0-9]+', '', name))
                                combined=str(id)+'&'+str(name)+'&'+str(filepath)
                                ftable.append(combined)
                            except Exception as e:
                                pass
                                #
                        elif 'ee.FeatureCollection("ft:' in line:
                            try:
                                id=(line.split('ft:')[1].split('"')[0])
                                name=(line.split('var')[1].split('=')[0])
                                name=str(re.sub('[^A-Za-z0-9]+', '', name))
                                filepath=geepath+'/'+str(re.sub('[^A-Za-z0-9]+', '', name))
                                #print(str(id),name,filepath)
                                combined=str(id)+'&'+str(name)+'&'+str(filepath)
                                ftable.append(combined)
                            except Exception as e:
                                pass
    print('Processing a total of '+str(len(set(ftable)))+' fusion tables')
    for items in set(ftable):
        id=(items.split('&')[0])
        name=(items.split('&')[1])
        filepath=(items.split('&')[2])
        print('Attempting export: '+str(name)+' to '+str(filepath))
        if ee.data.getInfo(filepath):
            print('File Already Exists: Skipping '+str(filepath))
        else:
            exportnow(collection=id,filename=name,filepath=filepath)


# fexp(local=r'C:\Users\samapriya\Box Sync\IUB\Pycodes\Applications and Tools\Earth Engine Codes\EE_Repo_Headless\samapriya-default',geepath='users/samapriya/vec/')
