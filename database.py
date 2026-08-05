from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from config import settings

# pool_pre_ping: SQLAlchemy 從連線池取出一條連線要拿去用之前，會先送一個輕量的「ping」測試這條連線是否還活著。
# pool_recycle: 能定期汰換舊連線，降低連線被資料庫端主動關閉的機率，但無法涵蓋「還沒到回收時間、卻因為其他原因（網路中斷、DB 重啟）意外斷線」的情況。
engine = create_engine(settings.database_url, pool_pre_ping=True, pool_recycle= 1800)

# autocommit:  所有的 INSERT/UPDATE/DELETE 都會停留在一個交易（transaction）裡，直到你自己呼叫 db.commit() 才會真正寫入資料庫；若中途出錯，你可以 db.rollback() 整批復原。這樣才能確保你的 API endpoint 裡多個資料庫操作要嘛全部成功、要嘛全部不生效（原子性）。

# autoflush: 控制 Session 是否在你每次執行查詢（如 db.query(...))前，自動把目前尚未寫入的變更（pending changes）先 flush（送到資料庫但還沒 commit）。設置False的好處是行為更可預期、少一些「查詢時意外觸發寫入」的驚訝；壞處是如果你在同一個 session 裡先新增了一筆資料、還沒 flush 就馬上查詢它，可能查不到剛剛新增的那筆，需要自己記得適時呼叫 db.flush()。
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
