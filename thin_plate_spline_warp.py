import numpy as np

# try thin plate spline warping
def thin_plate_spline_warp(warped_pts, ctrl_pts, obj_to_warp):

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

"""
def TPS(points, control_points, obj_dict):
    
    names = list(obj_dict.keys())
    obj = np.array(list(obj_dict.values()))
    
    pred_dict = {}
        
    n = points.shape[0]
    K = np.zeros((n,n))
    
    for i in range(n):
        for j in range(n):
            
            K[i,j] = np.linalg.norm(points[i]-points[j])**2
    
    K[K < 1e-320] = 1e-320
    
    K = np.sqrt(K)
    
    one_vec = np.ones((n, 1))
    P = np.hstack([one_vec, points])
        
    L = np.empty((n+4, n+4))
    L[:n, :n] = K
    L[:n, n:] = P
    L[n:, :n] = P.T
    L[n:, n:] = np.zeros((4, 4))

    vec = np.vstack([control_points, np.zeros((4,3))])
    
    L_inv = np.linalg.pinv(L)
    
    param = np.dot(L_inv, vec)
        
    ## Predict
    n_pred = obj.shape[0]
    points_pred = np.empty(n_pred)
    
    K = np.zeros((n_pred, n))
    
    gx = obj[:, 0]
    gy = obj[:, 1]
    gz = obj[:, 2]
    
    for k in range(n):
        
        K[:,k] = (gx - points[k,0])**2 + (gy - points[k,1])**2 + (gz - points[k,2])**2
        
    K[K < 1e-320] = 1e-320
    K = np.sqrt(K)
    
    P = np.array([np.ones(n_pred), gx, gy, gz])
    
    L = np.hstack([K, P.T])
    
    points_pred = np.dot(L, param)
    
    points_pred[:,1] = obj[:,1]
    
    for j in range(len(points_pred)):
        
        pred_dict[names[j]] = points_pred[j]
        
    return pred_dict """

# test tpsw
if __name__ == "__main__":
    warped_pts = [[1,2,3], [4,5,6], [7,8,9]]
    ctrl_pts = [[0,0,0], [1,2,3], [6,3,1]]
    obj_to_warp = [[3,2,5], [3,7,3]]

    coords = thin_plate_spline_warp(warped_pts, ctrl_pts, obj_to_warp)
    print(coords)
