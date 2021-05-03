# -*- coding: utf-8 -*-
"""
Viterbi Demo

@author: YBR10
"""
import numpy as np


def viterbi(init, transition, emission, state, observation):
    """T.H.E. Viterbi Algorithm!
    Given an HMM and an observation sequence,
    Viterbi Algorithm returns the most likely hidden state
    that produces the observation.

    Parameters
    ----------
    init : 1d-array
        Initial distribution of the HMM.
    transition : 2d-array
        Transition matrix of the Markov Chain
    emission : 2d-array
        Emission matrix of state i to produce observation j
    state : 1d-array
        States of the HMM.
    observation : 1d-array
        observation sequence

    Returns
    -------
    hidden : 1d-array
        The max-a-posteriori estimator of hidden state sequence.

    """
    hidden = np.zeros_like(observation)
    # likelihood that current observation i is emitted by state j
    phi = np.zeros((len(state), len(observation)))
    # previous maximizing estimator
    prev = np.zeros((len(state), len(observation)))
    
    phi[:, 0] = np.log(init) + np.log(emission[:, observation[0]])
    prev[:, 1] = -1
    
    for ob in range(1, len(observation)):
        score = np.log(transition).T + phi[:, ob-1]
        candidate = np.max(score, axis=1)
        
        prev[:, ob] = np.argmax(score, axis=1)
        phi[:, ob] = np.log(emission[:, observation[ob]]) + candidate
        
    ptr = np.argmax(phi[:, len(observation)-1])
    idx = len(observation) - 1
    while idx >= 0:
        hidden[idx] = ptr
        ptr = int(prev[ptr, idx])
        idx -= 1
            
    return hidden
    

A = np.array([
    [0.2, 0.3, 0.5],
    [0.3, 0.6, 0.1],
    [0.1, 0.8, 0.1]
])

B = np.array([
    [0.2, 0.6, 0.2],
    [0.6, 0.1, 0.3],
    [0.1, 0.2, 0.7]
])

pi = np.array([1/3, 1/3, 1/3])

state = np.array([0, 1, 2])
observation = np.array([0, 0, 1, 1, 1, 2, 2, 0])

ans = viterbi(pi, A, B, state, observation)
