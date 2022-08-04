import { Ion, Viewer, createWorldTerrain, Matrix4, Cartesian3, Transforms, JulianDate,CzmlDataSource, defined,SceneMode } from "cesium";
import "cesium/Widgets/widgets.css";
import "../src/css/main.css"
import "cesium"



// Initialize the Cesium Viewer in the HTML element with the `cesiumContainer` ID.
const viewer = new Viewer('cesiumContainer', {
terrainProvider: createWorldTerrain()
});


var czml_data = "";
//$.get("http://localhost/src/test.czml", function(data){  czml_data = data;});


var czmlDataSource2 = new CzmlDataSource();
czmlDataSource2.load("czml/booster.czml");
viewer.dataSources.add(czmlDataSource2);   

// Add Cesium OSM Buildings, a global 3D buildings layer.
var startDate = new Date(2022,0,22);
var startTime =  JulianDate.fromDate(startDate);
var endTime = JulianDate.addDays(startTime, 10, new JulianDate());
viewer.clock.currentTime = startTime;
viewer.timeline.zoomTo(startTime, endTime);


function icrf(scene, time) {
    if (scene.mode !== SceneMode.SCENE3D) {
        return;
    }

    var icrfToFixed = Transforms.computeIcrfToFixedMatrix(time);
    if (defined(icrfToFixed)) {
        var camera = viewer.camera;
        var offset = Cartesian3.clone(camera.position);
        var transform = Matrix4.fromRotationTranslation(icrfToFixed);
        camera.lookAtTransform(transform, offset);
    }
}

viewer.scene.postUpdate.addEventListener(icrf);
