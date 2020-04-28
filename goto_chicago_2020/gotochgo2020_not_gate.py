#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite
from dimod import BinaryQuadraticModel


# In[ ]:


# !x = z
qubo = {(0, 0): -1, (1, 1): -1, (0, 1): 2} 


# In[ ]:


bqm = BinaryQuadraticModel.from_qubo(qubo)
print(bqm)


# In[ ]:


sampler = EmbeddingComposite(DWaveSampler())


# In[ ]:


print("Sampling")
response = sampler.sample(bqm, num_reads=500)
print("Done")

