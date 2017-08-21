# -*- coding: utf-8 -*-

import re
import os
import shutil
import codecs
from utils import replaceInTemplate


def writeFoldersAndFiles(pluginDir, feedback, outputProjectFileName,
                         cluster_set, measure, matchCRS, layerSearch, canvas,
                         mapLibLocation, address, locate, debugLibs):
    feedback.showFeedback("Exporting libraries...")
    jsStore = os.path.join(outputProjectFileName, 'js')
    os.makedirs(jsStore)
    jsStore += os.sep
    jsDir = pluginDir + os.sep + 'js' + os.sep
    dataStore = os.path.join(outputProjectFileName, 'data')
    os.makedirs(dataStore)
    imageDir = pluginDir + os.sep + 'images' + os.sep
    imageStore = os.path.join(outputProjectFileName, 'images')
    legendStore = os.path.join(outputProjectFileName, 'legend')
    os.makedirs(legendStore)
    cssStore = os.path.join(outputProjectFileName, 'css')
    os.makedirs(cssStore)
    cssStore += os.sep
    cssDir = pluginDir + os.sep + 'css' + os.sep
    markerStore = os.path.join(outputProjectFileName, 'markers')
    os.makedirs(markerStore)
    shutil.copyfile(jsDir + 'qgis2web_expressions.js',
                    jsStore + 'qgis2web_expressions.js')
    shutil.copyfile(jsDir + 'leaflet-tilelayer-wmts.js',
                    jsStore + 'leaflet-tilelayer-wmts.js')
    shutil.copyfile(jsDir + 'leaflet-svg-shape-markers.min.js',
                    jsStore + 'leaflet-svg-shape-markers.min.js')
    if mapLibLocation == "Local":
        if debugLibs:
            shutil.copyfile(jsDir + 'leaflet-src.js',
                            jsStore + 'leaflet-src.js')
        else:
            shutil.copyfile(jsDir + 'leaflet.js', jsStore + 'leaflet.js')
        shutil.copyfile(cssDir + 'leaflet.css', cssStore + 'leaflet.css')
    if address:
        shutil.copyfile(jsDir + 'Control.OSMGeocoder.js',
                        jsStore + 'Control.OSMGeocoder.js')
        shutil.copyfile(cssDir + 'Control.OSMGeocoder.css',
                        cssStore + 'Control.OSMGeocoder.css')
    if locate:
        shutil.copyfile(jsDir + 'L.Control.Locate.min.js',
                        jsStore + 'L.Control.Locate.min.js')
        shutil.copyfile(cssDir + 'L.Control.Locate.min.css',
                        cssStore + 'L.Control.Locate.min.css')
    shutil.copyfile(jsDir + 'multi-style-layer.js',
                    jsStore + 'multi-style-layer.js')
    shutil.copyfile(jsDir + 'Autolinker.min.js',
                    jsStore + 'Autolinker.min.js')
    shutil.copyfile(jsDir + 'OSMBuildings-Leaflet.js',
                    jsStore + 'OSMBuildings-Leaflet.js')
    shutil.copyfile(jsDir + 'leaflet-heat.js',
                    jsStore + 'leaflet-heat.js')
    shutil.copyfile(jsDir + 'leaflet-hash.js', jsStore + 'leaflet-hash.js')
    shutil.copyfile(jsDir + 'leaflet.rotatedMarker.js',
                    jsStore + 'leaflet.rotatedMarker.js')
    if len(cluster_set):
        shutil.copyfile(jsDir + 'leaflet.markercluster.js',
                        jsStore + 'leaflet.markercluster.js')
        shutil.copyfile(cssDir + 'MarkerCluster.css',
                        cssStore + 'MarkerCluster.css')
        shutil.copyfile(cssDir + 'MarkerCluster.Default.css',
                        cssStore + 'MarkerCluster.Default.css')
    if layerSearch != "None":
        shutil.copyfile(jsDir + 'leaflet-search.js',
                        jsStore + 'leaflet-search.js')
        shutil.copyfile(cssDir + 'leaflet-search.css',
                        cssStore + 'leaflet-search.css')
        shutil.copytree(imageDir, imageStore)
    if measure != "None":
        shutil.copyfile(jsDir + 'leaflet-measure.js',
                        jsStore + 'leaflet-measure.js')
        shutil.copyfile(cssDir + 'leaflet-measure.css',
                        cssStore + 'leaflet-measure.css')
    shutil.copytree(cssDir + 'images', cssStore + 'images')
    if (matchCRS and
            canvas.mapSettings().destinationCrs().authid() != 'EPSG:4326'):
        shutil.copyfile(jsDir + 'proj4.js', jsStore + 'proj4.js')
        shutil.copyfile(jsDir + 'proj4leaflet.js', jsStore + 'proj4leaflet.js')
    feedback.completeStep()
    return dataStore, cssStore


