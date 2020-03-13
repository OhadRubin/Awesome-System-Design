# import pytest
# import sh
#
# # @pytest.fixture
# # def packet():
# #     import asd.asd_pb2
# #     reader = asd.reader.Reader("asd/sample.mind.gz")
# #
# #     el = next(iter(reader))
# #     user = asd.asd_pb2.User(user_id=reader.user_id,
# #                             username=reader.username,
# #                             birthday=reader.birthday,
# #                             gender=reader.gender)
# #     packet = asd.asd_pb2.Packet(snapshot=el, user=user).SerializeToString()
# #     return packet
#
#
# def test_save():
#     from asd.saver import Saver
#     saver = Saver(database_url)
#     data = None
#     saver.save('pose', data)
#
# #
# #
# # def test_save_raw_data():
# #     cmd = """python -m asd.saver save --database 'postgresql://127.0.0.1:5432' 'pose' 'pose.result'"""
# #     sh.bash(cmd)
# #
# #
# # def test_run_parser_cli():
# #     cmd = """python -m asd.saver run-saver 'postgresql://127.0.0.1:5432' 'rabbitmq://127.0.0.1:5672/'"""
# #     sh.bash(cmd)
# #
#
#
# python -m asd.saver save sqlite:///asd_db.sqlite pose asd/pose2.result