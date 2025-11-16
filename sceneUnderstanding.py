import math
import json 


def main() -> None: 
    file = open("cube.json","r")
    vertex_dict = json.load(file)

    vertex_data = vertex_dict["vertex-data"]
    print(vertex_data)

    for vertex in vertex_data:
        # print(vertex["id"])
        print()
        kind_list = vertex["kind-list"]
        # print(kind_list)
        line_vertices:set[str] = set()
        regions:list[int] = []

        for element in kind_list:
            if type(element) == str:
                line_vertices.add(element)
            elif type(element) == int:
                regions.append(element)

        if len(line_vertices) < 3:
            vertex["type"] = "L"
            print("TYPE",vertex["type"])
            print("No links generated")
        elif (len(line_vertices) >= 3):
            points:list[tuple[int,int]] = []

            points1 = vertex["coords"]
            # print(points1)
            p1_x = points1[0]
            p1_y = points1[1]

            # i:int = 0
            for vertex in vertex_data:
                if vertex["id"] in line_vertices:
                    points.append(vertex["coords"])

            big_angles:int = 0
            small_angles:int = 0

            # print(points)
            
            for i in range(len(points)):

                if i == len(points) - 1:
                    points2 = points[i]
                    points3 = points[0]
                else:
                    points2 = points[i]
                    points3 = points[i+1]

                p2_x = points2[0]
                
                p2_y = points2[1]

                p3_x = points3[0]
                p3_y = points3[1]

                p2_angle = math.atan2(p2_y-p1_y, p2_x-p1_x)

                
                p3_angle = math.atan2(p3_y-p1_y, p3_x-p1_x)

                # print(p2_x)
                # print(p2_y)
                # print(p2_angle)

                # print(p3_x)
                # print(p3_y)
                # print(p3_angle)

                if p3_angle > p2_angle:
                    angle_measure = p3_angle - p2_angle
                else: 
                    angle_measure = p2_angle - p3_angle
                print(math.degrees(angle_measure))

                # print(angle_measure)

                # if angle_measure < 0: 
                #     angle_measure += 2*math.pi

                # print(angle_measure)

                # if angle_measure > 0 and angle_measure < math.pi:
                #     small_angles +=1 
                # elif angle_measure < 0 and angle_measure > -math.pi:
                #     big_angles += 1

                if angle_measure > math.pi:
                    big_angles += 1
                elif angle_measure < math.pi:
                    small_angles += 1
            
            # print(small_angles)
            # print(big_angles)
            links = []
            if small_angles == 3:
                vertex["type"] = "FORK"
                print("Three Links Generated")
                for i in range(len(regions)):
                    for j in range(i + 1, len(regions)):
                        links.append((regions[i], regions[j]))
                        print()
                        print("Link created between regions", {regions[i]},{regions[j]} )
                        
            elif small_angles == 2 and big_angles == 1:
                vertex["type"] = "ARROW"
                print("One link generated")
                if len(regions) >= 2:
                    links.append((regions[0], regions[1]))
                    print()
                    print("Link created between regions", {regions[0]},{regions[1]} )
            else: 
                vertex["type"] = "T"
                print("No links generated")
            
            print("TYPE:",vertex["type"])

    # angle1 = math.atan2(1, 1)
    # print(f"Angle for (1, 1): {angle1} radians")

    # # Point in the third quadrant
    # angle2 = math.atan2(-1, -1)
    # print(f"Angle for (-1, -1): {angle2} radians")

    # # Point in the second quadrant
    # angle3 = math.atan2(1, -1)
    # print(f"Angle for (1, -1): {angle3} radians")

    # # Point in the fourth quadrant
    # angle4 = math.atan2(-1, 1)
    # print(f"Angle for (-1, 1): {angle4} radians")
    # # print(vertex_dict)
if __name__ == "__main__":
    main()