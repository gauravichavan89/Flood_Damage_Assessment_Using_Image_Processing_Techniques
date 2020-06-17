# Flood Damage Assessment Using Image Processing Techniques 

## (Property Evaluation Based on Area & Producing Front & Top view of each property)


In order to estimate every residential accommodation, we segregated the model functionality such that it caters to two primary requirements. The first requirement is to compute the area of the property and the second requirement is to produce the top and street view of the property which would help one in demonstrating the property’s architectural design(address, presence and type of garage, number of storeys, living area space). This was achieved using GIS, Satellite &amp; Street View Images, Google Maps and Places API, JSP, JSON &amp; jQuery. This property assessment was undertaken as a precautionary measure for flood damage control by the 'Government of Alberta'.



## Lets get this project up and running!!!


* Install Apache http server and enable the localhost for running the application.
* Click on the MapRetrievalProgram.html and run it on Chrome.
* Select your Province region from the given dropdown (preferably Alberta)
* Once the satellite view of the selected province loads, zoom in to any city region which has clear top view images of the plots/houses shown
* Click on the Draw Rectangle button to draw a Polygon for a particular property. This would load the Centroid coordinate values for that selected property.
* Once the polygon has been drawn, save the top view image of the property by clicking on the Save the TopView Maps button. 
* Next step is to Load the StreetView image of the selected property. Once this has been clicked, you will be able to see the street view image. Click on the Save the StreetView Maps button to save the street view image.
* Once all these steps have been completed, click on the Download CSV link to download a CSV file containing the information collected from the steps mentioned above. This CSV file called mapData will saved to the Downloads folder. Copy the CSV file and paste it in the same location as MapRetrievalProgram.html
* The images saved from the application will be stored inside the folder Images.
* Now run the python program ImageProcess.py
* This will now take in the generated images and the data collected from the CSV file for further processing.
* The results are then displayed with the selected property information which can then be used for evaluation purpose.

