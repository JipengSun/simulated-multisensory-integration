'''
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation

fig = plt.figure()
data = np.random.random((255, 255))
im = plt.imshow(data, cmap='gray')

# animation function.  This is called sequentially
def animate(i):
    data = np.random.random((255, 255))
    im.set_array(data)
    return [im]

anim = animation.FuncAnimation(fig, animate, frames=200, interval=60, blit=True)
plt.show()
'''

from __future__ import print_function
import torch
'''
x = torch.empty(5,3)
print (x)
y = torch.zeros(5,3,dtype=torch.long)
print (x[:,1])
z = x.view(-1,3)
a = z.numpy()
z.add_(1)
print (z)
print (a)
'''

x = torch.ones(2,2,requires_grad=True)
print (x)
y = x + 2
print (y)
print (y.grad_fn)
z = y * y * 3
out = z.mean()
print (z, out)

a = torch.randn(2,2)
a = ((a*3)/(a-1))
print (a.requires_grad)
a.requires_grad_(True)
print (a.requires_grad)
b = (a*a).sum()
print (b.grad_fn)
out.backward()
print(x.grad)