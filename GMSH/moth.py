# ------------------------------------------------------------------------------
#
#  Gmsh Python tutorial 13
#
#  Remeshing an STL file without an underlying CAD model
#
# ------------------------------------------------------------------------------

import gmsh
import math
import os
import sys

gmsh.initialize()


path = os.path.dirname(os.path.abspath(__file__))
gmsh.merge(os.path.join(path, 'moth.stl'))

angle = 30
forceParametrizablePatches = False


includeBoundary = True


curveAngle = 180

gmsh.model.mesh.classifySurfaces(angle * math.pi / 180., includeBoundary,
                                 forceParametrizablePatches,
                                 curveAngle * math.pi / 180.)

gmsh.model.mesh.createGeometry()

s = gmsh.model.getEntities(2)
l = gmsh.model.geo.addSurfaceLoop([s[i][1] for i in range(len(s))])
gmsh.model.geo.addVolume([l])

gmsh.model.geo.synchronize()

funny = False
f = gmsh.model.mesh.field.add("MathEval")
if funny:
    gmsh.model.mesh.field.setString(f, "F", "2*Sin((x+y)/5) + 3")
else:
    gmsh.model.mesh.field.setString(f, "F", "100")
gmsh.model.mesh.field.setAsBackgroundMesh(f)

gmsh.model.mesh.generate(3)
gmsh.write('moth.msh')


if '-nopopup' not in sys.argv:
    gmsh.fltk.run()

gmsh.finalize()

