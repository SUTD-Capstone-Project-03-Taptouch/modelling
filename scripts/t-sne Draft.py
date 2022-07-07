import numpy as np
from sklearn import manifold

# Note: Running this code on its own will result in an error. Google colab has all the important stuff for now.

X = np.array(lstm_embedding)
nsamples, nx, ny = X.shape
data = X.reshape((nsamples, nx * ny))

tsne_em = manifold.TSNE(n_components=20, perplexity=100, n_iter=500, verbose=1, method="exact").fit_transform(data)
print(tsne_em)