def writeHTMLstart(outputIndex, webpage_name, cluster_set, address, measure,
                   matchCRS, layerSearch, canvas, mapLibLocation, locate,
                   qgis2webJS, template, feedback, debugLibs):
    feedback.showFeedback("Writing HTML...")
    if webpage_name == "":
        pass
    else:
        webpage_name = unicode(webpage_name)
    if mapLibLocation == "Local":
        cssAddress = '<link rel="stylesheet" href="css/leaflet.css">'
        if debugLibs:
            jsAddress = '<script src="js/leaflet-src.js"></script>'
        else:
            jsAddress = '<script src="js/leaflet.js"></script>'
    else:
        cssAddress = '<link rel="stylesheet" href='
        cssAddress += '"http://unpkg.com/leaflet@1.0.3/dist/leaflet.css">'
        jsAddress = '<script src="http://'
        jsAddress += 'unpkg.com/leaflet@1.0.3/dist/leaflet.js"></script>'
    if locate:
        cssAddress += '<link rel="stylesheet" '
        cssAddress += 'href="http://maxcdn.bootstrapcdn.com/font-awesome/'
        cssAddress += '4.6.1/css/font-awesome.min.css">'
        cssAddress += '<link rel="stylesheet" '
        cssAddress += 'href="css/L.Control.Locate.min.css">'
        jsAddress += '<script src="js/L.Control.Locate.min.js"></script>'
    jsAddress += """
        <script src="js/multi-style-layer.js"></script>"""
    jsAddress += """
        <script src="js/leaflet-heat.js"></script>"""
    jsAddress += """
        <script src="js/leaflet-svg-shape-markers.min.js"></script>"""
    jsAddress += """
        <script src="js/leaflet.rotatedMarker.js"></script>"""
    jsAddress += """
        <script src="js/OSMBuildings-Leaflet.js"></script>"""
    extracss = '<link rel="stylesheet" href="css/qgis2web.css">'
    if len(cluster_set):
        clusterCSS = """<link rel="stylesheet" href="css/MarkerCluster.css">
        <link rel="stylesheet" href="css/MarkerCluster.Default.css">"""
        clusterJS = '<script src="js/leaflet.markercluster.js">'
        clusterJS += "</script>"
    else:
        clusterCSS = ""
        clusterJS = ""
    if layerSearch != "None":
        layerSearchCSS = '<link rel="stylesheet" '
        layerSearchCSS += 'href="css/leaflet-search.css">'
        layerSearchJS = '<script src="js/leaflet-search.js"></script>'
    else:
        layerSearchCSS = ""
        layerSearchJS = ""
    if address:
        addressCSS = """
        <link rel="stylesheet" href="css/Control.OSMGeocoder.css">"""
        addressJS = """
        <script src="js/Control.OSMGeocoder.js"></script>"""
    else:
        addressCSS = ""
        addressJS = ""
    if measure != "None":
        measureCSS = """
        <link rel="stylesheet" href="css/leaflet-measure.css">"""
        measureJS = """
        <script src="js/leaflet-measure.js"></script>"""
    else:
        measureCSS = ""
        measureJS = ""
    extraJS = """<script src="js/leaflet-hash.js"></script>
        <script src="js/leaflet-tilelayer-wmts.js"></script>
        <script src="js/Autolinker.min.js"></script>"""
    if (matchCRS and
            canvas.mapSettings().destinationCrs().authid() != 'EPSG:4326'):
        crsJS = """
        <script src="js/proj4.js"></script>
        <script src="js/proj4leaflet.js"></script>"""
    else:
        crsJS = ""
    exp_js = """
        <script src="js/qgis2web_expressions.js"></script>"""

    canvasSize = canvas.size()
    values = {"@PAGETITLE@": webpage_name,
              "@CSSADDRESS@": cssAddress,
              "@EXTRACSS@": extracss,
              "@JSADDRESS@": jsAddress,
              "@LEAFLET_CLUSTERCSS@": clusterCSS,
              "@LEAFLET_CLUSTERJS@": clusterJS,
              "@LEAFLET_LAYERSEARCHCSS@": layerSearchCSS,
              "@LEAFLET_LAYERSEARCHJS@": layerSearchJS,
              "@LEAFLET_ADDRESSCSS@": addressCSS,
              "@LEAFLET_MEASURECSS@": measureCSS,
              "@LEAFLET_EXTRAJS@": extraJS,
              "@LEAFLET_ADDRESSJS@": addressJS,
              "@LEAFLET_MEASUREJS@": measureJS,
              "@LEAFLET_CRSJS@": crsJS,
              "@QGIS2WEBJS@": qgis2webJS,
              "@MAP_WIDTH@": unicode(canvasSize.width()) + "px",
              "@MAP_HEIGHT@": unicode(canvasSize.height()) + "px",
              "@EXP_JS@": exp_js,
              "@OL3_BACKGROUNDCOLOR@": "",
              "@OL3_STYLEVARS@": "",
              "@OL3_POPUP@": "",
              "@OL3_GEOJSONVARS@": "",
              "@OL3_WFSVARS@": "",
              "@OL3_PROJ4@": "",
              "@OL3_PROJDEF@": "",
              "@OL3_GEOCODINGLINKS@": "",
              "@OL3_GEOCODINGJS@": "",
              "@OL3_LAYERSWITCHER@": "",
              "@OL3_LAYERS@": "",
              "@OL3_MEASURESTYLE@": ""}

    with codecs.open(outputIndex, 'w', encoding='utf-8') as f:
        base = replaceInTemplate(template + ".html", values)
        base = re.sub('\n[\s_]+\n', '\n', base)
        f.write(unicode(base))
        f.close()
    feedback.completeStep()


def writeCSS(cssStore, backgroundColor, feedback):
    feedback.showFeedback("Writing CSS...")
    with open(cssStore + 'qgis2web.css', 'w') as f_css:
        text = """
#map {
    background-color: """ + backgroundColor + """
}
th {
    text-align: left;
    vertical-align: top;
}
.info {
    padding: 6px 8px;
    font: 14px/16px Arial, Helvetica, sans-serif;
    background: white;
    background: rgba(255,255,255,0.8);
    box-shadow: 0 0 15px rgba(0,0,0,0.2);
    border-radius: 5px;
}
.info h2 {
    margin: 0 0 5px;
    color: #777;
}
.leaflet-container {
    background: #fff;
}
.leaflet-popup-content {
    width:auto !important;
}
.leaflet-tooltip {
    background: none;
    box-shadow: none;
    border: none;
}
.leaflet-tooltip-left:before, .leaflet-tooltip-right:before {
    border: 0px;
}"""
        f_css.write(text)
        f_css.close()
    feedback.completeStep()
