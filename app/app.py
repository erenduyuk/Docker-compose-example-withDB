import streamlit as st
from sqlalchemy import create_engine, Column, Integer, String, Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import time

# PostgreSQL veritabanı bağlantı bilgileri
DATABASE_URL = "postgresql://admin:admin@database:5432/postgres"

# Veritabanı bağlantısı oluştur
engine = create_engine(DATABASE_URL)
Base = declarative_base()

# Log tablosunu tanımla
class Log(Base):
    __tablename__ = 'logs'
    id = Column(Integer, Sequence('log_id_seq'), primary_key=True)
    message = Column(String(250))

# Oturum oluştur
Session = sessionmaker(bind=engine)

# Veritabanına bağlanmayı ve tabloyu oluşturmayı deneyin
connected = False
while not connected:
    try:
        # Veritabanını oluştur
        Base.metadata.create_all(engine)
        connected = True
    except Exception as e:
        st.write("Veritabanına bağlanma denemesi: ", e)
        time.sleep(5)  # Bağlantı hatası durumunda 5 saniye bekleyin ve tekrar deneyin

session = Session()

# Başlık
st.title("Basit Streamlit Uygulaması")

# Buton
if st.button('Log Mesajı Yazdır'):
    new_log = Log(message='Butona basıldı!')
    session.add(new_log)
    session.commit()
    st.write("Log mesajı veritabanına yazdırıldı.")
