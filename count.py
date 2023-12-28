# -*- coding: utf-8 -*-
import rhinoscriptsyntax as rs
import Rhino
import csv
import collections
from operator import add

def CalculateArea(Objects):
    SumArea = []
    for m in Objects:
        if rs.IsBrep(m):
             areaBrep = rs.Area(m)
             SumArea.append(areaBrep)
        elif rs.IsSurface(m):
             areaSurf = rs.Area(m)
             SumArea.append(areaSurf)
        elif rs.IsMesh(m):
             areaMesh = rs.Area(m)
             SumArea.append(areaMesh)
    f.write(str(round(sum(SumArea)/1000000,1))+ ',')

def CountWindow(Objects):
    sumLength = []
    sumArea = []
    
    for Object in Objects:
      
        boundingBoxCorner = rs.BoundingBox(Object)
        
        
        if boundingBoxCorner:
               cornerPoints = [ 
                                boundingBoxCorner[0],
                                boundingBoxCorner[2], 
                                boundingBoxCorner[6],  
                                boundingBoxCorner[4], 
                                boundingBoxCorner[0]
                              ]
               windowsCurve = rs.AddPolyline(cornerPoints)
               length = rs.CurveLength(windowsCurve)/1000
               area = rs.Area(windowsCurve)/1000000
               sumLength.append(length)
               sumArea.append(area)
               rs.DeleteObject(windowsCurve)
    f.write(str(round(sum(sumArea),1))+ ','  + str(round(sum(sumLength),1))+ ',')
    
def CalculateLength(Objects):
    handrailLength = []
    for m in Objects:
        if rs.IsCurve(m):
             len = rs.CurveLength(m)
             handrailLength.append(len)
    
    f.write("_" + ',' + str(round(sum(handrailLength)/1000,1))+ ',')


layers = Rhino.RhinoDoc.ActiveDoc.Layers
names = rs.LayerIds()

active_rhino_file_name = rs.DocumentName().split(".")[0]
file_name = '{}.csv'.format(active_rhino_file_name)

with open(file_name, "w") as f:
    f.write('レイヤーネーム'.encode('utf-8') + ',' + 'オブジェクト数'.encode('utf-8')+ ','+ "面積(m2)".encode('utf-8') +','+ "周長(m)".encode('utf-8') + "\n")
    for name, l in zip(names,layers):
        Objects = Rhino.RhinoDoc.ActiveDoc.Objects.FindByLayer(l)
        if "作図データ" in rs.LayerName(name):
            continue
        f.write(rs.LayerName(name).encode('utf-8') + ',' +str(len(Rhino.RhinoDoc.ActiveDoc.Objects.FindByLayer(l)))+ ',')
        if any(map(rs.LayerName(name).__contains__,("壁", "屋根","床", "天井", "ガラス", "外部", "階段","仮設","屋根"))):
            CalculateArea(Objects)
        if any(map(rs.LayerName(name).__contains__,("建具","サッシ"))):
            CountWindow(Objects)
        if any(map(rs.LayerName(name).__contains__,("手摺","格子","目地","付帯"))):
            CalculateLength(Objects)
        f.write("\n")

f.close()

rs.MessageBox("数量拾いが完了しました",0)