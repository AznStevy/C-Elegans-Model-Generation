import numpy as np

# try thin plate spline warping
def thin_plate_spline_warp_xyz(warped_pts, ctrl_pts, obj_to_warp):

    # convert everything to np array
    warped_pts = np.array(warped_pts)
    ctrl_pts = np.array(ctrl_pts)
    obj_to_warp = np.array(obj_to_warp)

    num_points = warped_pts.shape[0]
    K = np.zeros((num_points, num_points))
    for rr in np.arange(num_points):
        for cc in np.arange(num_points):
            K[rr,cc] = np.sum(np.subtract(warped_pts[rr,:], warped_pts[cc,:])**2) #R**2 
            K[cc,rr] = K[rr,cc]

    #calculate kernel function R
    K = np.maximum(K, 1e-320) 
    #K = K.* log(sqrt(K))
    K = np.sqrt(K) #
    # Calculate P matrix
    P = np.hstack((np.ones((num_points, 1)), warped_pts)) #nX4 for 3D
    # Calculate L matrix
    L_top = np.hstack((K, P))
    L_bot = np.hstack((P.T, np.zeros((4,4))))
    L = np.vstack((L_top, L_bot))

    param = np.matmul(np.linalg.pinv(L), np.vstack((ctrl_pts, np.zeros((4,3)))))
    # Calculate new coordinates (x',y',z') for each points 
    num_points_obj = obj_to_warp.shape[0]

    K = np.zeros((num_points_obj, num_points))
    gx = obj_to_warp[:,0]
    gy = obj_to_warp[:,1]
    gz = obj_to_warp[:,2]

    for nn in np.arange(num_points):
        K[:,nn] = \
        np.square(np.subtract(gx, warped_pts[nn,0])) + \
        np.square(np.subtract(gy, warped_pts[nn,1])) + \
        np.square(np.subtract(gz, warped_pts[nn,2])) # R**2
 
    K = np.maximum(K, 1e-320) 
    K = np.sqrt(K) #|R| for 3D
    gx = np.vstack(obj_to_warp[:,0])
    gy = np.vstack(obj_to_warp[:,1])
    gz = np.vstack(obj_to_warp[:,2])
    P = np.hstack((np.ones((num_points_obj,1)), gx, gy, gz))
    L = np.hstack((K, P))
    object_warped = np.matmul(L, param)
    object_warped[:,0] = np.round(object_warped[:,0]*10**3)*10**-3
    object_warped[:,1] = np.round(object_warped[:,1]*10**3)*10**-3
    object_warped[:,2] = np.round(object_warped[:,2]*10**3)*10**-3

    return object_warped

def thin_plate_spline_warp_xz(warped_pts, ctrl_pts, obj_to_warp):
    object_warped = thin_plate_spline_warp_xyz(warped_pts, ctrl_pts, obj_to_warp)

    y_diff = np.mean(ctrl_pts[:, 1]) - np.mean(warped_pts[:, 1])
    
    # go through, if x, z are 0, then make y 0 as well
    for coord_idx, coord in enumerate(object_warped):
        if not np.any(coord):
            object_warped[coord_idx, 1] = 0
        else:
            object_warped[coord_idx, 1] = obj_to_warp[coord_idx, 1] + y_diff

    return object_warped

# test tpsw
if __name__ == "__main__":
    warped_pts = [[1,2,3], [4,5,6], [7,8,9]]
    ctrl_pts = [[0,0,0], [1,2,3], [6,3,1]]
    obj_to_warp = [[3,2,5], [3,7,3]]

    coords = thin_plate_spline_warp(warped_pts, ctrl_pts, obj_to_warp)
    print(coords)
