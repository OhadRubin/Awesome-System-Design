import requests
from reader import Reader
import asd_pb2

addr = "http://localhost:5000"
reader = Reader()
user_fields = {"user_id": reader.user_id, "username": reader.username,
               "birthday": reader.birthday, "gender": reader.gender}

user = asd_pb2.User(**user_fields)

for i, snapshot in enumerate(reader):
    resp_result = requests.get(f'{addr}/config', data=user_fields).json()
    available_parsers = resp_result['parsers']
    snapshot_fields = {"color_image": snapshot.color_image,
                       "pose": snapshot.pose,
                       "depth_image": snapshot.depth_image,
                       "feelings": snapshot.feelings}

    snapshot = asd_pb2.Snapshot(**{parser_name: snapshot_fields[parser_name]
                                   for parser_name in available_parsers})
    packet = asd_pb2.Packet(snapshot=snapshot, user=user)
    resp = requests.post(f'{addr}/config', data=packet.SerializeToString(),
                         headers={'Content-Type': 'application/protobuf',
                                  'Content-Length': str(len(packet_b))})
    #TODO: fail gracefuly

    #     print(a.depth_image.ByteSize())
    if i == 5:
        break