-- Function for pagination
CREATE OR REPLACE FUNCTION get_contacts_paginated(
    p_limit INTEGER, 
    p_offset INTEGER
)
RETURNS TABLE(
    id INTEGER, 
    first_name VARCHAR, 
    last_name VARCHAR, 
    email VARCHAR, 
    birthday DATE, 
    group_name VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    SELECT c.id, c.first_name, c.last_name, c.email, c.birthday, g.name
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.id
    ORDER BY c.first_name
    LIMIT p_limit OFFSET p_offset;
END;
$$ LANGUAGE plpgsql;

-- Function for global search across all fields including phones
CREATE OR REPLACE FUNCTION search_contacts(p_query TEXT)
RETURNS TABLE(
    id INTEGER, 
    first_name VARCHAR, 
    last_name VARCHAR,
    email VARCHAR, 
    birthday DATE,
    group_name VARCHAR,
    phones TEXT
) AS $$
BEGIN
    RETURN QUERY
    SELECT DISTINCT 
        c.id, 
        c.first_name, 
        c.last_name,
        c.email, 
        c.birthday, 
        COALESCE(g.name, 'No group')::VARCHAR,
        COALESCE(string_agg(DISTINCT p.phone || ' (' || p.type || ')', ', '), '')::TEXT as phones
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.id
    LEFT JOIN phones p ON c.id = p.contact_id
    WHERE 
        c.first_name ILIKE '%' || p_query || '%'
        OR c.last_name ILIKE '%' || p_query || '%'
        OR c.email ILIKE '%' || p_query || '%'
        OR g.name ILIKE '%' || p_query || '%'
        OR p.phone ILIKE '%' || p_query || '%'
    GROUP BY c.id, c.first_name, c.last_name, c.email, c.birthday, g.name
    ORDER BY c.first_name;
END;
$$ LANGUAGE plpgsql;