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
                p2_y = points2[1]
    
                p3_x = points3[0]
                p3_y = points3[1]

                angle_measure = math.atan2(p3_y - p1_y, p3_x - p1_x) - math.atan2(p2_y - p1_y, p2_x - p1_x)
                
                # normalize to [0, 2π)
                # https://stackoverflow.com/questions/21483999/using-atan2-to-find-angle-between-two-vectors?
                angle_measure = (angle_measure + 2 * math.pi) % (2 * math.pi)
                angle_degree = math.degrees(angle_measure)

                # focusing on just the smaller angles 
                if angle_degree > 180:
                    angle_degree = 360 - angle_degree

                # using absolute value
                if abs(angle_degree - 180) < 5:   
                    big_angles += 1
                elif angle_degree > 120:         
                    big_angles += 1
                else:
                    small_angles += 1
                            

            # Classification logic
            if small_angles == 3:
                vertex["type"] = "FORK"
                print("Three links generated")
            elif small_angles == 2 and big_angles == 1:
                vertex["type"] = "ARROW"
                print("One link generated")
            else: 
                vertex["type"] = "T"
                print("No links generated")

            print("Vertex type:", vertex["type"])

if __name__ == "__main__":
    main()
