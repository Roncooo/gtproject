import numpy as np

arr = np.array([1,2,3])

copy = np.delete(arr, np.where(arr==1))

print(arr)
print(copy)