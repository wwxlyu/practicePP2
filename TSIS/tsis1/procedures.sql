-- Procedure to add phone by contact name
CREATE OR REPLACE PROCEDURE add_phone(
    p_name VARCHAR, 
    p_phone VARCHAR, 
    p_type VARCHAR DEFAULT 'mobile'
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_id INTEGER;
BEGIN
    SELECT id INTO v_id FROM contacts WHERE first_name = p_name LIMIT 1;
    
    IF v_id IS NOT NULL THEN
        INSERT INTO phones (contact_id, phone, type) VALUES (v_id, p_phone, p_type);
        RAISE NOTICE 'Phone added successfully';
    ELSE
        RAISE EXCEPTION 'Contact "%" not found', p_name;
    END IF;
END;
$$;

-- Procedure to move contact to group (creates group if doesn't exist)
CREATE OR REPLACE PROCEDURE move_to_group(
    p_name VARCHAR, 
    p_group_name VARCHAR
)
LANGUAGE plpgsql
AS $$
DECLARE
    v_contact_id INTEGER;
    v_group_id INTEGER;
BEGIN
    SELECT id INTO v_contact_id FROM contacts WHERE first_name = p_name LIMIT 1;
    
    IF v_contact_id IS NULL THEN
        RAISE EXCEPTION 'Contact "%" not found', p_name;
    END IF;
    
    -- Create group if it doesn't exist
    INSERT INTO groups (name) VALUES (p_group_name) ON CONFLICT (name) DO NOTHING;
    SELECT id INTO v_group_id FROM groups WHERE name = p_group_name;
    
    -- Update contact's group
    UPDATE contacts SET group_id = v_group_id WHERE id = v_contact_id;
    RAISE NOTICE 'Contact moved to group "%"', p_group_name;
END;
$$;