# 1. 選擇基礎 Image（別人已經做好的、裝好 Python 環境的模板）
FROM python:3.14-slim

# 2. 在 Container 內設定工作目錄
WORKDIR /app

# 3. 先複製套件描述檔，安裝套件（這樣做是為了加速之後的重複建置）
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. 複製其餘所有程式碼進去
COPY . .

# 5. 告訴 Docker 這個服務會用到的 port
EXPOSE 8000

# 6. Container 啟動時要執行的指令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
