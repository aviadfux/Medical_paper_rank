import os
import sys
import math

import numpy as np
import pandas


# Generalized matrix operations:

def __extractNodes(matrix):
    nodes = set()
    for colKey in matrix:
        nodes.add(colKey)
    for rowKey in matrix.T:
        nodes.add(rowKey)
    return nodes


def __makeSquare(matrix, keys, default=0.0):
    matrix = matrix.copy()

    def insertMissingColumns(matrix):
        for key in keys:
            if not key in matrix:
                matrix[key] = pandas.Series(default, index=matrix.index)
        return matrix

    matrix = insertMissingColumns(matrix)  # insert missing columns
    matrix = insertMissingColumns(matrix.T).T  # insert missing rows

    return matrix.fillna(default)


def __ensureRowsPositive(matrix):
    matrix = matrix.T
    for colKey in matrix:
        if matrix[colKey].sum() == 0.0:
            matrix[colKey] = pandas.Series(np.ones(len(matrix[colKey])), index=matrix.index)
    return matrix.T

def __normalizeRows(matrix, default = 0.0):
    return matrix.div(matrix.sum(axis=0), axis=1).fillna(default)

def __euclideanNorm(series):
    return math.sqrt(series.dot(series))

# PageRank specific functionality:
def __startState(nodes):
    if len(nodes) == 0: raise ValueError("There must be at least one node.")
    startProb = 1.0 / float(len(nodes))
    return pandas.Series({node: startProb for node in nodes})

def __integrateRandomSurfer(nodes, transitionProbabilities, d, papers_h_index):
    alpha = (papers_h_index * (1.0 - d)) / np.sum(papers_h_index)

    return transitionProbabilities.copy().multiply(d) + alpha

def __h_index_vector(papers_h_index, nodes, d):
    h_index_vector = pandas.Series(papers_h_index)
    h_index_vector = h_index_vector.div(h_index_vector.sum())
    return (h_index_vector * (1.0 - d)).T

def powerIteration(transitionWeights, papers_h_index, d=0.15, epsilon=0.00001, maxIterations=1000):

    # pandas.Series({node: startProb for node in nodes})

    # Clerical work:
    transitionWeights = pandas.DataFrame(transitionWeights)
    nodes = __extractNodes(transitionWeights)
    transitionWeights = __makeSquare(transitionWeights, nodes, default=0.0)
    # transitionWeights_ = __ensureRowsPositive(transitionWeights)

    # Setup:
    state = __startState(nodes)
    transitionProbabilities = __normalizeRows(transitionWeights)
    #transitionProbabilities = __integrateRandomSurfer(nodes, transitionProbabilities, d, papers_h_index)

    h_index_vector = __h_index_vector(papers_h_index, nodes, d)

    for iteration in range(maxIterations):
        last_state = state
        state = d * np.dot(transitionProbabilities, state.T) + h_index_vector
        if np.linalg.norm(state - last_state, 2) < epsilon:
            break

    return state

    # Power iteration:
    # for iteration in range(maxIterations):
    #     oldState = state.copy()
    #     state = state.dot(transitionProbabilities)
    #     delta = state - oldState
    #     if __euclideanNorm(delta) < epsilon:
    #         break


