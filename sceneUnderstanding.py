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
            # print(vertex["type"])
        elif (len(line_vertices) >= 3):
            points:list[tuple[int,int]] = []

            points1 = vertex["coords"]
            print(points1)
            p1_x = points1[0]
            p1_y = points1[1]

            # i:int = 0
            for vertex in vertex_data:
                if vertex["id"] in line_vertices:
                    points.append(vertex["coords"])

            big_angles:int = 0
            small_angles:int = 0

            print(points)
            
            for i in range(len(points)):

                if i == len(points) - 1:
                    points2 = points[i]
                    points3 = points[0]
                else:
                    points2 = points[i]
                    points3 = points[i+1]

                p2_x = points2[0]
                print(p2_x)
                p2_y = points2[1]
                print(p2_y)

                p3_x = points3[0]
                p3_y = points3[1]

                angle_measure = (math.atan2(p3_y-p1_y, p3_x-p1_x) - math.atan2(p2_y-p1_y, p2_x-p1_x))
                print(math.degrees(angle_measure))

                if angle_measure > 0 and angle_measure < math.pi:
                    small_angles +=1 
                elif angle_measure < 0 and angle_measure > -math.pi:
                    big_angles += 1
                
            
            print(small_angles)
            print(big_angles)

            if small_angles == 3:
                vertex["type"] = "FORK"
            elif small_angles == 2 and big_angles == 1:
                vertex["type"] = "ARROW"
            else: 
                vertex["type"] = "T"
            
            print(vertex["type"])


    # print(vertex_dict)

if __name__ == "__main__":
    main()