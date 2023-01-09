vdma0.writechannel.stop()
vdma0.readchannel.stop()
vdma1.writechannel.stop()
vdma1.readchannel.stop()
vdma0.writechannel.start()
vdma0.readchannel.start()
vdma1.writechannel.start()
vdma1.readchannel.start()
t1=0
t2=0
while 1:
    rgb_frame=vdma0.readchannel.readframe()
    frame_out[:]=rgb_frame
    vdma0.writechannel.writeframe(frame_out)
    cv2.waitKey(2)
    p1_left=target_detect_ip.read(0*4)
    p1_top=target_detect_ip.read(1*4)
    p1_right = target_detect_ip.read(2*4)
    p1_bottom = target_detect_ip.read(3*4)

    p2_left=target_detect_ip.read(4*4)
    p2_top=target_detect_ip.read(5*4)
    p2_right = target_detect_ip.read(6*4)
    p2_bottom = target_detect_ip.read(7*4)

    p3_left=target_detect_ip.read(8*4)
    p3_top=target_detect_ip.read(9*4)
    p3_right = target_detect_ip.read(10*4)
    p3_bottom = target_detect_ip.read(11*4)
    #=============================================
    if p1_left < p2_left:
        object_2d_position[0, 0] = (p1_left+p1_right)/2
        object_2d_position[0, 1] = (p1_top+p1_bottom)/2
        object_2d_position[1, 0] = (p2_left+p2_right)/2
        object_2d_position[1, 1] = (p2_top+p2_bottom)/2
    else:
        object_2d_position[0, 0] = (p2_left+p2_right)/2
        object_2d_position[0, 1] = (p2_top+p2_bottom)/2
        object_2d_position[1, 0] = (p1_left+p1_right)/2
        object_2d_position[1, 1] = (p1_top+p1_bottom)/2
    object_2d_position[2, 0] = (p3_left+p3_right)/2
    object_2d_position[2, 1] = (p3_top+p3_bottom)/2
        
    object_2d_position[3, 0] = ( (object_2d_position[0, 0]+object_2d_position[1, 0])/2 + object_2d_position[2, 0])/2
    object_2d_position[3, 1] = ( (object_2d_position[0, 1]+object_2d_position[1, 1])/2 + object_2d_position[2, 1])/2
    #==============================================
    if object_2d_position.all()!=0 :
        _, rvec, tvec = cv2.solvePnP(object_3d_position, object_2d_position, stereo_cam_mt,stereo_cam_ds) 
        distance = math.sqrt(tvec[0] ** 2 + tvec[1] ** 2 + tvec[2] ** 2) 
        rvec_matrix = cv2.Rodrigues(rvec)[0]
        proj_matrix = np.hstack((rvec_matrix, tvec))
        eulerAngles = cv2.decomposeProjectionMatrix(proj_matrix)[6] 
        pitch, yaw, roll = eulerAngles[0], eulerAngles[1], eulerAngles[2]
#     ========================================================================================
        #send_data = "Depth_distance: %.2fmm,3d pose: yaw: %.2f, pitch: %.2f, roll: %.2f" % (distance, yaw, pitch, roll)
        
        posDic = {}
        posList = eulerAngles.tolist()
       
        #posList.append(eulerAngles)
        posDic["BallCue"] = posList
        send_data = json.dumps(posDic)
        udp_socket.sendto(send_data.encode("utf-8"), (dst_ip, dst_port)).2f, roll: %.2f" % (distance, yaw, pitch, roll)
        #send_data = "Depth_distance: %.2fmm,3d pose: yaw: %.2f, pitch: %.2f, roll: %.2f" % (distance, yaw, pitch, roll)
        
        posDic = {}
        posList = eulerAngles.tolist()
       
        #posList.append(eulerAngles)
        posDic["BallCue"] = posList
        send_data = json.dumps(posDic)
        udp_socket.sendto(send_data.encode("utf-8"), (dst_ip, dst_port))
    #===============================================
    else:
        send_data="target points not found."
        udp_socket.sendto(send_data.encode("utf-8"), (dst_ip, dst_port))
    cv2.waitKey(1)
vdma0.writechannel.stop()
vdma0.readchannel.stop()
vdma1.writechannel.stop()
vdma1.readchannel.stop()