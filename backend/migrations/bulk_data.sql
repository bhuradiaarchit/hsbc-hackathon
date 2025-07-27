
CREATE TABLE IF NOT EXISTS bulk_data (
    id SERIAL PRIMARY KEY,
    date DATE,
    symbol VARCHAR(50),
    security_name VARCHAR(100),
    client_name VARCHAR(100),
    buy_sell VARCHAR(10),
    quantity_traded BIGINT,
    trade_price DECIMAL(10,2),
    remarks TEXT
);
