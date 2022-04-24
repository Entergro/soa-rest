import os.path
import pickle
from pathlib import Path

import pika
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker, declarative_base
from borb.pdf import Document
from borb.pdf import Page
from borb.pdf import SingleColumnLayout
from borb.pdf import Paragraph
from borb.pdf import Image
from borb.pdf import PDF

SQLALCHEMY_DATABASE_URL = "sqlite:///./users.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    gender = Column(String)
    image_url = Column(String, default='')
    hashed_password = Column(String)
    wins = Column(Integer, default=0)
    fails = Column(Integer, default=0)
    count_of_session = Column(Integer, default=0)
    secs = Column(Integer, default=0)

host = os.environ.get('AMQP_HOST', 'host.docker.internal')

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=host))
channel = connection.channel()

channel.queue_declare(queue='task_queue', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')


def callback(ch, method, properties, body):
    data = pickle.loads(body)
    db = SessionLocal()
    user = db.query(User).filter(User.name == data['name']).first()

    pdf = Document()
    page = Page()
    pdf.append_page(page)
    layout = SingleColumnLayout(page)

    if os.path.exists(f"images/{data['name']}.png"):
        layout.add(Image(Path(f"images/{data['name']}.png"), width=100, height=100))
        print(' [.] Add image')

    layout.add(Paragraph(f"Name: {user.name}"))
    layout.add(Paragraph(f"Email: {user.email}"))
    layout.add(Paragraph(f"Gender: {user.gender}"))
    layout.add(Paragraph(f"ImageURL: {user.image_url}"))
    layout.add(Paragraph(f"Count of sessions: {user.count_of_session}"))
    layout.add(Paragraph(f"Wins: {user.wins}"))
    layout.add(Paragraph(f"Fails: {user.fails}"))
    layout.add(Paragraph(f"Seconds: {user.secs}"))

    print(" [x] Done")
    pdffile = open(f"pdf/{data['name']}_{str(data['fileid'])}.pdf", "wb")
    PDF.dumps(pdffile, pdf)
    pdffile.close()
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='task_queue', on_message_callback=callback)

channel.start_consuming()

