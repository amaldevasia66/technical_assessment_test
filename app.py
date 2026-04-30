import trimesh
import numpy as np

mesh=trimesh.load("image_smpl.obj",process=False)

upaxis=np.argmax(mesh.extents)


lowest_point=mesh.bounds[0,upaxis]
highest_point=mesh.bounds[1,upaxis]
full_height=highest_point-lowest_point
target_height=lowest_point+(0.6*full_height)



def waist_calculator(mesh,height_z):
    plane_origin=[0,0,0]
    plane_normal=[0,0,0]
    upaxis=np.argmax(mesh.extents)
    plane_normal[upaxis]=1
    plane_origin[upaxis]=height_z
    section=mesh.section(plane_normal=plane_normal,plane_origin=plane_origin)

    if section is None:
        return 0,None
    loops=section.discrete
    if len(loops)==0:
        return 0,None
    
    max_l=0
    torso_points=0

    for loop in loops:
        section_length=np.linalg.norm(loop[1:]-loop[:-1],axis=1)
        total_len=np.sum(section_length)+np.linalg.norm(loop[-1]-loop[0])

        if total_len>max_l:
            max_l=total_len
            torso_points=loop

    closed_path=np.vstack([torso_points,torso_points[0]])
    visual_ring=trimesh.load_path(closed_path)

    return max_l,visual_ring

waist_len,waist_visual=waist_calculator(mesh,target_height)
print(f"total waist circum:{waist_len}")
waist_visual.colors=[[255,0,0,255]]*len(waist_visual.entities)
mesh.visual.face_colors=[100,100,100,100]
scene=trimesh.Scene([mesh,waist_visual])
scene.show()
    
