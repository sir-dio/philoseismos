""" philoseismos: with passion for the seismic method.

This files defines the Layer class.

@author: Ivan Dubrovin
e-mail: dubrovin.io@icloud.com """

import numpy as np


class Layer:

    def __init__(self, alpha, beta, rho, h):
        """ TODO: decribe """

        self.alpha = alpha
        self.beta = beta
        self.rho = rho
        self.h = h

    def layer_matrix_love(self, omega, c):
        """ Return a layer matrix for Love waves for a given phase velocity and frequency. """

        if c == self.beta:
            return np.identity(2)

        k = omega / c
        mu = self.beta ** 2 * self.rho

        s = np.lib.scimath.sqrt((omega / self.beta) ** 2 - k ** 2)
        Q = self.h * s

        a11 = np.cos(Q)
        a12 = np.sin(Q) / mu / s
        a21 = -mu * s * np.sin(Q)
        a22 = a11

        A = np.array([
            [a11, a12],
            [a21, a22]
        ])

        # all the values in A are real, but since `s` might have been imaginary, they
        # are stored as complex numbers. scipy.optimise.bisect is a dick about it, so
        # before returning the matrix we cast it to real

        return np.real(A)

    def layer_matrix_rayleigh(self, omega, c):
        """ Return a layer matrix for Rayleigh waves for a given phase velocity and frequency. """

        k = omega / c

        r = np.lib.scimath.sqrt((c / self.alpha) ** 2 - 1)
        s = np.lib.scimath.sqrt((c / self.beta) ** 2 - 1)

        gamma = 2 * (self.beta / c) ** 2
        delta = gamma - 1

        P = k * r * self.h
        Q = k * s * self.h

        a11 = a44 = gamma * np.cos(P) - delta * np.cos(Q)

        if r == 0:
            a12 = a34 = gamma * s * np.sin(Q)
        else:
            a12 = a34 = delta / r * np.sin(P) + gamma * s * np.sin(Q)

        a13 = a24 = -(np.cos(P) - np.cos(Q)) / self.rho

        if r == 0:
            a14 = s * np.sin(Q) / self.rho
        else:
            a14 = (np.sin(P) / r + s * np.sin(Q)) / self.rho

        if s == 0:
            a21 = a43 = gamma * r * np.sin(P)
        else:
            a21 = a43 = gamma * r * np.sin(P) + delta / s * np.sin(Q)

        a22 = a33 = -delta * np.cos(P) + gamma * np.cos(Q)

        if s == 0:
            a23 = -r * np.sin(P) / self.rho
        else:
            a23 = -(r * np.sin(P) + np.sin(Q) / s) / self.rho

        a31 = a42 = self.rho * gamma * delta * (np.cos(P) - np.cos(Q))

        if r == 0:
            a32 = self.rho * gamma ** 2 * s * np.sin(Q)
        else:
            a32 = self.rho * (delta ** 2 / r * np.sin(P) + gamma ** 2 * s * np.sin(Q))

        if s == 0:
            a41 = -self.rho * gamma ** 2 * r * np.sin(P)
        else:
            a41 = -self.rho * (gamma ** 2 * r * np.sin(P) + delta ** 2 / s * np.sin(Q))

        A = np.array([
            [a11, a12, a13, a14],
            [a21, a22, a23, a24],
            [a31, a32, a33, a34],
            [a41, a42, a43, a44]
        ])

        return np.real(A)
