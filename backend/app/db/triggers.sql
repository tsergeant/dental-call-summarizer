-- 1. Function: on call insert, lookup customer by phone
CREATE OR REPLACE FUNCTION populate_customer_id_on_call()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE calls
    SET customer_id = c.customer_id
    FROM customers c
    WHERE c.phone_number = NEW.phone_number
      AND calls.call_id = NEW.call_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_call_insert
AFTER INSERT ON calls
FOR EACH ROW
EXECUTE FUNCTION populate_customer_id_on_call();

-- 2. Function: on customer insert, lookup unmatched calls
CREATE OR REPLACE FUNCTION update_calls_with_new_customer()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE calls
    SET customer_id = NEW.customer_id
    WHERE phone_number = NEW.phone_number
      AND customer_id IS NULL;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_customer_insert
AFTER INSERT ON customers
FOR EACH ROW
EXECUTE FUNCTION update_calls_with_new_customer();
