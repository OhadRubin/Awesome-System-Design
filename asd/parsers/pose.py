import json

def parse_pose(context, snapshot):
    pose_obj = dict(translation=dict(
                        x=snapshot.pose.translation.x,
                        y=snapshot.pose.translation.y,
                        z=snapshot.pose.translation.z),
                    rotation=dict(
                        x=snapshot.pose.rotation.x,
                        y=snapshot.pose.rotation.y,
                        z=snapshot.pose.rotation.z,
                        w=snapshot.pose.rotation.w)
                )
    context.save('pose.json', json.dumps(pose_obj))

parse_pose.field = "pose"


