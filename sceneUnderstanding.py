# type:ignore
import math
import json 


def main() -> None: 
    file = open("cube.json","r")
    vertex_dict = json.load(file)
    
    vertex_data = vertex_dict["vertex-data"]
    print(vertex_data)
    all_links = []
    all_regions = set()

    for vertex in vertex_data:
        print(vertex["id"])
        print()
        kind_list = vertex["kind-list"]
        line_vertices:list[str] = []
        regions:list[int] = []

        for element in kind_list:
            if type(element) == str:
                line_vertices.append(element)
            elif type(element) == int:
                regions.append(element)
                all_regions.add(element) 
       
        if len(line_vertices) <= 3:
           # print(vertex["coords"])
            vertex["type"] = "L"
            print("TYPE",vertex["type"])
            print("No links generated")

        elif (len(line_vertices) > 3):
            points:list[tuple[int,int]] = []

            angle_to_region:list[tuple[float,int]] = []

            points1 = vertex["coords"]
            p1_x = points1[0]
            p1_y = points1[1]
            for vertex_id in line_vertices:
                for v in vertex_data:
                    if v["id"] == vertex_id:
                        points.append(v["coords"])

            big_angles:int = 0
            small_angles:int = 0

            
            for i in range(len(points)-1):

                points2 = points[i]
                points3 = points[i+1]

                p2_x = points2[0]
                
                p2_y = points2[1]

                p3_x = points3[0]
                p3_y = points3[1]

                p2_angle = math.atan2(p2_y-p1_y, p2_x-p1_x)

                # print(p2_angle)
                # print(f"point2 angle negative: {math.degrees(p2_angle)}")


                
                p3_angle = math.atan2(p3_y-p1_y, p3_x-p1_x)
                # print(f"point3 angle negative: {math.degrees(p3_angle)}")

                angle_measure = p3_angle - p2_angle

                #print(math.degrees(angle_measure))

                final_angle = angle_measure % (2*math.pi)

                #print(f"angle: {math.degrees(final_angle)}")


                if final_angle > math.pi:
                    big_angles += 1
                elif final_angle < math.pi:
                    small_angles += 1

                angle_to_region.append((final_angle, regions[i]))

                print(angle_to_region[i])

            links:list[tuple[int,int]] = []
            if small_angles == 3:
                vertex["type"] = "FORK"
                print("Three Links Generated")
                for i in range(len(regions)):
                    # links[regions[i]] = []
                    for j in range(i + 1, len(regions)):
                        links.append((regions[i], regions[j])) 
                        # links[regions[i]].append(regions[j]) #type: ignore
                        # print()
                        print("Link created between regions", {regions[i]},{regions[j]} )
                   
                        
            elif small_angles == 2 and big_angles == 1:
                vertex["type"] = "ARROW"
                print("One link generated")
                print(regions)
                if len(regions) >= 2:
                    
                    angle_to_region.sort()

                    #print(angle_to_region)

                    links.append((angle_to_region[0][1], angle_to_region[1][1])) 

                    print("Link created between regions", {angle_to_region[0][1]},{angle_to_region[1][1]} )

            else: 
                vertex["type"] = "T"
                print("No links generated")
            print("TYPE:",vertex["type"])

            print(links)
            # printed list without the background
            print("w/o background")
            background = vertex_dict["background"]
            links = [(a, b) for (a, b) in links if background not in (a, b)]
            print(links)
            # all the links in a list 
            all_links.extend(links)
            
    nuclei: dict = {}
    background = vertex_dict["background"]
    for r in all_regions:
        if r != background:
            nuclei[r] = {"regions": [r]}
    print(nuclei)
    
    # global 
    while True:
        items = list(nuclei.items())
        for i, (a, region_a) in enumerate(items):
            for b, region_b in items[i+1:]:
                # count links
                regions_a = region_a["regions"]
                regions_b = region_b["regions"]
                count = 0
                for x, y in all_links:
                    if (x in regions_a and y in regions_b) or (x in regions_b and y in regions_a):
                        count += 1
                
                if count >= 2:
                    # merge 
                    nuclei[a]["regions"] = region_a["regions"] + region_b["regions"]
                    # delete b
                    del nuclei[b]
                    print(nuclei)
                    print(f"regions {a} and {b} now merge to make {a}")
                    break  
            else:
                continue
            break
        else:
            break  #

    # singlebody
    while True:
        for a, region_a in list(nuclei.items()):
            if len(region_a['regions']) == 1:
                # find nuclei it links to
                linked_to = []
                for b, region_b in nuclei.items():
                    if a != b:
                        # count links
                        regions_a = region_a["regions"]
                        regions_b = region_b["regions"]
                        count = 0
                        for x, y in all_links:
                            if (x in regions_a and y in regions_b) or (x in regions_b and y in regions_a):
                                count += 1
                        
                        if count > 0:
                            linked_to.append(b)
                
                # only 1 link merge
                if len(linked_to) == 1:
                    b = linked_to[0]
                    region_b = nuclei[b]
                    nuclei[b]["regions"] = region_b["regions"] + region_a["regions"]
                    
                    del nuclei[a]
                    print(f"regions {a} and {b} now merge to make {b}")
                    print(nuclei)
                    break
        else:
            break  
        
    body_num = 1
    for nuclei_key, nuclei_data in nuclei.items():
        regions_list = sorted(nuclei_data['regions'])
        regions_str = ''
        for r in regions_list:
            regions_str += ' :' + str(r)
        print(f"(BODY {body_num}. IS :{regions_str})")
        body_num += 1
    
if __name__ == "__main__":
    main()