import adjustmentNetwork as adjNet

points,observations = adjNet.readIpl('Ex3.ipl')

options = {'fontSize':[14],
           'textOffset':[20],
           'scalePrecision':[10000],
           'scaleReliability':[10000],
           'scaleDisplacement':[10]}

adjNet.plotPoints(points,options)
adjNet.plotObservations(points,observations,options)
adjNet.plotPrecision(points,options)
adjNet.plotReliability(points,options)
adjNet.plotDisplacements(points,options)