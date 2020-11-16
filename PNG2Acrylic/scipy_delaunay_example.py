import numpy as np
import scipy.spatial

# Configuration.
POINTS_FILENAME = 'XYZcolorlist_D65.csv'
TARGETS_FILENAME = 'targets.csv'
OUTPUT_FILENAME = 'gamut.ppm'
DEFAULT_COLOR = np.array([[255, 255, 255]], dtype=np.uint8)

# Load colors
colors = np.loadtxt(POINTS_FILENAME, usecols=(0,), delimiter=',', 
                    converters={0:lambda s:s.split()}, dtype=np.uint8)

# Load points
points = np.loadtxt(POINTS_FILENAME, usecols=(1, 2, 3), delimiter=',')

# Load targets
targets = np.loadtxt(TARGETS_FILENAME, delimiter=',')
ntargets = len(targets)

# Compute Delaunay triangulation of points.
tri = scipy.spatial.Delaunay(points)

# Find the tetrahedron containing each target (or -1 if not found)
tetrahedra = tri.find_simplex(targets)

# Affine transformation for tetrahedron containing each target
X = tri.transform[tetrahedra, :3]

# Offset of each target from the origin of its containing tetrahedron
Y = targets - tri.transform[tetrahedra, 3]

# First three barycentric coordinates of each target in its tetrahedron.
# The fourth coordinate would be 1 - b.sum(axis=1), but we don't need it.
b = np.einsum('...jk,...k->...j', X, Y)

# Cumulative sum of barycentric coordinates of each target.
bsum = np.c_[b.cumsum(axis=1), np.ones(ntargets)]

# A uniform random number in [0, 1] for each target.
R = np.random.uniform(0, 1, size=(ntargets, 1))

# Randomly choose one of the tetrahedron vertices for each target,
# weighted according to its barycentric coordinates, and get its
# color.
C = colors[tri.simplices[tetrahedra, np.argmax(R <= bsum, axis=1)]]

# Mask out the targets where we failed to find a tetrahedron.
C[tetrahedra == -1] = DEFAULT_COLOR

# Determine width and height of image.
# (Since I don't have your TIFF, this is the best I can do!)
width, height = 1, ntargets

# Write output as image in PPM format.
with open(OUTPUT_FILENAME, 'wb') as ppm:
    ppm.write("P3\n{} {}\n255\n".format(width, height).encode('ascii'))
    np.savetxt(ppm, C, fmt='%d')