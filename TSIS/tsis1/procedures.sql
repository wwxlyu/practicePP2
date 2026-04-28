-- Upsert (вставка или обновление телефона)
CREATE OR REPLACE PROCEDURE upsert_contact(p_name VARCHAR, p_phone VARCHAR)
AS $$
BEGIN
    INSERT INTO phonebook (username, phone_number)
    VALUES (p_name, p_phone)
    ON CONFLICT (username) 
    DO UPDATE SET phone_number = EXCLUDED.phone_number;
END;
$$ LANGUAGE plpgsql;

--дилейт
CREATE OR REPLACE PROCEDURE delete_contact_proc(p_ident VARCHAR)
AS $$
BEGIN
    DELETE FROM phonebook WHERE username = p_ident OR phone_number = p_ident;
END;
$$ LANGUAGE plpgsql;

-- массовая вставка с валидацией
-- принимает массив имен и массив телефонов
CREATE OR REPLACE FUNCTION insert_many_with_validation(p_names VARCHAR[], p_phones VARCHAR[])
RETURNS TABLE (invalid_name VARCHAR, invalid_phone VARCHAR) AS $$
DECLARE
    i INT;
BEGIN
    FOR i IN 1 .. array_upper(p_names, 1) LOOP
        -- простая валидация: номер должен состоять только из цифр и быть длиннее 10 символов
        IF p_phones[i] ~ '^[0-9]+$' AND length(p_phones[i]) >= 10 THEN
            INSERT INTO phonebook (username, phone_number)
            VALUES (p_names[i], p_phones[i])
            ON CONFLICT (username) DO UPDATE SET phone_number = EXCLUDED.phone_number;
        ELSE
            -- если данные неверны, добавляем их в таблицу "плохих" данных для возврата
            invalid_name := p_names[i];
            invalid_phone := p_phones[i];
            RETURN NEXT;
        END IF;
    END LOOP;
END;
$$ LANGUAGE plpgsql;