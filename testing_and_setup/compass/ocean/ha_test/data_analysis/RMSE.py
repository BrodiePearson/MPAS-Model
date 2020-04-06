from glob import glob
import xarray as xr
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.image import imread
import numpy as np

def is_inside(point, center, radius):
  x = point[0]
  y = point[1]

  center_x = center[0]
  center_y = center[1]

  is_inside = np.sqrt( (x-center_x)**2 + (y-center_y)**2 )

  return is_inside <= radius

def get_RMSE(folder_name):

  # simulated data of where things should be
  simulated_center_location_x =  250000.58 
  simulated_center_location_y =  216506.35 
  radius = 50000.0

  theta = np.linspace(0, 2*np.pi, 100)
  simulated_x = radius * np.cos(theta) + simulated_center_location_x
  simulated_y = radius * np.sin(theta) + simulated_center_location_y



  # first we load the actual location ( saved in the image folder)
  KPP = glob("../"+folder_name+"/default/forward/output/KPP*")
  KPP = KPP[0]
  print("Processing... {}".format(KPP))


  # load data
  data = xr.open_dataset(KPP)
  last_frame = data.tracer1.shape[0] -1


  nCells = data.dims['nCells']
  tracer_exact = np.zeros(nCells)

  
  # get points inside location
  inside_x = []
  inside_y = []
  inside_value = []
  index = 0
  for i in zip(data.xCell.values, data.yCell.values):
    if is_inside(i, [simulated_center_location_x,simulated_center_location_y], radius):
      inside_x.append(i[0])
      inside_y.append(i[1])
      tracer_exact[index] = 1
  index = index + 1

  rmse = np.sqrt(np.mean(tracer_exact - data.tracer1[last_frame,:,99].values)**2)

  print("For  {} RMSE = {}".format(folder_name, rmse))
  # plot points

  plt.scatter(data.xCell, data.yCell, c=data.tracer1[last_frame,:,99])
  plt.scatter(simulated_x, simulated_y)
  plt.savefig("../visualization/"+str(folder_name)+"_plot.png")

  return int(folder_name[0:folder_name.find("km")]) , rmse
  

def main():
  folders = ["5km", "10km", "25km"]
  resolution = []
  rmse = []
  for folder in folders:
    x,y = get_RMSE(folder)
    resolution.append(x)
    rmse.append(y)

  print(resolution)
  print(rmse)
  plt.xlim(3,26)
  plt.ylim(.02,.04)
  plt.loglog()
  plt.scatter(resolution,rmse)
  plt.savefig("../visualization/rmse.png")


main()