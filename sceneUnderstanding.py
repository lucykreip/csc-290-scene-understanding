import math
import json 


def main() -> None: 
    file = open("one.json","r")
    vertex_dict = json.load(file)

    vertex_data = vertex_dict["vertex-data"]
    print(vertex_data)

    for vertex in vertex_data:
        print(vertex["id"])
        print()
        kind_list = vertex["kind-list"]
        # print(kind_list)
        # line_vertices:set[str] = set()
        line_vertices:list[str] = []
        regions:list[int] = []

        for element in kind_list:
            if type(element) == str:
                # line_vertices.add(element)
                line_vertices.append(element)
            elif type(element) == int:
                regions.append(element)

        if len(line_vertices) <= 3:
            print(vertex["coords"])
            vertex["type"] = "L"
            print("TYPE",vertex["type"])
            print("No links generated")

        elif (len(line_vertices) > 3):
            points:list[tuple[int,int]] = []

            angle_to_region:list[tuple[float,int]] = []

            points1 = vertex["coords"]
            p1_x = points1[0]
            p1_y = points1[1]

            # i:int = 0
            # for vertex in vertex_data:
            #     if vertex["id"] in line_vertices:
            #         points.append(vertex["coords"])

            for vertex_id in line_vertices:
                for vertex in vertex_data:
                    if vertex["id"] == vertex_id:
                        points.append(vertex["coords"])

            print(line_vertices)
            print(points1)
            print(points)



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
                # p2_angle = math.atan2(p1_y-p2_y, p1_x-p2_x)


                print(math.degrees(p2_angle))

                # print(p2_angle)
                # print(f"point2 angle negative: {math.degrees(p2_angle)}")


                
                p3_angle = math.atan2(p3_y-p1_y, p3_x-p1_x)
                # p3_angle = math.atan2(p1_y-p3_y, p1_x-p3_x)
                print(math.degrees(p3_angle))
                # print(f"point3 angle negative: {math.degrees(p3_angle)}")

                angle_measure = p3_angle - p2_angle

                print(math.degrees(angle_measure))

                final_angle = angle_measure % (2*math.pi)

                print(f"angle: {math.degrees(final_angle)}")


                if final_angle > math.pi:
                    big_angles += 1
                elif final_angle < math.pi:
                    small_angles += 1

                angle_to_region.append((final_angle, regions[i]))

                print(angle_to_region[i])

            links:list[tuple[int,int]] = []
            # links:dict[int, list[int]] = {}
            if small_angles == 3:
                vertex["type"] = "FORK"
                print("Three Links Generated")
                for i in range(len(regions)):
                    # links[regions[i]] = []
                    for j in range(i + 1, len(regions)):
                        links.append((regions[i], regions[j])) #type: ignore
                        # links[regions[i]].append(regions[j]) #type: ignore
                        # print()
                        print("Link created between regions", {regions[i]},{regions[j]} )
                    # print("Link created between regions", {regions[i]},{links.get(regions[i])}) #type: ignore
                        
            elif small_angles == 2 and big_angles == 1:
                vertex["type"] = "ARROW"
                print("One link generated")
                print(regions)
                if len(regions) >= 2:
                    
                    angle_to_region.sort()

                    print(angle_to_region)

                    links.append((angle_to_region[0][1], angle_to_region[1][1])) #type: ignore

                    print("Link created between regions", {angle_to_region[0][1]},{angle_to_region[1][1]} )

            else: 
                vertex["type"] = "T"
                print("No links generated")
            
            print("TYPE:",vertex["type"])

            print(links)

    


if __name__ == "__main__":
    main()