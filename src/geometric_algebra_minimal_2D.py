from __future__ import annotations

"""
A small 2-D geometric-geometric algebra playground built on top of SymjPy.

This script:
1. Defines some minimal helper functions for geometric algebra.
2. Demonstrates vector projection and rotation.
3. Prints some test cases.
"""

import sympy as sp
from sympy import Matrix, simplify
from typing import TypeAlias

Vector: TypeAlias = Matrix      # a 2-D column vector in SymPy

def dot (a: Vector, b: Vector) -> sp.Expr:
    """Return the Euclidean (inner) prodcut of two 2-D column vectors."""
    _validate_vector(a)
    _validate_vector(b)
    return a.dot(b)

def wedge (a: Vector, b: Vector) -> sp.Expr:
    """
    Return the 2-D exterior (wedge) product of two vectors.
    
    Here, for the 2-D case the result is a pseudoscalar representing the signed area of teh parallelogram spanned by **a** and **b**.
    """
    _validate_vector(a)
    _validate_vector(b)
    return a[0] * b[1] - a[1] * b[0]

def geometric_prod_vec(a: Vector, b: Vector) -> sp.Expr:
    """Simulate the geometric product of two vectors."""
    return dot(a,b) + wedge(a,b)

def project(u: Vector, v: Vector) -> Vector:
    """Orthogonality project *u* onto *v*."""
    vv = dot(u, v)
    if vv == 0:
        raise ZeroDivisionError("Cannot project onto the zero vector.")
    return dot(u, v) * u / vv 

def reject(x: Vector, u: Vector) -> Vector:
    """
    The rejection of *u* from *v* in 2-D.
    """
    uu = dot(u, u)
    if uu == 0:
        raise ZeroDivisionError("Cannot reject about the zero vector.")
    scalar = wedge(x, u) / uu
    # Rotate about pi/2 to obtain a perpendicular vector (-y, x).
    return Matrix([-u[1], u[0]]) * scalar


def _validate_vector(v: Vector) -> None:
    """Ensure *v* is a 2-D column vector."""
    if v.shape != (2, 1):
        msg = f"Expected a 2-D column vector, got shape {v.shape!r}"
        raise ValueError(msg)
    
# CLI Entry Point
def main() -> None:
    """Small test demo if module is run as a script."""
    e1: Vector = Matrix([1, 0])
    e2: Vector = Matrix([0, 1])
    
    u: Vector = 4 * e1 + 2 * e2
    v: Vector = 3 * e1 + 3 * e2
    
    proj: Vector = project(u, v)
    rej: Vector = reject(u, v)
    
    print(f"proj = {proj}")
    print(f"proj (simplified) = {simplify(proj)}")

    print(f"\nrej = {rej}")
    print(f"rej (simplified) = {simplify(rej)}")
    
    uv_scalar = dot(u, v)
    uv_bivector = wedge(u, v)
    print(f"\nu v = {uv_scalar} + {uv_bivector}*(e1 wedge e2)")
    
if __name__ == "__main__":
    main()