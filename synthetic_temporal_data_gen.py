#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  9 19:35:26 2021

@author: Grosvenor
"""

import numpy as np

def get_spirals_dataset(n_examples, n_rotations, env, n_envs,
                        n_dims_signatures,
                        seed=None):
    a = 1.0001 #exponentially increasing influence on spurious correlations with time
    #a=.00095 exponentially decreasing influence on spurious correlations with time
    alpha = np.pi/20
    
    assert env == 'test' or 0 <= int(env) < n_envs

    # Generate fixed dictionary of signatures
    rng = np.random.RandomState(seed)
    
    """
    The signatures_matrix is used to generate the spurious coordinates in 
    each environment. In the original dataset, the coordiantes are randomly 
    generated. In the case of temporal IRM, after generating the spurious 
    coordiantes randomly, we loop through the rows of the signatures_matrix 
    and act on each coordinate with a time dependent funtion. Time is 
    implicitly present as the coordinates of each environment 
    is dependent on pervious time step. 
    
    Here we have chosen two types of time influence: 
    The influence on spurious correlations can either increase or decrease 
    with time. There are potentially other more interesting choices as well. 
    """
    signatures_matrix = rng.randn(n_envs, n_dims_signatures)
    for i in range(n_envs-1):
        signatures_matrix[i+1]=np.multiply(signatures_matrix[i],a**i)
        

    radii = rng.uniform(0.08, 1, n_examples)
    angles = 2 * n_rotations * np.pi * radii
    
    labels = rng.randint(0, 2, n_examples)
    angles = angles + np.pi * labels
    
    radii += rng.uniform(-0.02, 0.02, n_examples)
    xs = np.cos(angles) * radii
    ys = np.sin(angles) * radii
   
    
    if env == 'test':
        signatures = rng.randn(n_examples, n_dims_signatures)
    
    
    else:
        env = int(env)
        signatures_labels = np.array(labels * 2 - 1).reshape(1, -1)
        signatures = signatures_matrix[env] * signatures_labels.T
        xs = np.cos(angles+(env+1)*alpha) * radii
        ys = np.sin(angles+(env+1)*alpha) * radii
        """
        Note that the above addtion to the angles rotates the Cartesian spiral 
        coordinates by an amount alpha (set above) as we progress through 
        environments. 
        """

    
    signatures = np.stack(signatures)
    mechanisms = np.stack((xs, ys), axis=1)
    mechanisms /= mechanisms.std(axis=0)  
    inputs = np.hstack((mechanisms, signatures))
    
    #
    return inputs.astype(np.float32), labels.astype(np.float32)