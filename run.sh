sudo docker run -d -p 5672:5672 rabbitmq

python -m asd.parsers run-parser 'pose' '127.0.0.1'

python -m asd.parsers run-parser 'feelings' '127.0.0.1'

python -m asd.parsers run-parser 'color_image' '127.0.0.1'

python -m asd.parsers run-parser 'depth_image' '127.0.0.1'


python -m asd.client upload-sample -h 127.0.0.1 --port 8000 asd/tiny.mind.gz
#+>> python -m asd.client upload-sample -h 127.0.0.1 --port 8000 scaffolding_files/tiny.mind.gz
python -m asd.db create-db


python -m asd.saver save '127.0.0.1'

python -m asd.server run-server -h '127.0.0.1' -p 8000
