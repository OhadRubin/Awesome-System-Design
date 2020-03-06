import json

def parse_pose(context, snapshot):
    pose_obj = dict(t_x=snapshot.pose.translation.x,
                    t_y=snapshot.pose.translation.y,
                    t_z=snapshot.pose.translation.z,
                    r_x=snapshot.pose.rotation.x,
                    r_y=snapshot.pose.rotation.y,
                    r_z=snapshot.pose.rotation.z,
                    r_w=snapshot.pose.rotation.w)
    res = json.dumps(pose_obj)
    context.save('pose.json', res)
    return pose_obj

parse_pose.field = "pose"


