import trimesh
import numpy as np

#loading the image
mesh=trimesh.load("image_smpl.obj",process=False)

def calculate_circumference(mesh, height_z):
    
    #1 find standing axis
    upaxis=np.argmax(mesh.extents)

    #2 define normal to the cutting plane and cutting height
    plane_normal=[0,0,0]
    plane_origin=[0,0,0]
    plane_normal[upaxis]=1
    plane_origin[upaxis]=height_z

    #3 cut along the height along the correct plane
    section=mesh.section(plane_origin=plane_origin,plane_normal=plane_normal)

    if section is None: #if the plane didnt cut through any part of the body
        return 0,None
    
    #4 find the torso points and calculate the length of it since there could also be arms at the cutting height
    loops=section.discrete
    
    if len(loops)==0: #if no cut was made
        return 0,None
    
    torso_points=0
    max_length=0

    for loop in loops:
        segment_length=np.linalg.norm(loop[1:]-loop[:-1],axis=1)
        total_length=np.sum(segment_length)+np.linalg.norm(loop[-1]-loop[0])

        if total_length>max_length:
            max_length=total_length
            torso_points=loop

    #5 for visual representation
    closed_path=np.vstack([torso_points,torso_points[0]])
    visual_ring=trimesh.load_path(closed_path)

    return max_length,visual_ring

#to find the height of the body and estimate the waist height
upaxis=np.argmax(mesh.extents)
lowest_point=mesh.bounds[0,upaxis]
highest_point=mesh.bounds[1,upaxis]
full_height=highest_point-lowest_point
target_height=lowest_point+(0.6*full_height)

waist_val,waist_visual=calculate_circumference(mesh,target_height)

print(f"Total height={full_height:.4f} m")
print(f"Waist height={target_height:.4f} m")
print(f"Waist circumference={waist_val:.4f} m")

#coloring
waist_visual.colors=[[255,0,0,255]]*len(waist_visual.entities)
mesh.visual.face_colors=[100,100,100,100]

#output
scene=trimesh.Scene([mesh,waist_visual])
scene.show()