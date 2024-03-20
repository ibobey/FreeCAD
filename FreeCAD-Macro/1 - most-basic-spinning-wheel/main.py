import FreeCAD
from PySide import QtCore
import PartDesignGui
import ProfileLib.RegularPolygon


r = 0
x = 0
timer = QtCore.QTimer()

# Creating New Doc

App.newDocument()

# Creating Part
App.activeDocument().addObject('PartDesign::Body','Body')
App.ActiveDocument.getObject('Body').Label = 'Body'
App.ActiveDocument.recompute()


# Creating Sketch
App.getDocument('Unnamed').getObject('Body').newObject('Sketcher::SketchObject','Sketch')
App.getDocument('Unnamed').getObject('Sketch').Support = (App.getDocument('Unnamed').getObject('XY_Plane'),[''])
App.getDocument('Unnamed').getObject('Sketch').MapMode = 'FlatFace'
App.ActiveDocument.recompute()

 
# Drawing Circle
App.getDocument('Unnamed').getObject('Sketch').addGeometry(Part.Circle(App.Vector(0.000000,0.000000,0),App.Vector(0,0,1),35.576162),False)
App.getDocument('Unnamed').getObject('Sketch').addConstraint(Sketcher.Constraint('Coincident',0,3,-1,1)) 

App.getDocument('Unnamed').getObject('Sketch').addConstraint(Sketcher.Constraint('Radius',0,35.576162))
App.getDocument('Unnamed').getObject('Sketch').setDatum(1,App.Units.Quantity('1000.000000 mm'))


# Drawing Hexagon
ProfileLib.RegularPolygon.makeRegularPolygon(App.getDocument('Unnamed').getObject('Sketch'),6,App.Vector(0.000000,0.000000,0),App.Vector(321.354431,0.000000,0),False)
App.getDocument('Unnamed').getObject('Sketch').addConstraint(Sketcher.Constraint('Coincident',7,3,0,3)) 
App.getDocument('Unnamed').getObject('Sketch').addConstraint(Sketcher.Constraint('PointOnObject',6,2,-1)) 
App.getDocument('Unnamed').getObject('Sketch').addConstraint(Sketcher.Constraint('DistanceX',5,1,5,2,321.354431))
App.getDocument('Unnamed').getObject('Sketch').setDatum(21,App.Units.Quantity('250.000000 mm'))

App.ActiveDocument.recompute()
App.getDocument('Unnamed').recompute()


# Create Pad
App.getDocument('Unnamed').getObject('Body').newObject('PartDesign::Pad','Pad')
App.getDocument('Unnamed').getObject('Pad').Profile = App.getDocument('Unnamed').getObject('Sketch')
App.getDocument('Unnamed').getObject('Pad').Length = 10
App.ActiveDocument.recompute()
App.getDocument('Unnamed').getObject('Pad').ReferenceAxis = (App.getDocument('Unnamed').getObject('Sketch'),['N_Axis'])
App.getDocument('Unnamed').getObject('Sketch').Visibility = False
App.ActiveDocument.recompute()


# Padding Sketch
App.getDocument('Unnamed').getObject('Pad').Length = 500.000000
App.getDocument('Unnamed').getObject('Pad').TaperAngle = 0.000000
App.getDocument('Unnamed').getObject('Pad').UseCustomVector = 0
App.getDocument('Unnamed').getObject('Pad').Direction = (0, 0, 1)
App.getDocument('Unnamed').getObject('Pad').ReferenceAxis = (App.getDocument('Unnamed').getObject('Sketch'), ['N_Axis'])
App.getDocument('Unnamed').getObject('Pad').AlongSketchNormal = 1
App.getDocument('Unnamed').getObject('Pad').Type = 0
App.getDocument('Unnamed').getObject('Pad').UpToFace = None
App.getDocument('Unnamed').getObject('Pad').Reversed = 0
App.getDocument('Unnamed').getObject('Pad').Midplane = 0
App.getDocument('Unnamed').getObject('Pad').Offset = 0
App.getDocument('Unnamed').recompute()
App.getDocument('Unnamed').getObject('Sketch').Visibility = False

# update function
def update():
	global r
	global x
	
	if x > 1000:
		timer.stop()
		return

	x += 2 * 3.14 * r * (1 / 360)
	FreeCAD.getDocument('Unnamed').getObject('Body').Placement = App.Placement(App.Vector(x,0,0),App.Rotation(App.Vector(0,0,1), r))
	r += 1
	print(f"angle: {r}, position: {x}")
	return 

# Starting Animation

timer.timeout.connect(update)
timer.start(100)
	
