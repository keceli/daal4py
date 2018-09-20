#*******************************************************************************
# Copyright 2014-2018 Intel Corporation
# All Rights Reserved.
#
# This software is licensed under the Apache License, Version 2.0 (the
# "License"), the following terms apply:
#
# You may not use this file except in compliance with the License.  You may
# obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#
# See the License for the specific language governing permissions and
# limitations under the License.
#*******************************************************************************

# daal4py LBFGS (limited memory Broyden-Fletcher-Goldfarb-Shanno) example for shared memory systems
# using cross entropy loss function

import daal4py as d4p
import numpy as np

# let's try to use pandas' fast csv reader
try:
    import pandas
    read_csv = lambda f, c: pandas.read_csv(f, usecols=c, delimiter=',', header=None).values
except:
    # fall back to numpy loadtxt
    read_csv = lambda f, c: np.loadtxt(f, usecols=c, delimiter=',')


def main():
    nFeatures = 6
    nClasses = 5
    nIterations = 1000
    stepLength = 1.0e-4

    infile = "./data/batch/logreg_train.csv"

    # Read the data
    data = read_csv(infile, range(nFeatures))
    dep_data = read_csv(infile, range(nFeatures, nFeatures + 1))
    nVectors = data.shape[0]
    dep_data.shape = (nVectors, 1) # must be a 2d array

    # configure a function
    func = d4p.optimization_solver_cross_entropy_loss(nClasses, nVectors)
    func.setup(data, dep_data, None)

    # configure a algorithm
    stepLengthSequence = np.array([[stepLength]], dtype=np.float64)
    alg = d4p.optimization_solver_lbfgs(func,
                                        stepLengthSequence=stepLengthSequence,
                                        nIterations=nIterations)

    # do the cumputation
    nParameters = nClasses * (nFeatures + 1)
    initialPoint = np.full((nParameters, 1), 0.001, dtype=np.float64)
    res = alg.compute(initialPoint)

    # result provides minimum and nIterations
    assert res.minimum.shape == (nParameters, 1)
    assert res.nIterations[0][0] <= nIterations

    return res


if __name__ == "__main__":
    res = main()
    print("\nExpected coefficients:\n", np.array([[-2.277], [2.836], [14.985], [0.511], [7.510], [-2.831], [-5.814], [-0.033], [13.227], [-24.447], [3.730],
        [10.394], [-10.461], [-0.766], [0.077], [1.558], [-1.133], [2.884], [-3.825], [7.699], [2.421], [-0.135], [-6.996], [1.785], [-2.294], [-9.819], [1.692],
        [-0.725], [0.069], [-8.41], [1.458], [-3.306], [-4.719], [5.507], [-1.642]], dtype=np.float64))
    print("\nResulting coefficients:\n", res.minimum)
    print("\nNumber of iterations performed:\n", res.nIterations[0][0])
    print('All looks good!')

