-- поиск (имя или телефон)
CREATE OR REPLACE FUNCTION search_contacts(pattern TEXT)
RETURNS TABLE (id INT, username VARCHAR, phone_number VARCHAR) AS $$
BEGIN
    RETURN QUERY 
    SELECT * FROM phonebook 
    WHERE phonebook.username ILIKE '%' || pattern || '%' 
       OR phonebook.phone_number LIKE '%' || pattern || '%';
END;
$$ LANGUAGE plpgsql;

-- пагинация
CREATE OR REPLACE FUNCTION get_paginated_contacts(p_limit INT, p_offset INT)
RETURNS TABLE (id INT, username VARCHAR, phone_number VARCHAR) AS $$
BEGIN
    RETURN QUERY 
    SELECT * FROM phonebook 
    ORDER BY id 
    LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;