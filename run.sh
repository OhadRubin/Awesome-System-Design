sudo docker run -d -p 5672:5672 rabbitmq
sudo docker run -d -p 5432:5432 postgres

python -m asd.parsers run-parser 'pose' '127.0.0.1'

python -m asd.parsers run-parser 'feelings' '127.0.0.1'

python -m asd.parsers run-parser 'color_image' '127.0.0.1'

python -m asd.parsers run-parser 'depth_image' '127.0.0.1'


python -m asd.client upload-sample -h 127.0.0.1 --port 8000 asd/tiny.mind.gz
#+>> python -m asd.client upload-sample -h 127.0.0.1 --port 8000 scaffolding_files/tiny.mind.gz
python -m asd.db create-db


python -m asd.saver save '127.0.0.1'

python -m asd.server run-server -h '127.0.0.1' -p 8000
#docker run --name postgres1 -e POSTGRES_PASSWORD=asd -e POSTGRES_USER=asd -p 5432:5432 -d postgres
#docker run --name mysql1 -e MYSQL_USER=asd -e MYSQL_PASSWORD=asd  -e MYSQL_DATABASE=asd -p 3306:3306 -d mysql

#python -m asd.db create-db -a "mysql://asd:asd@localhost:3306/asd"
python -m asd.db create-db -a "sqlite:///./data/asd.sqlite"
python -m asd.client upload-sample -h 127.0.0.1 --port 8000 ../sample.mind.gz