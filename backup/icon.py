import matrix, numpy as np, pygame, copy
rotation_matrix = matrix.rotation_matrix

def drawIcon(screen,pos,rot,size,color=[(255,255,255),(100,100,100)],line_thickness=2,icon={"layers":[]}):
    # draw icon
    for o in icon["layers"]:
        # if the layer is made of paths
        if o["type"] == "paths":
            paths = o["paths"]
            # draw all paths
            for p in paths:
                # calculate the path position rotated
                pa = rotation_matrix(rot,p["from"],size)
                pb = rotation_matrix(rot,p["to"],size)
                # make it relativ to the center
                pa = np.add(pa,pos)
                pb = np.add(pb,pos)
                # draw the path
                pygame.draw.line(screen,color[p["col"]],pa,pb,int(line_thickness))
        # if the layer is made of polygons
        elif o["type"] == "polygons":
            polygons = o["polygons"]
            # draw all polygons
            for p in polygons:
                lp = copy.deepcopy( p )
                # calculate the path position rotated
                for i in range(len(p["p"])):
                    lp["p"][i] = rotation_matrix(rot,lp["p"][i],size)
                # make it relativ to the center
                for i in range(len(p["p"])):
                    lp["p"][i] = np.add(lp["p"][i],pos)
                # draw the polygon
                pygame.draw.polygon(screen,color[lp["col"]],lp["p"])

        elif o["type"] == "circles":
            circles = o["circles"]
            # draw all circles
            for c in circles:
                # calculate the path position rotated
                p = rotation_matrix(rot,c["p"],size)
                # make it relativ to the center
                p = np.add(p,pos)
                # draw circle
                pygame.draw.circle(screen,color[c["col"]],p,int(c["r"]*size),int(c["w"]*size))
